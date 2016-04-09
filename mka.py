#!/bin/python


import argparse
import sys

def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', nargs=1, help='insert corrent input file name', type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument('--output', nargs=1, help='insert corrent output file name', type=argparse.FileType('w', encoding='UTF-8'))
    parser.add_argument('-f','--find-non-finishing', help='finding nonfinishing state of MKA', action='store_true')
    parser.add_argument('-m','--minimize', help='will make minimalization of automata', action='store_true')
    parser.add_argument('-i','--case-insensitive', help='will properly convert the case of letters', action='store_true')

    args = parser.parse_args(['--input=lel.txt', '--output=omg.txt', '--minimize'])
    print(args)

init_parser()
sys.exit(0);
