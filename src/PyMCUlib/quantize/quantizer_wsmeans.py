# quantize/quantizer_wsmeans.py

from typing import Dict, List
import random
from PyMCUlib.quantize.lab_point_provider import LabPointProvider

# Constants
MAX_ITERATIONS = 10
MIN_MOVEMENT_DISTANCE = 3.0


class DistanceAndIndex:
    """
    A wrapper for maintaining a table of distances between K-Means clusters.
    """
    def __init__(self):
        self.distance = -1
        self.index = -1
        
    def __lt__(self, other):
        """
        Allows for sorting DistanceAndIndex objects by distance.
        """
        return self.distance < other.distance


class QuantizerWsmeans:
    """
    An image quantizer that improves on the speed of a standard K-Means algorithm
    by implementing several optimizations, including deduping identical pixels
    and a triangle inequality rule that reduces the number of comparisons needed
    to identify which cluster a point should be moved to.

    Wsmeans stands for Weighted Square Means.

    This algorithm was designed by M. Emre Celebi, and was found in their 2011
    paper, Improving the Performance of K-Means for Color Quantization.
    https://arxiv.org/abs/1101.0395
    """

    @staticmethod
    def quantize(
        input_pixels: List[int], 
        starting_clusters: List[int],
        max_colors: int
    ) -> Dict[int, int]:
        """
        Args:
            input_pixels: Colors in ARGB format.
            starting_clusters: Defines the initial state of the quantizer. Passing
                an empty array is fine, the implementation will create its own initial
                state that leads to reproducible results for the same inputs.
                Passing an array that is the result of Wu quantization leads to higher
                quality results.
            max_colors: The number of colors to divide the image into. A lower
                number of colors may be returned.
            
        Returns:
            Map with keys of colors in ARGB format, and values of number of
            pixels in the original image that correspond to the color in the
            quantized image.
        """
        pixel_to_count = {}
        points = []
        pixels = []
        point_provider = LabPointProvider()
        point_count = 0
        
        # Deduplicate pixels
        for input_pixel in input_pixels:
            pixel_count = pixel_to_count.get(input_pixel)
            if pixel_count is None:
                point_count += 1
                points.append(point_provider.from_int(input_pixel))
                pixels.append(input_pixel)
                pixel_to_count[input_pixel] = 1
            else:
                pixel_to_count[input_pixel] = pixel_count + 1
        
        counts = [0] * point_count
        for i in range(point_count):
            pixel = pixels[i]
            count = pixel_to_count.get(pixel)
            if count is not None:
                counts[i] = count
        
        cluster_count = min(max_colors, point_count)
        if len(starting_clusters) > 0:
            cluster_count = min(cluster_count, len(starting_clusters))
        
        # Initialize clusters
        clusters = []
        for i in range(len(starting_clusters)):
            clusters.append(point_provider.from_int(starting_clusters[i]))
        
        additional_clusters_needed = cluster_count - len(clusters)
        if len(starting_clusters) == 0 and additional_clusters_needed > 0:
            for i in range(additional_clusters_needed):
                l = random.random() * 100.0
                a = random.random() * (100.0 - (-100.0) + 1) + -100
                b = random.random() * (100.0 - (-100.0) + 1) + -100
                clusters.append([l, a, b])
        
        cluster_indices = []
        for i in range(point_count):
            cluster_indices.append(random.randint(0, cluster_count - 1))
        
        # Initialize index matrix and distance-to-index matrix
        index_matrix = []
        for i in range(cluster_count):
            index_matrix.append([0] * cluster_count)
        
        distance_to_index_matrix = []
        for i in range(cluster_count):
            distance_to_index_matrix.append([DistanceAndIndex() for _ in range(cluster_count)])
        
        pixel_count_sums = [0] * cluster_count
        
        # Main iteration loop
        for iteration in range(MAX_ITERATIONS):
            # Calculate distances between clusters
            for i in range(cluster_count):
                for j in range(i + 1, cluster_count):
                    distance = point_provider.distance(clusters[i], clusters[j])
                    distance_to_index_matrix[j][i].distance = distance
                    distance_to_index_matrix[j][i].index = i
                    distance_to_index_matrix[i][j].distance = distance
                    distance_to_index_matrix[i][j].index = j
                
                # Sort distances
                distance_to_index_matrix[i].sort()
                
                # Update index matrix
                for j in range(cluster_count):
                    index_matrix[i][j] = distance_to_index_matrix[i][j].index
            
            points_moved = 0
            # Assign points to clusters
            for i in range(point_count):
                point = points[i]
                previous_cluster_index = cluster_indices[i]
                previous_cluster = clusters[previous_cluster_index]
                previous_distance = point_provider.distance(point, previous_cluster)
                minimum_distance = previous_distance
                new_cluster_index = -1
                
                # Use triangle inequality to reduce comparisons
                for j in range(cluster_count):
                    if (distance_to_index_matrix[previous_cluster_index][j].distance >= 
                            4 * previous_distance):
                        continue
                    
                    distance = point_provider.distance(point, clusters[j])
                    if distance < minimum_distance:
                        minimum_distance = distance
                        new_cluster_index = j
                
                if new_cluster_index != -1:
                    distance_change = abs(
                        (minimum_distance ** 0.5) - (previous_distance ** 0.5)
                    )
                    if distance_change > MIN_MOVEMENT_DISTANCE:
                        points_moved += 1
                        cluster_indices[i] = new_cluster_index
            
            # Check for convergence
            if points_moved == 0 and iteration != 0:
                break
            
            # Update clusters
            component_a_sums = [0] * cluster_count
            component_b_sums = [0] * cluster_count
            component_c_sums = [0] * cluster_count
            
            for i in range(cluster_count):
                pixel_count_sums[i] = 0
            
            for i in range(point_count):
                cluster_index = cluster_indices[i]
                point = points[i]
                count = counts[i]
                pixel_count_sums[cluster_index] += count
                component_a_sums[cluster_index] += (point[0] * count)
                component_b_sums[cluster_index] += (point[1] * count)
                component_c_sums[cluster_index] += (point[2] * count)
            
            for i in range(cluster_count):
                count = pixel_count_sums[i]
                if count == 0:
                    clusters[i] = [0.0, 0.0, 0.0]
                    continue
                
                a = component_a_sums[i] / count
                b = component_b_sums[i] / count
                c = component_c_sums[i] / count
                clusters[i] = [a, b, c]
        
        # Generate result mapping
        argb_to_population = {}
        for i in range(cluster_count):
            count = pixel_count_sums[i]
            if count == 0:
                continue
            
            possible_new_cluster = point_provider.to_int(clusters[i])
            if possible_new_cluster in argb_to_population:
                continue
            
            argb_to_population[possible_new_cluster] = count
        
        return argb_to_population