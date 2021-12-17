import re
import sys
import textwrap

from pathlib import Path


"""
To Use:

Start up the `wikidpad` env
- In CMD navigate to `C:/Users/natdm/Documents/Programming/venvs/wikidpad/Scripts`
- call `activate` to start the venv
- navigate to `C:/Users/natdm/Documents/Programming/tsv-to-wikidpad`
- run `python convert_tsv <path to file> (to_wiki|from_wiki) <wrap width (default is 15)>`
"""


def tsv_to_wikidpad(file, wrap):
	lines = file.readlines()

	output = "<<|t\n"
	for line in lines:
		line = line.strip('\n')
		cells = line.split('\t')
		for idx, cell in enumerate(cells):
			cell = "<br>".join(textwrap.wrap(cell, width=wrap))

			if not cell:
				cell = " "

			cells[idx] = cell

		output += "\t" + "\t".join(cells) + "\n"

	output += ">>\n"

	return output


def wikidpad_to_tsv(file):
	lines = file.readlines()

	output = ""
	for line in lines:
		if "<<|t" in line or ">>" in line:
			continue

		line = line.lstrip('\t')
		cells = line.split('\t')
		for idx, cell in enumerate(cells):
			cell = cell.replace("<br>", " ")
			cell = cell.strip()

			cells[idx] = cell

		output += "\t".join(cells) + "\n"

	return output


if __name__ == "__main__":
	input_path = Path(sys.argv[1])

	mode = "to_wiki"
	if len(sys.argv) > 2:
		mode = sys.argv[2]

	wrap = 15
	if len(sys.argv) > 3:
		wrap = int(sys.argv[3])

	output = ""
	ext = "txt"

	with input_path.open() as f:
		if mode == 'from_wiki':
			output = wikidpad_to_tsv(f)
			ext = "tsv"
		else:
			output = tsv_to_wikidpad(f, wrap)

	output_path = input_path.parent / "output.{}".format(ext)
	output_path.write_text(output)

	print("Output written to {}".format(output_path))
