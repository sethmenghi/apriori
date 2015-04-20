import pandas as pd
import numpy as np
from itertools import combinations

#
#	Due April 24 
#

# Overview of Apriori
# Bottom-up approach
#	Frequent item-sets are extended one step at a time


def load_tables():
	"""Loads tables into pandas.DataFrame with the product names as the header."""
	products = pd.read_csv('data/products', header=None)
	products.columns = ['products', 'price']
	df = pd.read_csv('data/small_basket.dat', header=None)
	#transaction_ids = df[0].copy()
	del df[0]
	df.columns = products['products']
	return df, products

def load_test():
	"""Loads tables into pandas.DataFrame with the product names as the header."""
	products = pd.read_csv('data/products', header=None)
	products.columns = ['products', 'price']
	df = pd.read_csv('data/test_basket.dat', header=None)
	del df[0]
	#transaction_ids = df[0].copy()
	df.columns = products['products']
	# for i,n in zip(products['products'], range(0,75)):
	# 	del df[i]
	# 	if n == 74:
	# 		break
	return df, products


def support(df, minimum_support):
	# Go through each columns
	support_df = pd.DataFrame(columns=["itemset", "count"])
	transactions = len(df)
	products = df.columns
	min_count = minimum_support * transactions
	itemsets = pd.Series([], index=['itemset'])
	# Delete all sets that don't reach minimum support
	for col in df:
		support = df[col].sum()
		if support <= (minimum_support * transactions):
			del df[col]

	# Create itemsets up to len(product) long
	for i in range(0, len(products)):
		# Combinations that are i+1 long
		for cols in combinations(df, i+1):
			support = df[list(cols)].all(axis=1)
			# Create pattern of names
			if support >= min_count:
				itemset = ",".join(cols)
				itemsets = itemsets.append(itemset)
				support_df.append(pd.Series([itemset, support], ['itemset', 'count']), ignore_index=True)

		print("Itemset Length: %d\t %.2f\r" % (i, len(products)))

	#support_df = pd.DataFrame(itemsets, columns=["itemset", "count"])
	support_df = support_df[support_df.support >= (minimum_support * transactions)]
	return support_df


def apriori():
	df, products = load_tables()
	support_df = support(df, .05)


def test():
	try:
		df, products = load_test()
		df = init_drop_low_support(df, .025)
		print(df)
	except KeyBoardInterrupt:
		del df

if __name__ == '__main__':
	#apriori()
	test()