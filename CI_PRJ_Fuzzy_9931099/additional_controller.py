class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class FuzzyGasController:
    """
    # emtiazi todo
    write all the fuzzify,inference,defuzzify method in this class
    """

    def __init__(self):
        pass

    def equation(self, point1, point2, x):
        gd = float(point2.y - point1.y) / float(point2.x - point1.x)
        return gd * (x - point1.x) + point1.y

    def eq_close_dist(self, x):
        if 0 <= x < 50:
            point1 = Point(0, 1)
            point2 = Point(50, 0)
            return self.equation(point1, point2, x)
        return 0

    def eq_moderate_dist(self, x):
        if 40 <= x < 50:
            point1 = Point(40, 0)
            point2 = Point(50, 1)
            return self.equation(point1, point2, x)
        elif 50 <= x < 100:
            point1 = Point(50, 1)
            point2 = Point(100, 0)
            return self.equation(point1, point2, x)
        return 0

    def eq_far_dist(self, x):
        if 90 <= x < 200:
            point1 = Point(90, 0)
            point2 = Point(200, 1)
            return self.equation(point1, point2, x)
        if x >= 200:
            return 1
        return 0

    def eq_low_gas(self, x):
        if 0 <= x < 5:
            point1 = Point(0, 0)
            point2 = Point(5, 1)
            return self.equation(point1, point2, x)
        elif 5 <= x < 10:
            point1 = Point(5, 1)
            point2 = Point(10, 0)
            return self.equation(point1, point2, x)
        return 0

    def eq_medium_gas(self, x):
        if 0 <= x <= 15:
            point1 = Point(0, 0)
            point2 = Point(15, 1)
            return self.equation(point1, point2, x)
        elif 15 < x <= 30:
            point1 = Point(15, 1)
            point2 = Point(30, 0)
            return self.equation(point1, point2, x)
        return 0

    def eq_high_gas(self, x):
        if 25 <= x < 30:
            point1 = Point(25, 0)
            point2 = Point(30, 1)
            return self.equation(point1, point2, x)
        elif 30 <= x < 90:
            point1 = Point(30, 1)
            point2 = Point(90, 0)
            return self.equation(point1, point2, x)
        return 0

    def linespace(self, start, stop, count):
        delta = (stop - start) / count
        evenly_spaced = [start + i * delta for i in range(count + 1)]
        return evenly_spaced, delta

    def decide(self, center_dist):
        """
        main method for doin all the phases and returning the final answer for gas
        """

        low_membership = self.eq_close_dist(center_dist)
        high_membership = self.eq_far_dist(center_dist)
        medium_membership = self.eq_moderate_dist(center_dist)

        def max_gas_val(x):
            L = min(low_membership, self.eq_low_gas(x))
            H = min(high_membership, self.eq_high_gas(x))
            M = min(medium_membership, self.eq_medium_gas(x))
            return max(L, H, M)

        numerator = 0.0
        denominator = 0.0
        lineSpace = self.linespace(0, 90, 900)
        delta = lineSpace[1]
        for i in lineSpace[0]:
            U = max_gas_val(i)
            numerator += U * i * delta
            denominator += U * delta
        if denominator != 0:
            return 1.0 * float(numerator) / float(denominator)
        return 0


