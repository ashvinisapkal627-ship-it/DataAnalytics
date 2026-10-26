import pandas as pd

df = pd.DataFrame({
        "flo_name": ["rose","lilies","sunflower","marrygold"],
        "flo_color": ["red","yellow","yellow","orange"],
        "flo_season": ["rainy","winter","winter","rainy"],
        "flo_ratio": [8.5, 4.5, 6.5, 8.9]
})

print ("original data:\n", df)

#data subsetting
print ("\nsubset (flo_ratio > 5.5): \n", df[df["flo_ratio"] > 5.5])

#sorting in ascending order
print("\nsorted by flo_name (ascending):\n")
print(df.sort_values("flo_name"))

#sorting in decending order
print("\nsorted by flo_name(decending):\n")
print(df.sort_values("flo_name", ascending=False))

#grouping
print("\ngrouped (average flo_ratio by flo_season):\n")
print(df.groupby("flo_season")["flo_ratio"].mean())

#statistical operation
print("mean:", df["flo_ratio"].mean())
print("median:", df["flo_ratio"].median())
print("mode:", df["flo_ratio"].mode())
print("min:", df["flo_ratio"].min())