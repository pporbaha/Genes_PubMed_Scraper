import pandas as pd
import numpy as np
import os

path = 'genes intersection data'
os.chdir(path)

# %%
disgen = pd.read_excel('Alzheimer genes.xlsx')
disgen = disgen.loc[:, 'Gene']

df = pd.read_excel('parkinson genes.xlsx')
df = df.loc[:, 'Gene']

print(f'{len(disgen)=}, {len(df)=}\n')
# =>> len(disgen)=1236, len(df)=1060

intersect = np.intersect1d(disgen, df)
union = np.union1d(disgen, df)
disgen_only = np.setdiff1d(disgen, df)
df_only = np.setdiff1d(df, disgen)


def shape_df_build():
    shape = []
    shape.append(['Parkinson', len(df)])
    shape.append(['Alzheimer', len(disgen)])
    shape.append(['', np.nan])
    shape.append(['intersect', len(intersect)])
    shape.append(['union', len(union)])
    shape.append(['Alzheimer_only', len(disgen_only)])
    shape.append(['Parkinson_only', len(df_only)])

    shape = pd.DataFrame(shape, columns=['type', 'count'])
    return shape


shape = shape_df_build()


def write_excel(arr, sheet_name, f):
    series = pd.Series(arr)
    series.to_excel(f, sheet_name=sheet_name, index=False, header=False)
# %%


with pd.ExcelWriter('genes intersection_Alz Parkinson.xlsx',
                    engine='xlsxwriter') as f:
    
    shape.to_excel(f, sheet_name='summary', index=False)
    df.to_excel(f, sheet_name='Parkinson data', index=False, header=False)
    disgen.to_excel(f, sheet_name='Alzheimer data', index=False, header=False)
    write_excel(intersect, 'intersection', f)
    write_excel(union, 'union', f)
    write_excel(disgen_only, 'Alzheimer_only', f)
    write_excel(df_only, 'Parkinson_only', f)
