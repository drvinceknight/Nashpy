from nashpy import *
import time
import numpy as np
from test_variables import *

'''
print('non-degenerate PD:')
print(lemke_howson(prisoner_A,prisoner_B))
print(lemke_howson_lex(prisoner_A,prisoner_B))

print('degen PD:')
print(lemke_howson(prisoner_A,prisoner_degen_B))
print(lemke_howson_lex(prisoner_A,prisoner_degen_B))\
'''

def strategies_match(A,B):
	return np.array_equal(A[0],B[0]) and np.array_equal(A[1],B[1])

def test(A,B,test_name,answer):
	print('+++++++++++++++',test_name,'++++++++++++++++')
	lemke_howson_answer = lemke_howson(A,B)
	lemke_howson_lex_answer = lemke_howson_lex(A,B)
	print('lemke_howson passed: ',strategies_match(lemke_howson_answer,answer))
	print('lemke_howson result: ',lemke_howson_answer)
	print('lemke_howson_lex passed: ',strategies_match(lemke_howson_lex_answer,answer))
	print('lemke_howson_lex result: ',lemke_howson_lex_answer)
	return strategies_match(lemke_howson_lex_answer,answer)
	

#test(*bos_test_1)
#test(*degen_test_3)
#test(*prisoner_test_1)
test(*prisoner_degen_test_1) #problematic fully degenerate test
#test(*prisoner_degen_test_2)
#test(*degen_test_2)
#test(*degen_test_3)