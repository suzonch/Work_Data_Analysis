import pandas as pd


data1 = pd.read_csv('/home/suzon/Work/LED_tests/short_run/VAOL-5EWY4/led1/0/spec_1556173319.csv', header=None)
df1 = pd.DataFrame(data1)
data2 = pd.read_csv('/home/suzon/Work/LED_tests/short_run/VAOL-5EWY4/led1/0/dark.csv', header=None)
df2 = pd.DataFrame(data2)
df = df1.subtract(df2, fill_value=0)
df[df < 0] = 0
print(df)
df.to_csv(f"/home/suzon/spec_filtered_verify_1556173319.csv",header=False, index=None)