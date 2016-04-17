#!/bin/python

#MKA:xkrajn02
import argparse
import sys
import re
from collections import OrderedDict

class automata:     #class used to store all values needed
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
    ka_end_states = []             #list of end states

    output = sys.stdout

    def get_char(self):
        while(self.buffer_index < len(self.buffer) -1):
            self.buffer_index += 1
            yield self.buffer[self.buffer_index]

    def get_list(self): #goind through part betwee{} char by char and return them
                        #in list
        self.state += 1
        string = ''                          #epmty string
        l = []                              #setup empty list
        for char in self.get_char():
            if char.isspace():  #skip inwanted chars
                pass
            elif char == ',':               #end if current token, store it
                l.append(string)             #and go to next
                string = ''
            elif char == '}':               #end of section
                if string == '':
                    return l
                mka.curlybracket += 1
                l.append(string)            #store token and go back
                string = ''
                return l                    #returns list if tokens found in {}
            else:
                string += char               #appending char to string


    def get_dict(self):
        self.state += 1
        counter = 0                         #counter for goining through one rule
        l = ['','','','']                   #empty list, every rule has 4 strings
        d = OrderedDict()                             #prepare empty dict
        for char in self.get_char():

            if char.isspace() or char == '\n':  #skiping newlines and whitespaces
                pass

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
                    #print('ERRR')

            elif counter == 3:              #final stage
                if char == ',' or char == '}' :
                    mka.curlybracket += 1
                    if l[0] not in d.keys():    #check if key is already in dict
                        d[l[0]] = OrderedDict({l[1] : l[3]}) #if not store another dict inside
                    else:
                        d[l[0]].update({l[1] : l[3]}) #TODO:function
                    if char == '}':
                        break;
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
                if self.state == 0:     #and properly store everything inside
                    self.ka_states = self.get_list()
                elif self.state == 1:
                    self.ka_alphabet = self.get_list()
                elif self.state == 2:
                    self.ka_rules = self.get_dict()
                elif self.state == 4:
                    self.ka_end_states = self.get_list()
                self.curlybracket += 1
            elif char == ',' and self.state == 3:   # start states in not
                self.commas += 1                    #inside {}
                self.ka_start = self.get_start()
            elif char == ',':
                self.commas += 1                    #counting commas
            elif char == '(' or char == ')':
                self.roundbrackets += 1             # and brackets


    def print_list(self,l):

        self.output.write('{')           #start
        for string in l[:-1]:
            self.output.write(string)    #every element will be written with comma
            self.output.write(', ')
        else:
            self.output.write(l[-1])     #last element without comma
        self.output.write('}')        #properly end


    def print_dict(self,d):

        self.output.write('{\n')           #start
        s=0                             #element count - due proper formating
        for a in d:
            for b in d[a]:
                s += 1;
        c=0
        for a in d:
            for b in d[a]:
                self.output.write('%s ' %a)
                self.output.write('%s -> ' %b)
                c += 1;
                if c != s:
                    self.output.write('%s,\n' %d[a][b])
                else:
                    self.output.write('%s\n' %d[a][b])   #lastest element
        self.output.write('},\n')        #properly end


    def print_automata(self):
        self.output.write('(\n')                                 #start
        self.print_list(self.ka_states)            #printing lists
        self.output.write(',\n')
        self.print_list(self.ka_alphabet)
        self.output.write(',\n')
        self.print_dict(self.ka_rules)             #printing dict

        self.output.write(self.ka_start)            #start state + ,
        self.output.write(',\n')

        self.print_list(self.ka_end_states)
        self.output.write('\n)')                                #end


    def check_trap(self):
        for a in self.ka_rules:
            forward_states = []
            for b in self.ka_rules[a]:
                if self.ka_rules[a][b] not in forward_states:
                    forward_states.append(self.ka_rules[a][b])
            if len(forward_states) == 1 and a in forward_states:
                print(a)
        else:
            print(0)


    def check_automata(self):
        if not self.ka_alphabet:        #alphabet is empty
            error('empty alphabet',61)
        if self.ka_start not in self.ka_states: #start state no defined in states
            error('start state is not defined',61)
        #rule consists of undefined state of unknown symbol
        for a in self.ka_rules:
            if a not in self.ka_states:                         #check state
                error('state: %s in rules is not defined'%a,61)
            for b in self.ka_rules[a]:
                if b not in self.ka_alphabet:                   #check symbol
                    error('symbol: %s in rules is not defined'%b,61)
                if self.ka_rules[a][b] not in self.ka_states:
                    error('state: %s in rules is not defined'%self.ka_rules[a][b],61)
        #end states must be defined as states
        for a in self.ka_end_states:
            if a not in self.ka_states:                         #check state
                error('state: %s in rules is not defined'%a,61)


    def write(self, mka):
        if args.output is None:
            self.print_automata()                               #file opened, get stuff
        else:
            try:                                #tries to open fiel
                f = open(args.output[0], 'w')
            except:                             #error handling
                error('Cannot open file:%s'%args.input,3 )
            self.output = f
            self.print_automata()                        #file opened, get stuf
            f.close()


    def same_items(self,l):
        for item in l:
            if item != l[0]:
                return False;
        else: return True;

    def same_group(self, test_members, groups):

        for grp in groups:
            membership = True;
            for member in test_members:
                if not self.is_member(member,grp):
                    membership = False
                    break;
            else:
                return membership


    def is_member(self, member, group):

        if member not in group:
            return False;
        else:
            return True;

    def get_key(self, d, value1, value2):
        for key in d.keys():
            if d[key][value1] == value2:
                return key;

    def get_rules_for_group(self, group):

        d = OrderedDict()
        for member in group:
                d[member] = self.ka_rules[member]
        return d

    def add_rules(self, d, state, symbol, next_state):

        if state not in d.keys():
            d[state] = OrderedDict({symbol:next_state})
        else:
            d[state].update({symbol:next_state})
        return d


    def update_states(self, groups):

        new_states = []
        for group in groups:
            if len(group) == 1:
                new_states.append(group[0])
            else:
                new_states.append("_".join(group))
        return new_states

    def find_merged_state(self,groups,state):

        for group in groups:
            if state in group:
                return "_".join(group)

    def find_merged(self,groups,state):

        for group in groups:
            if state == '_'.join(group):
                return group[0]


    def create_rules(self, groups, states):

        new_rules = OrderedDict() #
        for state in states:
            for symbol in self.ka_alphabet:
                if state not in self.ka_rules.keys():
                    temp_state = self.find_merged(groups,state)
                    next_state = self.ka_rules[temp_state][symbol]
                    if next_state not in states:
                        next_state = self.find_merged_state(groups,next_state)
                    self.add_rules(new_rules, state, symbol,next_state)
                else:
                    next_state = self.ka_rules[state][symbol]
                    if next_state not in states:
                        next_state = self.find_merged_state(groups,next_state)
                    self.add_rules(new_rules, state, symbol,next_state)
        return new_rules


    def minimize(self):

        other_states = []   #initial division of states
        for state in self.ka_states:
            if state not in self.ka_end_states:
                other_states.append(state)

        groups = []         #added divided states in groups
        groups.append(self.ka_end_states) #end states last
        groups.append(other_states)       #other states first

        temp = []   #temporary list of nextstates for certain state and given symbol

        temp_groups = []    #init empty list !!!! very important
        temp_groups = list(groups)
        # for every symbol
        division_counter = 0 # end this when states are not divided in two cycles in a row
        while(True):
            other_states = groups[-1]
            division_flag = False
            for symbol in self.ka_alphabet:
                #go though states that are not in end states
                for grp in groups:
                    # go through every group
                    temp_rules = self.get_rules_for_group(grp) #reload rules

                    for state in grp:   #add next states of group in one list to
                                        #see deviding is needed
                        temp.append(self.ka_rules[state][symbol])
                    if not self.same_group(temp,groups): #divide

                        division_counter = 0
                        grp1 = []
                        grp2 = []
                        for member in temp: #check groups for every memeber
                                            #and correctly divide them in right groups
                            key = self.get_key(temp_rules,symbol,member)
                            del temp_rules[key]
                            if self.is_member(member, other_states):
                                grp1.append(key)#member
                            else:
                                grp2.append(key)

                        temp_groups.remove(other_states)#delete group which was devided
                        if len(grp1) > len(grp2):       # add new groups
                            temp_groups.append(grp2)
                            temp_groups.append(grp1)
                        else:
                            temp_groups.append(grp1)
                            temp_groups.append(grp2)
                        division_flag = True
                    temp = []
                if division_flag:
                    break;  #groups was devided, no need to check another symbol

            if temp_groups == groups: # no change
                division_counter += 1
            if division_counter == 2:
                break;  #no change for two iterations, no further minimalisation
            groups = list(temp_groups) # update list of grups due division changes
        groups.sort()
        for group in groups:
            group.sort()

        #minimized ! handle new automata
        ma = automata() #creating minimized automata
        ma.ka_states = self.update_states(groups)
        ma.ka_rules = self.create_rules(groups,ma.ka_states)
        ma.ka_end_states = self.ka_end_states
        ma.ka_alphabet = self.ka_alphabet
        ma.ka_start = ma.ka_states[0]
        return ma

def error(message,code):
    sys.stderr.write("ERR:%s\n"%message)
    sys.exit(code)


def get_rid_of_comments(ka):
    regex = re.compile('(#.*)$',re.MULTILINE)
    return re.sub(regex, '',mka.buffer)


def get_input(args):            #reads input from file TODO: stdin
    if args.input is not None:
        try:                                #tries to open fiel
            f = open(args.input[0], 'r')
        except:                             #error handling
            error('Cannot open file %s' %args.input)
        else:                               #file opened, get stuff
            buffer = f.read()
            f.close()
            return buffer                   #return inside a string
    else:
        return sys.stdin.read()


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
    for end in mka.ka_end_states:
        print(end)

    print ("CURLY:%d" % mka.curlybracket)
    print ("ROUND:%d" % mka.roundbrackets)
    print ("COMMAS:%d" % mka.commas)


'''
MAIN
'''
parser = args_handler()
args = parser.parse_args()
#print(args)
check_args(args)

mka = automata();
mka.buffer = get_input(args)
mka.buffer = get_rid_of_comments(mka.buffer)
#print(mka.buffer)
if args.case_insensitive:
    mka.buffer = mka.buffer.lower()

mka.parse_automata()

mka.check_automata()
#debug(mka)
if not args.find_non_finishing and not args.minimize:
    mka.write(args)
elif args.find_non_finishing:
    mka.check_trap()
elif args.minimize:
    ma = mka.minimize()
    ma.write(args)
