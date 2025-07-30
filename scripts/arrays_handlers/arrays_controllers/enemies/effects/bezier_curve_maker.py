from panda3d.core import Vec2


class BezierCurveMaker:
    def __init__(self):
        self.__SAMPLES = 100
        self.__EPSILON = 0.0001
        self.__NUM_POINTS = 30

    @staticmethod
    def __bezier_curve_point(p0:Vec2, p1:Vec2, p2:Vec2, p3:Vec2, t:float)->Vec2:
        """Возвращает точку на кривой Безье для параметра t"""
        return (1-t)**3 * p0 + 3*(1-t)**2*t * p1 + 3*(1-t)*t**2 * p2 + t**3 * p3

    def __calculate_curve_length(self, p0:Vec2, p1:Vec2, p2:Vec2, p3:Vec2, samples:int)->float:
        """Вычисляет приблизительную длину кривой Безье"""
        length = 0.0
        prev_point = self.__bezier_curve_point(p0, p1, p2, p3, 0)

        for i in range(1, samples + 1):
            t = i / samples
            current_point = self.__bezier_curve_point(p0, p1, p2, p3, t)
            length += (current_point - prev_point).length()
            prev_point = current_point

        return length

    def __find_t_for_distance(self, p0:Vec2, p1:Vec2, p2:Vec2, p3:Vec2, target_distance:float)->float:
        """Находит параметр t, соответствующий пройденному расстоянию"""
        low, high = 0.0, 1.0

        while high - low > self.__EPSILON:
            mid = (low + high) / 2
            current_distance = self.__calculate_curve_length(p0, p1, p2, p3, mid * self.__SAMPLES)

            if current_distance < target_distance:
                low = mid
            else:
                high = mid

        return (low + high) / 2

    def generate_uniform_points(self, p0, p1, p2, p3):
        """Генерирует точки для равномерного движения"""
        total_length = self.__calculate_curve_length(p0, p1, p2, p3, self.__SAMPLES)
        segment_length = total_length / (self.__NUM_POINTS - 1)

        points = []
        for i in range(self.__NUM_POINTS):
            target_dist = i * segment_length
            t = self.__find_t_for_distance(p0, p1, p2, p3, target_dist)
            points.append(self.__bezier_curve_point(p0, p1, p2, p3, t))

        return points