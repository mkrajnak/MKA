#!/bin/python


import argparse
import sys
import re

class automata:
    buffer = ''
    buffer_index = -1
    roundbrackets = 0
    curlybracket = 0
    commas = 0
    state = 0

    ka_states = []
    ka_alphabet = []
    ka_rules = {}
    ka_start = ''
    ka_end = []

    def get_list(self):

        self.state += 1
        state = ''
        l = []
        for char in get_char(self):
            if char == '\'' or char.isspace():
                pass
            elif char == ',':
                l.append(state)
                state = ''
            elif char == '}':
                l.append(state)
                state = ''
                return l
            else:
                state += char


    def get_dict(self):
        self.state += 1
        counter = 0
        l = ['','','','']
        d = {}
        for char in get_char(self):
            if char.isspace() or char == '\n':
                pass
            elif char == '}':
                break
            elif counter == 0:
                if char == '\'':
                    counter += 1
                    l[counter] += char
                else:
                    l[counter] += char

            elif counter == 1:
                if char == '\'':
                    l[counter] += char
                    counter += 1
                else:
                    l[counter] += char

            elif counter == 2:
                if char == '-':
                    l[counter] += char
                elif char == '>':
                    l[counter] += char
                    counter += 1
                else:
                    print('ERRR')

            elif counter == 3:
                if char == ',':
                    if l[0] not in d.keys():
                        d[l[0]] = {l[1] : l[3]}
                    else:
                        d[l[0]].update({l[1] : l[3]})
                    l = ['','','','']
                    counter = 0
                else:
                    l[counter] += char
        return d

'''
@brief will erase comments from input
@return string without comments
'''
def get_rid_of_comments(ka):
    regex = re.compile('(#.*)$',re.MULTILINE)
    return re.sub(regex, '',mka.buffer)

def get_char(ka):
    while(mka.buffer_index < len(mka.buffer) -1):
        mka.buffer_index += 1
        yield mka.buffer[mka.buffer_index]




parser = argparse.ArgumentParser()
parser.add_argument('--input', nargs=1, help='insert corrent input file name')
parser.add_argument('--output', nargs=1, help='insert corrent output file name')
parser.add_argument('-f','--find-non-finishing', help='finding nonfinishing state of MKA', action='store_true')
parser.add_argument('-m','--minimize', help='will make minimalization of automata', action='store_true')
parser.add_argument('-i','--case-insensitive', help='will properly convert the case of letters', action='store_true')

args = parser.parse_args()
#print(args)

mka = automata();

if args.input != None:
    try:
        f = open(args.input[0], 'r')
    except:
        print('Cannot open file', args.input)
    else:
        mka.buffer = f.read()
        f.close()
mka.buffer = get_rid_of_comments(mka)
print(mka.buffer)

for char in get_char(mka):
    print(char)
    if char.isspace():
        pass
    if char == '{':
        if mka.state == 0:
            mka.ka_states = mka.get_list()
        elif mka.state == 1:
            mka.ka_alphabet = mka.get_list()
        elif mka.state == 2:
            mka.ka_rules = mka.get_dict()
        else:
            break

print('*********')
for s in mka.ka_states:
    print(s)
print('ABC')
for s in mka.ka_alphabet:
    print(s)

for rule in mka.ka_rules:
    print ("%s:" % rule)
    print ("%s:" % mka.ka_rules[rule])

#init_parser()
#for line in sys.stdin:
#    print (line)
