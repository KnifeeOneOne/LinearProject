from math import sqrt, acos, pi
from decimal import Decimal, getcontext
getcontext().prec = 30

class Vector(object):
    
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates
    
    def plus(self, other):
        return Vector([x+y for x,y in zip(self.coordinates, other.coordinates)])
    
    def minus(self, other):
        return Vector([x-y for x,y in zip(self.coordinates, other.coordinates)])
    
    def times_scalar(self, scalar):
        return Vector([Decimal(scalar)*x for x in self.coordinates])
    
    def magnitude(self):
        return sqrt(sum([x**2 for x in self.coordinates]))
    
    def normalized(self):
        try:
            return self.times_scalar(Decimal('1.0')/self.magnitude())
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)
            
            
    def dot(self, other):
        return sum([x*y for x,y in zip(self.coordinates, other.coordinates)])
    
    def angle_with(self, other, in_degrees=False):
        try:
            i1=self.normalized()
            i2=other.normalized()
#            cos_theta = max(i1*i2,-1)
#            cos_theta = min(cos_theta, 1)
            
            angle_in_radians = acos(i1.dot(i2)) # the result maybe >1 or < -1, round it
            if in_degrees:
                return 180./pi*angle_in_radians
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e
                
    def is_zero(self, tolerance = 1e-10):
        return self.magnitude()<tolerance
                
    def is_parallel_to(self, x):
        return (self.is_zero() or 
                x.is_zero() or 
                self.angle_with(x)==0 or 
                self.angle_with(x)==pi )
                
    
    def is_orthogonal_to(self, x, tolerance = 1e-10):
        return abs(self.dot(x) )< tolerance
    
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
                
    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e
                
    def cross(self, v):
        try:
            x_1, y_1, z_1 =self.coordinates
            x_2, y_2, z_2 = v.coordinates
            new_coordinates = [ y_1*z_2 - y_2*z_1,
                               x_2*z_1 - x_1*z_2,
                               x_1*y_2 - x_2*y_1]
            return Vector(new_coordinates)
        
        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))  
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif (msg == 'too many value to unpack' or 
                  msg == 'need more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e
    def area_of_triangle_with(self, v):
        return self.area_of_parallelogram_with(v)/ Decimal('2.0')
    
    def area_of_parallelogram_with(self, v):
        cross_product = self.cross(v)
        return cross_product.magnitude()
    
#print( Vector([3.039,1.879]).proj_in(Vector([0.825,2.036])))   
#print( Vector([-9.88,-3.264,-8.159]) - Vector([-9.88,-3.264,-8.159]).proj_in(Vector([-2.155,-9.353,-9.473])))
#
#print( Vector([3.009,-6.172,3.692,-2.51]) - Vector([3.009,-6.172,3.692,-2.51]).proj_in(Vector([6.404,-9.144,2.759,8.718])))    
    

#print( Vector([-7.579, -7.88]).is_parallel_to(Vector([-7.578,-7.88]))    )
#print( Vector([-7.579, -7.88]).normalized() * Vector([22.737,23.64]).normalized())
