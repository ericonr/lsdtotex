#!/usr/bin/env python3

from sys import argv
from collections import namedtuple
from functools import reduce
from datetime import datetime

file_name = 'Sim1.lsd'
dest = 'Sim1.tex'
if len(argv) > 1:
    file_name = argv[1]
if len(argv) > 2:
    dest = argv[2]

class ParameterPretty:
    def __init__(self, name, tex, braces=None):
        self.pretty_name = name
        self.tex = tex
        self.braces = braces
        self.unused = False

pp = ParameterPretty
pretties = {
        'interest_rate': pp('interest rate', r'i'),
        'depreciation_rate': pp('depreciation rate', r'\delta'),
        ('propensity_consume_income', 'propensity_consume_wealth'): pp('propensities to consume (income and wealth)', r'\alpha_{1,2}', '()'),
        'aha': pp('','')
        }

Parameter = namedtuple('Parameter', 'name value')
final_dict = {}

def print_entry(f, symbol, name, value, key=""):
    f.write(f'\t\t${symbol}$ & {name} & {value} \\\\ % {key}\n')

with open(file_name, 'r') as f:
    read_vars = False
    for line in f.readlines():
        if read_vars:
            if "Param:" in line:
                pieces = line.split()
                entry = Parameter(pieces[1], pieces[-1])
                final_dict[entry.name] = entry
        elif line == 'DATA\n':
            read_vars = True
            print("start reading params")

with open(dest, 'w') as f:
    f.write(f'% tabela gerada em {datetime.now()}\n\n')
    for key in pretties.keys():
        # always 'continue' after using a key!
        if isinstance(key, str) and key in final_dict.keys():
            entry = pretties[key]
            entryv = final_dict[key].value
            print_entry(f, entry.tex, entry.pretty_name, entryv, key);
            continue
        elif isinstance(key, tuple) and len([k for k in key if k in final_dict.keys()]) == len(key):
            entry = pretties[key]
            entry_values = [final_dict[k].value for k in key]
            entryv = reduce(lambda x, y: x + ', ' + y, entry_values)
            if not entry.braces is None:
                entryv = entry.braces[0] + entryv + entry.braces[1]
            keyfmt = reduce(lambda x, y: x + ' ' + y, key)
            print_entry(f, entry.tex, entry.pretty_name, entryv, keyfmt)
            continue
        pretties[key].unused = True

unused_keys = [key for key in pretties.keys() if pretties[key].unused]
if len(unused_keys) > 0:
    print(f'WARNING: ({len(unused_keys)}) unused keys:')
    for key in unused_keys:
        print(f' - {key}')
