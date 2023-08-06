#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2022-05-04
Purpose: Pyperclip CLI
"""

import argparse
import sys



# --------------------------------------------------
def get_args():
	"""Get command-line arguments"""

	parser = argparse.ArgumentParser(
		description='Pyperclip CLI',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('action',
						metavar='ACTION',
						help='copy or paste',
						choices=['copy', 'paste'], default='copy', nargs='?')

	# parser.add_argument('-a',
	#                     '--arg',
	#                     help='A named string argument',
	#                     metavar='str',
	#                     type=str,
	#                     default='')

	# parser.add_argument('-i',
	#                     '--int',
	#                     help='A named integer argument',
	#                     metavar='int',
	#                     type=int,
	#                     default=0)

	parser.add_argument('-f',
						'--file',
						help='Copy the content of the file',
						metavar='FILE',
						type=argparse.FileType('rt'),
						default=sys.stdin, )

	parser.add_argument('-o',
						'--out',
						help='Paste to file',
						metavar='OUT',
						type=argparse.FileType('wt'),
						default=sys.stdout)

	# parser.add_argument('-o',
	#                     '--on',
	#                     help='A boolean flag',
	#                     action='store_true')

	return parser.parse_args()


# --------------------------------------------------
def main():
	"""Make a jazz noise here"""

	args = get_args()
	action = args.action
	file = args.file
	out = args.out
	import pyperclip
	# if file:
	# 	pyperclip.copy(file.read())
	# 	return

	match action:
		case 'copy':
			pyperclip.copy(file.read())
		case 'paste':
			out.write(pyperclip.paste())
		case _:
			raise ValueError('Unknown action: {}'.format(action))




# --------------------------------------------------
if __name__ == '__main__':
	main()
