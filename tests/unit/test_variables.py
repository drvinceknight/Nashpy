import numpy as np

prisoner_A = np.array([	[3,0],
						[5,1]])
prisoner_B = np.array([	[3,5],
						[0,1]])
prisoner_test_1 = (prisoner_A,prisoner_B,'prisoner_test_1',(np.array([0,1]),np.array([0,1])))


prisoner_degen_B = np.array([	[3,3],
								[1,1]])
prisoner_degen_test_1 = (prisoner_A,prisoner_degen_B,'prisoner_degen_test_1',(np.array([0,1]),np.array([1,0])))

prisoner_B_2 = np.array([	[3,3],
							[2,1]])
prisoner_degen_test_2 = (prisoner_A,prisoner_B_2,'prisoner_degen_test_2',(np.array([0,1]),np.array([1,0])))

bos_A = np.array([	[2,0],
					[0,1]])
bos_B = np.array([	[1,0],
					[0,2]])
bos_test_1 = (bos_A,bos_B,'bos_test_1',(np.array([1,0]),np.array([1,0])))



non_degen_A_1 = np.array([	[0,6],
							[2,5],
							[3,3]])
degen_B_1 = np.array([	[1,0],
						[0,2],
						[4,4]])

non_degen_A_2 = np.array([	[3,3],
							[2,5],
							[0,5]])
non_degen_B_2 = np.array([	[3,2],
							[2,6],
							[3,1]])
degen_B_2 = np.array([	[3,3],
						[2,6],
						[3,1]])
non_degen_test_2 = (non_degen_A_2, non_degen_B_2,'non_degen_test_2',(np.array([1,0,0]),np.array([1,0])))
degen_test_2 = (non_degen_A_2, degen_B_2,'degen_test_2',((np.array([1,0,0]),np.array([1,0]))))

degen_A_3 = np.array([	[1,3,3],
						[3,1,3],
						[1,3,3]])
degen_B_3 = np.array([	[3,3,1],
						[1,1,3],
						[3,1,3]])

degen_test_3 = (degen_A_3, degen_B_3,'degen_test_3',(np.array([0.5,0.5,0]),np.array([0,0,1])))







