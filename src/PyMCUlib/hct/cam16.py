# hct/cam16.py

import math
from PyMCUlib.utils import color_utils
from PyMCUlib.utils import math_utils
from PyMCUlib.hct.viewing_conditions import ViewingConditions

class Cam16:
    """
    CAM16, a color appearance model. Colors are not just defined by their hex
    code, but rather, a hex code and viewing conditions.

    CAM16 instances also have coordinates in the CAM16-UCS space, called J*, a*,
    b*, or jstar, astar, bstar in code. CAM16-UCS is included in the CAM16
    specification, and should be used when measuring distances between colors.

    In traditional color spaces, a color can be identified solely by the
    observer's measurement of the color. Color appearance models such as CAM16
    also use information about the environment where the color was
    observed, known as the viewing conditions.

    For example, white under the traditional assumption of a midday sun white
    point is accurately measured as a slightly chromatic blue by CAM16. (roughly,
    hue 203, chroma 3, lightness 100)
    """

    def __init__(
       self,
       hue: float, chroma: float, j: float, q: float,
       m: float, s: float, jstar: float, astar: float, bstar: float
    ) -> None:
        """
        All of the CAM16 dimensions can be calculated from 3 of the dimensions, in
        the following combinations:
            -  {j or q} and {c, m, or s} and hue
            - jstar, astar, bstar
        Prefer using a static method that constructs from 3 of those dimensions.
        This constructor is intended for those methods to use to return all
        possible dimensions.

        Args:
            hue: Hue in CAM16
            chroma: Chroma in CAM16, informally, colorfulness / color intensity. 
                    Like saturation in HSL, except perceptually accurate.
            j: Lightness in CAM16
            q: Brightness in CAM16; ratio of lightness to white point's lightness
            m: Colorfulness in CAM16
            s: Saturation in CAM16; ratio of chroma to white point's chroma
            jstar: CAM16-UCS J coordinate
            astar: CAM16-UCS a coordinate
            bstar: CAM16-UCS b coordinate
        """
        self.hue = hue
        self.chroma = chroma
        self.j = j
        self.q = q
        self.m = m
        self.s = s
        self.jstar = jstar
        self.astar = astar
        self.bstar = bstar
    
    def distance(self, other: 'Cam16') -> float:
        """
        CAM16 instances also have coordinates in the CAM16-UCS space, called J*,
        a*, b*, or jstar, astar, bstar in code. CAM16-UCS is included in the CAM16
        specification, and is used to measure distances between colors.

        Args:
            other: Another CAM16 instance

        Returns:
            The distance between the colors in CAM16-UCS space.
        """
        d_j = self.jstar - other.jstar
        d_a = self.astar - other.astar
        d_b = self.bstar - other.bstar
        d_e_prime = math.sqrt(d_j * d_j + d_a * d_a + d_b * d_b)
        d_e = 1.41 * math.pow(d_e_prime, 0.63)
        return d_e
    
    @classmethod
    def from_int(cls, argb: int) -> 'Cam16':
        """
        Creates a CAM16 color from an ARGB integer.

        Args:
            argb: ARGB representation of a color.

        Returns:
            CAM16 color, assuming the color was viewed in default viewing conditions.
        """
        return cls.from_int_in_viewing_conditions(argb, ViewingConditions.DEFAULT)
    
    @classmethod
    def from_int_in_viewing_conditions(
        cls,
        argb: int,
        viewing_conditions: ViewingConditions
    ) -> 'Cam16':
        """
        Creates a CAM16 color from an ARGB integer and viewing conditions.

        Args:
            argb: ARGB representation of a color.
            viewing_conditions: Information about the environment where the color
                was observed.

        Returns:
            CAM16 color
        """
        red = (argb & 0x00ff0000) >> 16
        green = (argb & 0x0000ff00) >> 8
        blue = (argb & 0x000000ff)
        red_l = color_utils.linearized(red)
        green_l = color_utils.linearized(green)
        blue_l = color_utils.linearized(blue)
        x = 0.41233895 * red_l + 0.35762064 * green_l + 0.18051042 * blue_l
        y = 0.2126 * red_l + 0.7152 * green_l + 0.0722 * blue_l
        z = 0.01932141 * red_l + 0.11916382 * green_l + 0.95034478 * blue_l
        
        r_c = 0.401288 * x + 0.650173 * y - 0.051461 * z
        g_c = -0.250268 * x + 1.204414 * y + 0.045854 * z
        b_c = -0.002079 * x + 0.048952 * y + 0.953127 * z
        
        r_d = viewing_conditions.rgb_d[0] * r_c
        g_d = viewing_conditions.rgb_d[1] * g_c
        b_d = viewing_conditions.rgb_d[2] * b_c
        
        r_af = math.pow((viewing_conditions.fl * abs(r_d)) / 100.0, 0.42)
        g_af = math.pow((viewing_conditions.fl * abs(g_d)) / 100.0, 0.42)
        b_af = math.pow((viewing_conditions.fl * abs(b_d)) / 100.0, 0.42)
        
        r_a = (math_utils.signum(r_d) * 400.0 * r_af) / (r_af + 27.13)
        g_a = (math_utils.signum(g_d) * 400.0 * g_af) / (g_af + 27.13)
        b_a = (math_utils.signum(b_d) * 400.0 * b_af) / (b_af + 27.13)
        
        a = (11.0 * r_a + -12.0 * g_a + b_a) / 11.0
        b = (r_a + g_a - 2.0 * b_a) / 9.0
        u = (20.0 * r_a + 20.0 * g_a + 21.0 * b_a) / 20.0
        p2 = (40.0 * r_a + 20.0 * g_a + b_a) / 20.0
        
        atan2 = math.atan2(b, a)
        atan_degrees = (atan2 * 180.0) / math.pi
        hue = atan_degrees if atan_degrees >= 0 else atan_degrees + 360.0
        hue = hue if hue < 360 else hue - 360.0
        hue_radians = (hue * math.pi) / 180.0
        
        ac = p2 * viewing_conditions.nbb
        
        j = 100.0 * math.pow(
            ac / viewing_conditions.aw,
            viewing_conditions.c * viewing_conditions.z)
            
        q = (4.0 / viewing_conditions.c) * math.sqrt(j / 100.0) * \
            (viewing_conditions.aw + 4.0) * viewing_conditions.fl_root
            
        hue_prime = hue + 360.0 if hue < 20.14 else hue
        
        e_hue = 0.25 * (math.cos((hue_prime * math.pi) / 180.0 + 2.0) + 3.8)
        
        p1 = (50000.0 / 13.0) * e_hue * viewing_conditions.nc * viewing_conditions.ncb
        
        t = (p1 * math.sqrt(a * a + b * b)) / (u + 0.305)
        alpha = math.pow(t, 0.9) * \
            math.pow(1.64 - math.pow(0.29, viewing_conditions.n), 0.73)
            
        c = alpha * math.sqrt(j / 100.0)
        
        m = c * viewing_conditions.fl_root
        
        s = 50.0 * \
            math.sqrt((alpha * viewing_conditions.c) / (viewing_conditions.aw + 4.0))
            
        jstar = ((1.0 + 100.0 * 0.007) * j) / (1.0 + 0.007 * j)
        mstar = (1.0 / 0.0228) * math.log(1.0 + 0.0228 * m)
        astar = mstar * math.cos(hue_radians)
        bstar = mstar * math.sin(hue_radians)
        
        return cls(hue, c, j, q, m, s, jstar, astar, bstar)
    
    @classmethod
    def from_jch(
        cls,
        j: float,
        c: float,
        h: float
    ) -> 'Cam16':
        """
        Creates a CAM16 color from J, C, and h in default viewing conditions.

        Args:
            j: Lightness
            c: Chroma
            h: Hue

        Returns:
            CAM16 color
        """
        return cls.from_jch_in_viewing_conditions(j, c, h, ViewingConditions.DEFAULT)
    
    @classmethod
    def from_jch_in_viewing_conditions(
        cls,
        j: float,
        c: float,
        h: float,
        viewing_conditions: ViewingConditions
    ) -> 'Cam16':
        """
        Creates a CAM16 color from J, C, and h in the given viewing conditions.

        Args:
            j: Lightness
            c: Chroma
            h: Hue
            viewing_conditions: Information about the environment where the color
                will be viewed.

        Returns:
            CAM16 color
        """
        q = (4.0 / viewing_conditions.c) * math.sqrt(j / 100.0) * \
            (viewing_conditions.aw + 4.0) * viewing_conditions.fl_root
            
        m = c * viewing_conditions.fl_root
        
        alpha = c / math.sqrt(j / 100.0)
        
        s = 50.0 * \
            math.sqrt((alpha * viewing_conditions.c) / (viewing_conditions.aw + 4.0))
            
        hue_radians = (h * math.pi) / 180.0
        
        jstar = ((1.0 + 100.0 * 0.007) * j) / (1.0 + 0.007 * j)
        mstar = (1.0 / 0.0228) * math.log(1.0 + 0.0228 * m)
        astar = mstar * math.cos(hue_radians)
        bstar = mstar * math.sin(hue_radians)
        
        return cls(h, c, j, q, m, s, jstar, astar, bstar)
    
    @classmethod
    def from_ucs(
        cls,
        jstar: float,
        astar: float,
        bstar: float
    ) -> 'Cam16':
        """
        Creates a CAM16 color from CAM16-UCS coordinates in default viewing conditions.

        Args:
            jstar: CAM16-UCS lightness.
            astar: CAM16-UCS a dimension. Like a* in L*a*b*, it is a Cartesian
                coordinate on the Y axis.
            bstar: CAM16-UCS b dimension. Like a* in L*a*b*, it is a Cartesian
                coordinate on the X axis.

        Returns:
            CAM16 color
        """
        return cls.from_ucs_in_viewing_conditions(
            jstar, astar, bstar, ViewingConditions.DEFAULT)
    
    @classmethod
    def from_ucs_in_viewing_conditions(
        cls,
        jstar: float,
        astar: float,
        bstar: float,
        viewing_conditions: ViewingConditions
    ) -> 'Cam16':
        """
        Creates a CAM16 color from CAM16-UCS coordinates in the given viewing conditions.

        Args:
            jstar: CAM16-UCS lightness.
            astar: CAM16-UCS a dimension. Like a* in L*a*b*, it is a Cartesian
                coordinate on the Y axis.
            bstar: CAM16-UCS b dimension. Like a* in L*a*b*, it is a Cartesian
                coordinate on the X axis.
            viewing_conditions: Information about the environment where the color
                will be viewed.

        Returns:
            CAM16 color
        """
        a = astar
        b = bstar
        m = math.sqrt(a * a + b * b)
        M = (math.exp(m * 0.0228) - 1.0) / 0.0228
        c = M / viewing_conditions.fl_root
        h = math.atan2(b, a) * (180.0 / math.pi)
        if h < 0.0:
            h += 360.0
        j = jstar / (1 - (jstar - 100) * 0.007)
        
        return cls.from_jch_in_viewing_conditions(j, c, h, viewing_conditions)
    
    def to_int(self) -> int:
        """
        Converts this color to ARGB format.

        Returns:
            ARGB representation of color, assuming the color was viewed in default
            viewing conditions, which are near-identical to the default viewing
            conditions for sRGB.
        """
        return self.viewed(ViewingConditions.DEFAULT)
    
    def viewed(self, viewing_conditions: ViewingConditions) -> int:
        """
        Converts this color to ARGB format.

        Args:
            viewing_conditions: Information about the environment where the color
                will be viewed.

        Returns:
            ARGB representation of color
        """
        alpha = 0.0 if self.chroma == 0.0 or self.j == 0.0 else \
            self.chroma / math.sqrt(self.j / 100.0)
        
        t = math.pow(
            alpha / math.pow(1.64 - math.pow(0.29, viewing_conditions.n), 0.73),
            1.0 / 0.9)
            
        h_rad = (self.hue * math.pi) / 180.0
        
        e_hue = 0.25 * (math.cos(h_rad + 2.0) + 3.8)
        
        ac = viewing_conditions.aw * \
            math.pow(
                self.j / 100.0, 1.0 / viewing_conditions.c / viewing_conditions.z)
                
        p1 = e_hue * (50000.0 / 13.0) * viewing_conditions.nc * viewing_conditions.ncb
        
        p2 = ac / viewing_conditions.nbb
        
        h_sin = math.sin(h_rad)
        h_cos = math.cos(h_rad)
        
        gamma = (23.0 * (p2 + 0.305) * t) / \
            (23.0 * p1 + 11.0 * t * h_cos + 108.0 * t * h_sin)
            
        a = gamma * h_cos
        b = gamma * h_sin
        
        r_a = (460.0 * p2 + 451.0 * a + 288.0 * b) / 1403.0
        g_a = (460.0 * p2 - 891.0 * a - 261.0 * b) / 1403.0
        b_a = (460.0 * p2 - 220.0 * a - 6300.0 * b) / 1403.0
        
        r_c_base = max(0, (27.13 * abs(r_a)) / (400.0 - abs(r_a)))
        r_c = math_utils.signum(r_a) * (100.0 / viewing_conditions.fl) * \
            math.pow(r_c_base, 1.0 / 0.42)
            
        g_c_base = max(0, (27.13 * abs(g_a)) / (400.0 - abs(g_a)))
        g_c = math_utils.signum(g_a) * (100.0 / viewing_conditions.fl) * \
            math.pow(g_c_base, 1.0 / 0.42)
            
        b_c_base = max(0, (27.13 * abs(b_a)) / (400.0 - abs(b_a)))
        b_c = math_utils.signum(b_a) * (100.0 / viewing_conditions.fl) * \
            math.pow(b_c_base, 1.0 / 0.42)
            
        r_f = r_c / viewing_conditions.rgb_d[0]
        g_f = g_c / viewing_conditions.rgb_d[1]
        b_f = b_c / viewing_conditions.rgb_d[2]
        
        x = 1.86206786 * r_f - 1.01125463 * g_f + 0.14918677 * b_f
        y = 0.38752654 * r_f + 0.62144744 * g_f - 0.00897398 * b_f
        z = -0.01584150 * r_f - 0.03412294 * g_f + 1.04996444 * b_f
        
        argb = color_utils.argb_from_xyz(x, y, z)
        return argb
    
    @classmethod
    def from_xyz_in_viewing_conditions(
        cls,
        x: float,
        y: float,
        z: float,
        viewing_conditions: ViewingConditions
    ) -> 'Cam16':
        """
        Creates a CAM16 color from XYZ coordinates in the given viewing conditions.

        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate
            viewing_conditions: Information about the environment where the color
                was observed.

        Returns:
            CAM16 color
        """
        # Transform XYZ to 'cone'/'rgb' responses
        r_c = 0.401288 * x + 0.650173 * y - 0.051461 * z
        g_c = -0.250268 * x + 1.204414 * y + 0.045854 * z
        b_c = -0.002079 * x + 0.048952 * y + 0.953127 * z
        
        # Discount illuminant
        r_d = viewing_conditions.rgb_d[0] * r_c
        g_d = viewing_conditions.rgb_d[1] * g_c
        b_d = viewing_conditions.rgb_d[2] * b_c
        
        # Chromatic adaptation
        r_af = math.pow(viewing_conditions.fl * abs(r_d) / 100.0, 0.42)
        g_af = math.pow(viewing_conditions.fl * abs(g_d) / 100.0, 0.42)
        b_af = math.pow(viewing_conditions.fl * abs(b_d) / 100.0, 0.42)
        
        r_a = math_utils.signum(r_d) * 400.0 * r_af / (r_af + 27.13)
        g_a = math_utils.signum(g_d) * 400.0 * g_af / (g_af + 27.13)
        b_a = math_utils.signum(b_d) * 400.0 * b_af / (b_af + 27.13)
        
        # redness-greenness
        a = (11.0 * r_a + -12.0 * g_a + b_a) / 11.0
        # yellowness-blueness
        b = (r_a + g_a - 2.0 * b_a) / 9.0
        
        # auxiliary components
        u = (20.0 * r_a + 20.0 * g_a + 21.0 * b_a) / 20.0
        p2 = (40.0 * r_a + 20.0 * g_a + b_a) / 20.0
        
        # hue
        atan2 = math.atan2(b, a)
        atan_degrees = atan2 * 180.0 / math.pi
        
        hue = atan_degrees if atan_degrees >= 0 else atan_degrees + 360.0
        hue = hue if hue < 360 else hue - 360.0
        
        hue_radians = hue * math.pi / 180.0
        
        # achromatic response to color
        ac = p2 * viewing_conditions.nbb
        
        # CAM16 lightness and brightness
        J = 100.0 * \
            math.pow(
                ac / viewing_conditions.aw,
                viewing_conditions.c * viewing_conditions.z)
                
        Q = (4.0 / viewing_conditions.c) * math.sqrt(J / 100.0) * \
            (viewing_conditions.aw + 4.0) * (viewing_conditions.fl_root)
            
        hue_prime = hue + 360.0 if hue < 20.14 else hue
        
        e_hue = (1.0 / 4.0) * (math.cos(hue_prime * math.pi / 180.0 + 2.0) + 3.8)
        
        p1 = 50000.0 / 13.0 * e_hue * viewing_conditions.nc * viewing_conditions.ncb
        
        t = p1 * math.sqrt(a * a + b * b) / (u + 0.305)
        
        alpha = math.pow(t, 0.9) * \
            math.pow(1.64 - math.pow(0.29, viewing_conditions.n), 0.73)
            
        # CAM16 chroma, colorfulness, saturation
        C = alpha * math.sqrt(J / 100.0)
        
        M = C * viewing_conditions.fl_root
        
        s = 50.0 * \
            math.sqrt((alpha * viewing_conditions.c) / (viewing_conditions.aw + 4.0))
            
        # CAM16-UCS components
        jstar = (1.0 + 100.0 * 0.007) * J / (1.0 + 0.007 * J)
        mstar = math.log(1.0 + 0.0228 * M) / 0.0228
        astar = mstar * math.cos(hue_radians)
        bstar = mstar * math.sin(hue_radians)
        
        return cls(hue, C, J, Q, M, s, jstar, astar, bstar)
    
    def xyz_in_viewing_conditions(self, viewing_conditions: ViewingConditions) -> list[float]:
        """
        Converts a CAM16 color to XYZ coordinates in the given viewing conditions.

        Args:
            viewing_conditions: Information about the environment where the color
                will be viewed.

        Returns:
            XYZ coordinates
        """
        alpha = 0.0 if self.chroma == 0.0 or self.j == 0.0 else \
            self.chroma / math.sqrt(self.j / 100.0)
        
        t = math.pow(
            alpha / math.pow(1.64 - math.pow(0.29, viewing_conditions.n), 0.73),
            1.0 / 0.9)
            
        h_rad = self.hue * math.pi / 180.0
        
        e_hue = 0.25 * (math.cos(h_rad + 2.0) + 3.8)
        
        ac = viewing_conditions.aw * \
            math.pow(
                self.j / 100.0, 1.0 / viewing_conditions.c / viewing_conditions.z)
                
        p1 = e_hue * (50000.0 / 13.0) * viewing_conditions.nc * viewing_conditions.ncb
        
        p2 = (ac / viewing_conditions.nbb)
        
        h_sin = math.sin(h_rad)
        h_cos = math.cos(h_rad)
        
        gamma = 23.0 * (p2 + 0.305) * t / \
            (23.0 * p1 + 11 * t * h_cos + 108.0 * t * h_sin)
            
        a = gamma * h_cos
        b = gamma * h_sin
        
        r_a = (460.0 * p2 + 451.0 * a + 288.0 * b) / 1403.0
        g_a = (460.0 * p2 - 891.0 * a - 261.0 * b) / 1403.0
        b_a = (460.0 * p2 - 220.0 * a - 6300.0 * b) / 1403.0
        
        r_c_base = max(0, (27.13 * abs(r_a)) / (400.0 - abs(r_a)))
        r_c = math_utils.signum(r_a) * (100.0 / viewing_conditions.fl) * \
            math.pow(r_c_base, 1.0 / 0.42)
            
        g_c_base = max(0, (27.13 * abs(g_a)) / (400.0 - abs(g_a)))
        g_c = math_utils.signum(g_a) * (100.0 / viewing_conditions.fl) * \
            math.pow(g_c_base, 1.0 / 0.42)
            
        b_c_base = max(0, (27.13 * abs(b_a)) / (400.0 - abs(b_a)))
        b_c = math_utils.signum(b_a) * (100.0 / viewing_conditions.fl) * \
            math.pow(b_c_base, 1.0 / 0.42)
            
        r_f = r_c / viewing_conditions.rgb_d[0]
        g_f = g_c / viewing_conditions.rgb_d[1]
        b_f = b_c / viewing_conditions.rgb_d[2]
        
        x = 1.86206786 * r_f - 1.01125463 * g_f + 0.14918677 * b_f
        y = 0.38752654 * r_f + 0.62144744 * g_f - 0.00897398 * b_f
        z = -0.01584150 * r_f - 0.03412294 * g_f + 1.04996444 * b_f
        
        return [x, y, z]