import pandas as pd


df = pd.read_csv(
		"[Input File Path]",
		sep=",",
		header=0,
		index_col=None,
		encoding="utf-8",
		)

print(df.head(10))


df["Date"] = df["Date"].str[:10]

print(df.head(10))

try:
	df.to_csv(
		"[Output File Path]",
		index=False, 
		sep=",",
		encoding="utf-8",
	)
	print("Written")

except Exception as error:
	print(error)
