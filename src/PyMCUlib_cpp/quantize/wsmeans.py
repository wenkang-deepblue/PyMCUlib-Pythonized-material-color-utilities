# wsmeans.py

from typing import Dict, List
import random
from PyMCUlib_cpp.utils.utils import Argb
from PyMCUlib_cpp.quantize.lab import Lab, lab_from_int, int_from_lab

# Constants
MAX_ITERATIONS = 100
MIN_DELTA_E = 3.0

class QuantizerResult:
    """
    Result of color quantization.
    Contains a mapping of colors to their frequency counts
    and a mapping of input pixels to their corresponding cluster pixels.
    """
    def __init__(self):
        self.color_to_count: Dict[Argb, int] = {}
        self.input_pixel_to_cluster_pixel: Dict[Argb, Argb] = {}

class Swatch:
    """Represents a color swatch with its population count."""
    def __init__(self, argb: Argb = 0, population: int = 0):
        self.argb = argb
        self.population = population
    
    def __lt__(self, other):
        """For sorting swatches by population in descending order."""
        return self.population > other.population

class DistanceToIndex:
    """Associates a distance with an index."""
    def __init__(self, distance: float = 0.0, index: int = 0):
        self.distance = distance
        self.index = index
    
    def __lt__(self, other):
        """For sorting by distance in ascending order."""
        return self.distance < other.distance

def quantize_wsmeans(input_pixels: List[Argb], 
                     starting_clusters: List[Argb], 
                     max_colors: int) -> QuantizerResult:
    """
    Quantizes colors using a weighted spherical k-means algorithm.
    
    Args:
        input_pixels: List of pixels in ARGB format.
        starting_clusters: Initial cluster centers in ARGB format.
        max_colors: Maximum number of colors to generate.
        
    Returns:
        A QuantizerResult with mappings of colors to counts and input pixels to cluster pixels.
    """
    if max_colors == 0 or not input_pixels:
        return QuantizerResult()
    
    if max_colors > 256:
        # If colors is outside the range, just set it the max
        max_colors = 256
    
    pixel_count = len(input_pixels)
    pixel_to_count = {}
    pixels = []
    points = []
    
    # Process input pixels to count unique colors
    for pixel in input_pixels:
        if pixel in pixel_to_count:
            pixel_to_count[pixel] += 1
        else:
            pixels.append(pixel)
            points.append(lab_from_int(pixel))
            pixel_to_count[pixel] = 1
    
    cluster_count = min(max_colors, len(points))
    
    if starting_clusters:
        cluster_count = min(cluster_count, len(starting_clusters))
    
    pixel_count_sums = [0] * 256
    clusters = []
    
    # Initialize clusters from starting_clusters
    for argb in starting_clusters:
        clusters.append(lab_from_int(argb))
    
    # Add random clusters if needed
    random.seed(42688)
    additional_clusters_needed = cluster_count - len(clusters)
    
    if not starting_clusters and additional_clusters_needed > 0:
        for i in range(additional_clusters_needed):
            # Adds a random Lab color to clusters
            l = random.random() * 100.0
            a = random.random() * 200.0 - 100.0
            b = random.random() * 200.0 - 100.0
            clusters.append(Lab(l, a, b))
    
    # Initialize cluster assignments randomly
    cluster_indices = []
    random.seed(42688)
    for i in range(len(points)):
        cluster_indices.append(random.randint(0, cluster_count - 1))
    
    index_matrix = [[0 for _ in range(cluster_count)] for _ in range(cluster_count)]
    distance_to_index_matrix = [[DistanceToIndex() for _ in range(cluster_count)] for _ in range(cluster_count)]
    
    # Main iteration loop
    for iteration in range(MAX_ITERATIONS):
        # Calculate cluster distances
        for i in range(cluster_count):
            distance_to_index_matrix[i][i].distance = 0
            distance_to_index_matrix[i][i].index = i
            
            for j in range(i + 1, cluster_count):
                distance = clusters[i].delta_e(clusters[j])
                
                distance_to_index_matrix[j][i].distance = distance
                distance_to_index_matrix[j][i].index = i
                distance_to_index_matrix[i][j].distance = distance
                distance_to_index_matrix[i][j].index = j
            
            row = distance_to_index_matrix[i].copy()
            row.sort()
            
            for j in range(cluster_count):
                index_matrix[i][j] = row[j].index
        
        # Reassign points
        color_moved = False
        
        for i in range(len(points)):
            point = points[i]
            
            previous_cluster_index = cluster_indices[i]
            previous_cluster = clusters[previous_cluster_index]
            previous_distance = point.delta_e(previous_cluster)
            minimum_distance = previous_distance
            new_cluster_index = -1
            
            for j in range(cluster_count):
                if distance_to_index_matrix[previous_cluster_index][j].distance >= 4 * previous_distance:
                    continue
                
                distance = point.delta_e(clusters[j])
                if distance < minimum_distance:
                    minimum_distance = distance
                    new_cluster_index = j
            
            if new_cluster_index != -1:
                distance_change = abs(pow(minimum_distance, 0.5) - pow(previous_distance, 0.5))
                if distance_change > MIN_DELTA_E:
                    color_moved = True
                    cluster_indices[i] = new_cluster_index
        
        if not color_moved and iteration != 0:
            break
        
        # Recalculate cluster centers
        component_a_sums = [0.0] * 256
        component_b_sums = [0.0] * 256
        component_c_sums = [0.0] * 256
        
        for i in range(cluster_count):
            pixel_count_sums[i] = 0
        
        for i in range(len(points)):
            cluster_index = cluster_indices[i]
            point = points[i]
            count = pixel_to_count[pixels[i]]
            
            pixel_count_sums[cluster_index] += count
            component_a_sums[cluster_index] += (point.l * count)
            component_b_sums[cluster_index] += (point.a * count)
            component_c_sums[cluster_index] += (point.b * count)
        
        for i in range(cluster_count):
            count = pixel_count_sums[i]
            if count == 0:
                clusters[i] = Lab(0, 0, 0)
                continue
            
            a = component_a_sums[i] / count
            b = component_b_sums[i] / count
            c = component_c_sums[i] / count
            clusters[i] = Lab(a, b, c)
    
    # Prepare the result
    swatches = []
    cluster_argbs = []
    all_cluster_argbs = []
    
    for i in range(cluster_count):
        possible_new_cluster = int_from_lab(clusters[i])
        all_cluster_argbs.append(possible_new_cluster)
        
        count = pixel_count_sums[i]
        if count == 0:
            continue
        
        use_new_cluster = 1
        for j in range(len(swatches)):
            if swatches[j].argb == possible_new_cluster:
                swatches[j].population += count
                use_new_cluster = 0
                break
        
        if use_new_cluster == 0:
            continue
        
        cluster_argbs.append(possible_new_cluster)
        swatches.append(Swatch(possible_new_cluster, count))
    
    swatches.sort()
    
    # Construct the final result
    result = QuantizerResult()
    for swatch in swatches:
        result.color_to_count[swatch.argb] = swatch.population
    
    for i in range(len(points)):
        pixel = pixels[i]
        cluster_index = cluster_indices[i]
        cluster_argb = all_cluster_argbs[cluster_index]
        result.input_pixel_to_cluster_pixel[pixel] = cluster_argb
    
    return result