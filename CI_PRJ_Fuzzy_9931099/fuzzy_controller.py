class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class FuzzyController:
    """
    #todo
    write all the fuzzify,inference,defuzzify method in this class
    """

    def __init__(self):
        pass

    def equation(self, point1, point2, x):
        gd = float(point2.y - point1.y) / float(point2.x - point1.x)
        return gd * (x - point1.x) + point1.y

    # Left distance equations
    def eq_close_L(self, x):
        if 0 <= x < 50:
            return -x / 50 + 1
        return 0

    def eq_far_L(self, x):
        if 50 < x <= 100:
            return x / 50 - 1
        return 0

    def eq_moderate_L(self, x):
        if 35 < x < 50:
            return x / 15 - 7 / 3
        elif 50 <= x < 65:
            return -x / 15 + 13 / 3
        return 0

    # Right distance equations
    def eq_close_R(self, x):
        if 0 <= x < 50:
            return -x / 50 + 1
        return 0

    def eq_far_R(self, x):
        if 50 < x <= 100:
            return x / 50 - 1
        return 0

    def eq_moderate_R(self, x):
        if 35 < x < 50:
            return x / 15 - 7 / 3
        elif 50 <= x < 65:
            return -x / 15 + 13 / 3
        return 0

    # Rotate amount equations

    def eq_high_R(self, x):
        if -50 <= x <= -20:
            return x / 30 + 5 / 3
        elif -20 < x < -5:
            return -x / 15 - 1 / 3
        return 0

    def eq_low_R(self, x):
        if -20 < x < -10:
            point1 = Point(-20, 0)
            point2 = Point(-10, 1)
            return self.equation(point1, point2, x)
        elif -10 <= x < 0:
            point1 = Point(-10, 1)
            point2 = Point(0, 0)
            return self.equation(point1, point2, x)
        return 0

    def eq_nothing(self, x):
        if -10 < x <= 0:
            point1 = Point(-10, 0)
            point2 = Point(0, 1)
            return self.equation(point1, point2, x)
        elif 0 < x < 10:
            point1 = Point(0, 1)
            point2 = Point(10, 0)
            return self.equation(point1, point2, x)
        return 0

    def eq_low_L(self, x):
        if 0 < x <= 10:
            point1 = Point(0, 0)
            point2 = Point(10, 1)
            return self.equation(point1, point2, x)
        elif 10 < x < 20:
            point1 = Point(10, 1)
            point2 = Point(20, 0)
            return self.equation(point1, point2, x)
        return 0

    def eq_high_L(self, x):
        if 5 < x < 20:
            point1 = Point(5, 0)
            point2 = Point(20, 1)
            return self.equation(point1, point2, x)
        elif 20 <= x < 50:
            point1 = Point(20, 1)
            point2 = Point(50, 0)
            return self.equation(point1, point2, x)
        return 0

    def linespace(self, start, stop, count):
        delta = (stop - start) / (count)
        evenly_spaced = [start + i * delta for i in range(count+1)]
        return evenly_spaced, delta

    def decide(self, left_dist, right_dist):
        """
        main method for doin all the phases and returning the final answer for rotation
        """
        low_right_membership = min(self.eq_close_L(left_dist), self.eq_moderate_R(right_dist))
        high_right_membership = min(self.eq_close_L(left_dist), self.eq_far_R(right_dist))
        nothing_membership = min(self.eq_moderate_R(right_dist), self.eq_moderate_L(left_dist))
        low_left_membership = min(self.eq_close_R(right_dist), self.eq_moderate_L(left_dist))
        high_left_membership = min(self.eq_close_R(right_dist), self.eq_far_L(left_dist))

        def max_rotate_val(x):
            LR = min(low_right_membership, self.eq_low_R(x))
            HR = min(high_right_membership, self.eq_high_R(x))
            NTH = min(nothing_membership, self.eq_nothing(x))
            LL = min(low_left_membership, self.eq_low_L(x))
            HL = min(high_left_membership, self.eq_high_L(x))

            return max(LR, HR, NTH, LL, HL)

        numerator = 0.0
        denominator = 0.0
        lineSpace = self.linespace(-50, 50, 1000)
        delta = lineSpace[1]
        for i in lineSpace[0]:
            U = max_rotate_val(i)
            numerator += U * i * delta
            denominator += U * delta
        if denominator != 0:
            return 1.0 * float(numerator) / float(denominator)
        return 0

