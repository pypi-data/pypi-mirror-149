import numpy as np
import shapey
import numpy as np
import pandas as pd
import pytest
import copy 

x=np.random.random(100)
y=np.random.random(100)

df=pd.DataFrame([x, y]).transpose()
df.columns=['x', 'y']


import math 
import numpy.testing as npt

#these tests have nothing to do with anything 

# inf = float('inf')  # this is a quick-and-easy way to get the "infinity" value 

# def function_a(angle=180):
#     anglerad = math.radians(angle)
#     return math.sin(anglerad/2)/math.sin(anglerad)

# def function_b(value):
#     if value < 0:
#         return value - 1
#     else:
#         value2 = subfunction_b(value + 1)
#         return value + value2
    
# def subfunction_b(inp):
#     vals_to_accum = []
#     for i in range(10):
#         vals_to_accum.append(inp ** (i/10))
#     if vals_to_accum[-1] > 2:
#         vals.append(100)
#     # really you would use numpy to do this kind of number-crunching... but we're doing this for the sake of example right now
#     return sum(vals_to_accum) 

# # know that to not have to worry about this, you should just use `astropy.coordinates`



# def test_function_a():
# 	assert np.isclose(function_a(angle=180),  8165619676597685.0)

# def test_function_b():
# 	assert function_b(-20.0)==-21.0

# def test_function_positive():
# 	with pytest.raises(NameError): 
# 		function_b(20.0)

# #you can also do this with exceptions
# #also check for coverage with codecov


def test_box():
	b1=shapey.Box()
	b1.data=df
	b2=copy.deepcopy(b1)
	b2.rotate(np.pi/2)
	b3=copy.deepcopy(b1)
	assert len(b3.select(df)) < len(df)
	assert len(b1) == len(b2)
	assert b2.angle != b1.angle

