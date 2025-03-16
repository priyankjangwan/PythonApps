import numpy as np
import pandas as pd


data1 = {'EmpID':['E1','E2','E3','E4'],'Designation':['Team Lead','Developer','Manager','Tester']}
data2 = {'EmpID':['E1','E3'],'Project':['Google','Microsoft'],'Location':['India','USA']}

employee_df = pd.DataFrame(data1)
projects_df = pd.DataFrame(data2)

joins= pd.merge(employee_df,projects_df,how='inner',on='EmpID')
print(joins)