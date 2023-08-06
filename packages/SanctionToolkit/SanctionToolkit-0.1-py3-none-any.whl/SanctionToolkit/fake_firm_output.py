import pandas as pd 
import csv
import random
import numpy as np

np.random.seed(1234)
random.seed(1234)

expected_cols = ["FRN-like","ID","Name","Matched Name","Match List","Score","Date"]

df = pd.read_csv("output/synthetic_sanction_data_alldepths.txt", sep="\t", encoding="utf-8")

use = df.sample(frac=0.9)

out_dict = {}

out_dict["FRN-like"] = [58008 for _ in range(len(use))]
out_dict["ID"] = use["encr_id"]
out_dict["Name"] = use["Fullname"]
out_dict["Matched Name"] = use["Original"]
out_dict["Match List"] = [random.choice(["HMT List", "EU List", "OFAC List"]) for _ in range(len(use))]
out_dict["Score"] = [random.randint(0,5)+95 for _ in range(len(use))]
out_dict["Date"] = ["20220428" for _ in range(len(use))]

out = pd.DataFrame(out_dict)
out = out[expected_cols].reset_index(drop=True)
print(out[["Name", "Matched Name"]])
#standard
out.to_csv("fake_output/almost_all.csv", index=False)

#define changes
def quote_change_single(df):
    df.to_csv("fake_output/single_quote.csv", quotechar="'", quoting=csv.QUOTE_ALL, index=False)


#run changes
quote_change_single(out)
