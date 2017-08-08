import math

class Vector(object):
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates
    
    def __add__(self, other):
        return Vector([x+y for x,y in zip(self.coordinates, other.coordinates)])
    
    def __sub__(self, other):
        return Vector([x-y for x,y in zip(self.coordinates, other.coordinates)])
    
    def times_scalar(self, scalar):
        return Vector([scalar*x for x in self.coordinates])
    
    def magnitude(self):
        return math.sqrt(sum([x**2 for x in self.coordinates]))
    
    def normalized(self):
        try:
            return self.times_scalar(1.0/self.magnitude())
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)
            
    def __mul__(self, other):
        return sum([x*y for x,y in zip(self.coordinates, other.coordinates)])
    
    def angle_with(self, other, in_degrees=False):
        try:
            i1=self.normalized()
            i2=other.normalized()
            cos_theta = max(i1*i2,-1)
            cos_theta = min(cos_theta, 1)
            angle_in_radians = math.acos(cos_theta) # the result maybe >1 or < -1, round it
            if in_degrees:
                return 180./math.pi*angle_in_radians
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e
                
    def is_zero(self, tolerance = 1e-10):
        return self.magnitude()<tolerance
                
    def is_parallel_to(self, x, tolerance = 1e-10):
        return (self.is_zero() or x.is_zero() 
                or abs(self.angle_with(x))<tolerance or abs(self.angle_with(x)-math.pi)<tolerance)
    
    def is_orthogonal_to(self, x, tolerance = 1e-10):
        return abs(self * x) < tolerance
    
    def component_parallel_to(self, basis):
        try:
            u = basis.normalized()
            weight = self * u
            return u.times_scalar(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e
                
    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self - projection
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
                raise e
        
    
    
#print( Vector([3.039,1.879]).proj_in(Vector([0.825,2.036])))   
#print( Vector([-9.88,-3.264,-8.159]) - Vector([-9.88,-3.264,-8.159]).proj_in(Vector([-2.155,-9.353,-9.473])))
#
#print( Vector([3.009,-6.172,3.692,-2.51]) - Vector([3.009,-6.172,3.692,-2.51]).proj_in(Vector([6.404,-9.144,2.759,8.718])))    
    

#print( Vector([-7.579, -7.88]).is_parallel_to(Vector([-7.578,-7.88]))    )
#print( Vector([-7.579, -7.88]).normalized() * Vector([22.737,23.64]).normalized())
