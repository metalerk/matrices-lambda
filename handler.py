#!/usr/bin/env python3

import json
import pandas as pd
import argparse

from tabulate import tabulate

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

def main(event, context, **kwargs):
	if event:
		kwargs = event
	dimension = get_line_number(kwargs['file'])
	matrix = pd.read_csv(kwargs['file'])
	initial_pos = 0
	dimension_aux = dimension
	list_df = list()

	while(initial_pos < matrix.shape[0]):
		list_df.append(matrix.iloc[initial_pos: dimension_aux].mean())
		initial_pos += dimension
		dimension_aux += dimension

	dfs = pd.concat(
		[x.to_frame().T for x in list_df]
	).reset_index(drop=True)

	if kwargs['verbose']: print(tabulate(dfs, headers="keys", tablefmt="psql"))

	if kwargs['output']:
		if kwargs['mode'] == 'csv':
			if kwargs['verbose']: print('[+] Escribiendo CSV...')
			dfs.to_csv(kwargs['output'], sep=',')
			if kwargs['verbose']: print('[+] Hecho.')

		elif kwargs['mode'] == 'html':
			if kwargs['verbose']: print('[+] Escribiendo HTML...')
			dfs.to_html(kwargs['output'], escape=True)
			if kwargs['verbose']: print('[+] Hecho.')

	return {}

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Promedio de ancestría por población.')
	parser.add_argument('-f', '--file', type=str, default='matrices.csv', help='Archivo CSV')
	parser.add_argument('-o', '--output', type=str, help='Archivo resultante')
	parser.add_argument('-m', '--mode', type=str, default='csv', help='Archivo HTML resultante')
	parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose')

	args = parser.parse_args()
	main(event={},
		 context={},
		 file=args.file,
		 output=args.output,
		 mode=args.mode,
		 verbose=args.verbose
	)
