import pandas as pd 

df = pd.read_csv("fake_output/single_quote.csv")

print(df.iloc[22].values)