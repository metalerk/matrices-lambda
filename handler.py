import json
import pandas as pd

def get_line_number(path):
	with open('matrices.csv', 'r') as f:
		f.__next__()
		f.__next__()
		c = 2
		for line in f.readlines():
			c += 1
			if not line[0].isdigit():
				return c - 2
	return 0

# def main(event, context):
def main():
	dimension = get_line_number('matrices.csv')
	matrix = pd.read_csv('matrices.csv')
	initial_pos = 0
	dimension_aux = dimension
	list_df = list()
	while(initial_pos < matrix.shape[0]):
		# print(pd.DataFrame(matrix.iloc[initial_pos: dimension_aux].mean()))
		list_df.append(matrix.iloc[initial_pos: dimension_aux].mean())
		initial_pos += dimension
		dimension_aux += dimension

	return {}

main()