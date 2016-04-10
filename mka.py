#!/bin/python


import argparse
import sys
import re

class automata:     #class used to store all values needed to work with automata
    buffer = ''
    buffer_index = -1
    roundbrackets = 0
    curlybracket = 0
    commas = 0
    state = 0

    ka_states = []          #list of finit states
    ka_alphabet = []        #list of aplhabet
    ka_rules = {}           #dictionary inside dictionary of rules
    ka_start = ''           #start state store inside string
    ka_end = []             #list of end states


    def get_list(self): #goind through part betwee{} char by char and return them
                        #in list
        self.state += 1
        state = ''                          #epmty string
        l = []                              #setup empty list
        for char in get_char(self):
            if char == '\'' or char.isspace():  #skip inwanted chars
                pass
            elif char == ',':               #end if current token, store it
                l.append(state)             #and go to next
                state = ''
            elif char == '}':               #end of section
                mka.curlybracket += 1
                l.append(state)             #store token and go back
                state = ''
                return l                    #returns list if tokens found in {}
            else:
                state += char               #appending char to string


    def get_dict(self):
        self.state += 1
        counter = 0                         #counter for goining through one rule
        l = ['','','','']                   #empty list, every rule has 4 strings
        d = {}                              #prepare empty dict
        for char in get_char(self):
            if char.isspace() or char == '\n':  #skiping newlines and whitespaces
                pass
            elif char == '}':                   #rule definition ends here
                mka.curlybracket += 1
                break
            elif counter == 0:              #process first part of rule
                if char == '\'':
                    counter += 1            #increment counter to go to next part
                    l[counter] += char      #append char (' is needed)
                else:
                    l[counter] += char

            elif counter == 1:              #process second part of rule
                if char == '\'':
                    l[counter] += char
                    counter += 1
                else:
                    l[counter] += char

            elif counter == 2:              #process third part of rule
                if char == '-':
                    l[counter] += char
                elif char == '>':
                    l[counter] += char
                    counter += 1
                else:
                    print('ERRR')

            elif counter == 3:              #final stage
                if char == ',':
                    if l[0] not in d.keys():    #check if key is already in dict
                        d[l[0]] = {l[1] : l[3]} #if not store another dict inside
                    else:
                        d[l[0]].update({l[1] : l[3]}) #TODO:function
                    l = ['','','','']
                    counter = 0
                else:
                    l[counter] += char
        return d

    def get_start(self):
        self.state += 1
        string = ''                          #epmty string
        for char in get_char(self):
            if char.isspace():  #skip inwanted chars
                pass
            elif char == ',' and string != '':               #end if current token, store it
                self.commas += 1
                print(char)
                return string
            else:
                string += char               #appending
            print('HERE')
            print(string)

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
        elif mka.state == 4:
            mka.ka_end = mka.get_list()
        mka.curlybracket += 1
    elif char == ',' and mka.state == 3:
        mka.ka_start = mka.get_start()
        mka.commas += 1
    elif char == ',':
        mka.commas += 1
    elif char == '(' or char == ')':
        mka.roundbrackets += 1

print('*********')
for s in mka.ka_states:
    print(s)
print('ABC')
for s in mka.ka_alphabet:
    print(s)
print('RULES')
for rule in mka.ka_rules:
    print ("%s:" % rule)
    print ("%s:" % mka.ka_rules[rule])
print('START')
print(mka.ka_start)
print('END')
for end in mka.ka_end:
    print(end)

print ("CURLY:%d" % mka.curlybracket)
print ("ROUND:%d" % mka.roundbrackets)
print ("COMMAS:%d" % mka.commas)

#init_parser()
#for line in sys.stdin:
#    print (line)
