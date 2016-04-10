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

    def get_char(self):
        while(self.buffer_index < len(self.buffer) -1):
            self.buffer_index += 1
            yield self.buffer[self.buffer_index]

    def get_list(self): #goind through part betwee{} char by char and return them
                        #in list
        self.state += 1
        state = ''                          #epmty string
        l = []                              #setup empty list
        for char in self.get_char():
            if char.isspace():  #skip inwanted chars
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
        for char in self.get_char():
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
        for char in self.get_char():
            if char.isspace():               #skip inwanted chars
                pass
            elif char == ',' and string != '':   #end if current token, store it
                self.commas += 1
                return string
            else:
                string += char               #appending


    def parse_automata(self):   #stores automata in data structures

        for char in self.get_char():    #going through text char by char

            if char.isspace() or char =='\n':  #skipping spaces
                pass
            if char == '{':             #go inside every part started wih {
                if self.state == 0:     #and properly store everything
                    self.ka_states = self.get_list()
                elif self.state == 1:
                    self.ka_alphabet = self.get_list()
                elif self.state == 2:
                    self.ka_rules = self.get_dict()
                elif self.state == 4:
                    self.ka_end = self.get_list()
                self.curlybracket += 1
            elif char == ',' and self.state == 3:   # start states in not
                self.commas += 1                    #inside {}
                self.ka_start = self.get_start()
            elif char == ',':
                self.commas += 1                    #counting commas
            elif char == '(' or char == ')':
                self.roundbrackets += 1             # and brackets


    def print_list(self,l):

        sys.stdout.write('{')           #start
        for string in l[:-1]:
            sys.stdout.write(string)    #every element will be written with comma
            sys.stdout.write(',')
        else:
            sys.stdout.write(l[-1])     #last element without comma
        sys.stdout.write('},\n')        #properly end


    def print_dict(self,d):

        sys.stdout.write('{')           #start
        s=0
        for a in d:
            for b in d[a]:
                s += 1;
        c=0
        for a in d:
            for b in d[a]:
                sys.stdout.write('%s ' %a)
                sys.stdout.write('%s -> ' %b)
                c += 1;
                if c != s:
                    sys.stdout.write('%s,\n' %d[a][b])
                else:
                    sys.stdout.write('%s\n' %d[a][b])
        sys.stdout.write('},\n')        #properly end


    def print_automata(self):
        print('(')
        self.print_list(self.ka_states)
        self.print_list(self.ka_alphabet)
        self.print_dict(self.ka_rules)
        print(self.ka_start)            #start state + ,
        sys.stdout.write(',')

        self.print_list(self.ka_end)
        print(')')



def error(message,code):
    sys.stderr.write("ERR:%s\n"%message)
    sys.exit(code)

'''
@brief will erase comments from input
@return string without comments
'''
def get_rid_of_comments(ka):
    regex = re.compile('(#.*)$',re.MULTILINE)
    return re.sub(regex, '',mka.buffer)


def get_input(args):            #reads input from file TODO: stdin
    if args.input != None:
        try:                                #tries to open fiel
            f = open(args.input[0], 'r')
        except:                             #error handling
            print('Cannot open file', args.input)
        else:                               #file opened, get stuff
            buffer = f.read()
            f.close()
            return buffer                   #return inside a string


def args_handler():       #setting properly arg library options

    parser = argparse.ArgumentParser(prog='PROG', description='MKA',add_help=False)
    parser.add_argument('--help', action="help", help='print out this message and exits')
    parser.add_argument('--input', nargs=1, help='insert corrent input file name')
    parser.add_argument('--output', nargs=1, help='insert corrent output file name')
    parser.add_argument('-f','--find-non-finishing', help='finding nonfinishing state of MKA', action='store_true')
    parser.add_argument('-m','--minimize', help='will make minimalization of automata', action='store_true')
    parser.add_argument('-i','--case-insensitive', help='will properly convert the case of letters', action='store_true')
    return parser;


def check_args(args):

    if args.find_non_finishing and args.minimize:
        error("Cannot use this combination of arguments",1)


def debug(mka):
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


'''
MAIN
'''
parser = args_handler()
args = parser.parse_args()
print(args)
check_args(args)

mka = automata();
mka.buffer = get_input(args)
mka.buffer = get_rid_of_comments(mka.buffer)
print(mka.buffer)

mka.parse_automata()
debug(mka)
if not args.find_non_finishing and not args.minimize:
    mka.print_automata()
