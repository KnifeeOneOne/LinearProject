# coding:utf-8
# meow

from decimal import Decimal, getcontext
from math import sqrt, acos, pi

getcontext().prec = 30

class Vector(object):
    def __init__(self, coordinates):

        self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'cannot normalize the zero vector'
        self.NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'no unique parallel component'
        self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'only defined in 2 and 3 dimensions'
        
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(map(Decimal, coordinates))
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __iter__(self):
        self.current = -1
        return self

    def next(self):
        self.current += 1
        if self.current >= self.dimension:
            raise StopIteration
        else:
            return self.coordinates[self.current]

    def __getitem__(self, key):
        if key >= self.dimension:
            raise IndexError
        else:
            return self.coordinates[key]

    def area_of_triangle_with(self, v):
        return self.area_of_parallelogram_with(v)/Decimal('2.0')

    def area_of_parallelogram_with(self, v):
        cross_product = self.cross(v)
        return cross_product.magnitude()

    def cross(self, v):
        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            new_coordinates = [y_1*z_2 - y_2*z_1,
                               -(x_1*z_2 - x_2*z_1),
                               x_1*y_2 - x_2*y_1]
            return Vector(new_coordinates)

        except ValueError as e:
            msg = str(e)
            if msg == 'need more than two values to unpack':
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif msg == 'too many values to unpack' or msg == 'need more than 1 value to unpack':
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e

    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)

        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def component_parallel_to(self, basis):
        try:
            u = basis.normalized()
            weight = self.dot(u)
            return u.times_scalar(weight)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    # 判断正交
    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    # 判断平行
    def is_parallel_to(self, v):
        return (self.is_zero() or
                v.is_zero() or
                self.angle_with(v) == 0 or 
                self.angle_with(v) == pi)

    # 点乘
    def dot(self, v):
        return sum([x * y for x, y in zip(self.coordinates, v.coordinates)])

    # 夹角
    def angle_with(self, v, in_degrees=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            d = u1.dot(u2)
            angle_in_radians = acos(d)

            if in_degrees:
                degrees_per_radian = 180. / pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot computer an angel with the zero vector')
            else:
                raise e

    # 向量大小
    def magnitude(self):
        coordinates_squared = [x ** 2 for x in self.coordinates]
        return Decimal.sqrt(sum(coordinates_squared))
    
    # 向量方向
    def normalized(self):
        try:
            magnitude = self.magnitude()
            # return self.times_scalar(Decimal('1.0')/magnitude)
            return self.times_scalar(Decimal('1.0') / Decimal(magnitude))

        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

    # 向量加法
    def plus(self, v):
        new_coordinates = [x + y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    
    # 向量减法
    def minus(self, v):
        new_coordinates = [x - y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    
    # 向量与标量相乘
    def times_scalar(self, c):
        new_coordinates = [Decimal(c) * x for x in self.coordinates]
        # new_coordinates = [c * x for x in self.coordinates]
        return Vector(new_coordinates)

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates


