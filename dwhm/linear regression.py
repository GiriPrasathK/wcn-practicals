import pandas as pd
import numpy as np

x = 27

df = pd.DataFrame({
    'X': [5, 7, 12, 16, 20],
    'Y': [40, 120, 180, 210, 240]
})

mean_X = df['X'].mean()

mean_Y = df['Y'].mean()

df['a'] = np.nan

df['b'] = np.nan

df['a*b'] = np.nan

df['a^2'] = np.nan

# a = X - mean_X
for index, row in df.iterrows():
    df.at[index, 'a'] = df.at[index, 'X'] - mean_X


# b =  Y - mean_Y
for index, row in df.iterrows():
    df.at[index, 'b'] = df.at[index, 'Y'] - mean_Y

# a*b
for index, row in df.iterrows():
    df.at[index, 'a*b'] = df.at[index, 'a']*df.at[index, 'b']

# sum of a*b
sum_ab = df['a*b'].sum()

for index, row in df.iterrows():
    df.at[index, 'a^2'] = df.at[index, 'a']*df.at[index, 'a']

# sum of a*a
sum_aa = df['a^2'].sum()

# w1
w1 = sum_ab / sum_aa

# w0
w0 = mean_Y - w1*mean_X

# estimated value of y for x = 27
y = w0 + w1*x

print(f"estimated value of y for x={x} is {y}")






