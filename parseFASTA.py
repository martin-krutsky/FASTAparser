#!/usr/bin/env python3

"""parseFASTA.py: Parse FASTA files, print relevant info to console
   and (possibly) aggregate them to an output file.
"""

__author__ = "Martin Krutsky"

import argparse
from typing import Dict


def parse_description(descr_line: str):
    # split the description line into three parts (at most)
    # leaving the description itself together
    descr_ls = descr_line.split(maxsplit=2)

    id = descr_ls[1]  # there is '>' at 0th index
    description = descr_ls[2].strip()
    print(f'ID: {id}\nDescription: {description}')


def parse_fasta_file(filename: str):
    seq_dict = dict()  # storage of sequences; used for writing back the data
    last_desc_line = ''  # contains last seen description; used as key for storing the sequence
    sequence = ''  # accumulator string containing FASTA sequence

    with open(filename, 'r') as fasta_file:
        for line in fasta_file:
            if line[0] == '>':  # the line contains description
                if sequence:
                    # the sequence is non-empty and we are at a new description
                    # --> save the seq., print its length and start a new one
                    print(f'Sequence length: {len(sequence)}\n')
                    seq_dict[last_desc_line] = sequence
                    sequence = ''

                parse_description(line)  # parse and print the new description
                last_desc_line = line
            else:  # sequence line follows - add the string to the sequence
                sequence += line.strip()

        print(f'Sequence length: {len(sequence)}')
        # add the sequence to dict for future write back
        seq_dict[last_desc_line] = sequence

    return seq_dict


def save_to_file(filename: str, wrap: int, seq_dict: Dict[str, str]):
    with open(filename, 'w+') as output_file:
        for desc in seq_dict:
            output_file.write(desc)  # description line already contains newline; simply write it to the file
            sequence = seq_dict[desc]

            # split the sequence so that, except the last one, all lines have exactly
            # 'wrap' nr of characters; write them to output file padded with newlines
            seq_split = [sequence[j:j+wrap] + '\n' for j in range(0, len(sequence), wrap)]
            output_file.writelines(seq_split)


def main(args: argparse.Namespace):
    sequence_dict = dict()  # dict in the form of {description: sequence,...}
    for i, file in enumerate(args.input_files):
        if i != 0:
            print()  # add a newline before next file
        print(f'FILENAME: {file}')
        # merge the new dict with the old one; assuming IDs are unique, otherwise data might be lost
        sequence_dict.update(parse_fasta_file(file))
        # in case of non-unique description lines, data should be stored as a list of tuples

    if args.output:  # if no output specified - args.output is None
        save_to_file(args.output, args.wrap, sequence_dict)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process FASTA files.')
    parser.add_argument("input_files", type=str, nargs='+', help="path to input file(s)")  # positional arguments
    parser.add_argument('--output', type=str, help='path to an output file')  # optional argument
    parser.add_argument('--wrap', type=int, default=80, help='max length of a sequence line')  # optional argument

    args = parser.parse_args()  # parse the args as specified above to a Namespace object
    main(args)
