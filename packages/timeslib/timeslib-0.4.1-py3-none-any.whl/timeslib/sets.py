# -*- coding: utf-8 -*-
"""
Copyright 2019-2022 Olexandr Balyk

This file is part of Timeslib.

Timeslib is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Timeslib is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Timeslib. If not, see <https://www.gnu.org/licenses/>.
"""

import pandas as pd
import re

# pd needs xlrd


def subset(master_set, name_pattern):
    #
    result = set()
    # wildcard translation between VEDA-BE and re
    subst_dict = {'*': '.*', '?': '.', '_': '.'}
    # substitute wildcards according to the dictionary
    for old, new in subst_dict.items():
        name_pattern = name_pattern.replace(old, new)
    # split comma-separated name patterns
    name_patterns = set(name_pattern.split(","))
    # match name patterns and combine the elements in one set
    for pattern in name_patterns:
        string = re.compile(pattern, re.I)
        for i in master_set:
            if string.match(i) is not None:
                result.add(string.match(i).group())
    return result


def com_filter(c, desc_dict, sets_dict, name_rule, desc_rule, sets,
               andor_cch, andor_sc):
    main_dict = dict()
    if pd.notnull(name_rule): 
        name_specified = True
        main_dict['byname'] = subset(c, name_rule)
    else:
        name_specified = False
    
    if pd.notnull(desc_rule):
        desc_specified = True
        superset = set()
        for k in subset(frozenset(desc_dict), desc_rule):
            for set_member in desc_dict[k]:
                superset.add(set_member)
        main_dict['bydesc'] = superset
    else:
        desc_specified = False
    
    if pd.notnull(sets):
        sets_specified = True
        byset = set()
        for s in set(sets.split(',')):
            byset = byset | sets_dict.get(s, set())
        main_dict['byset'] = byset
    else:
        sets_specified = False
            
    if name_specified and desc_specified:
        if andor_cch != 'OR':
            comb_set = main_dict['byname'] & main_dict['bydesc']
        else:
            comb_set = main_dict['byname'] | main_dict['bydesc']
    elif name_specified and not desc_specified:
        comb_set = main_dict['byname']
    elif not name_specified and desc_specified:
        comb_set = main_dict['bydesc']
    else:
        comb_set = set()
    
    if sets_specified:
        if not name_specified and not desc_specified:
            comb_set = main_dict['byset']
        else:
            if andor_sc != 'OR':
                comb_set = comb_set & main_dict['byset']
            else:
                comb_set = comb_set | main_dict['byset']
    else:
        return comb_set
    return comb_set


def prc_filter(p, desc_dict, in_dict, out_dict, sets_dict, name_rule, desc_rule,
               in_rule, out_rule, sets, andor_pch, andor_sp):
    
    main_dict = dict()
    
    if pd.notnull(name_rule): 
        main_dict['byname'] = subset(p, name_rule)
    
    if pd.notnull(desc_rule):
        superset = set()
        for k in subset(frozenset(desc_dict), desc_rule):
            for set_member in desc_dict[k]:
                superset.add(set_member)
        main_dict['bydesc'] = superset
    if pd.notnull(in_rule):
        superset = set()
        for k in subset(frozenset(in_dict), in_rule):
            for set_member in in_dict[k]:
                superset.add(set_member)
        main_dict['byin'] = superset
    if pd.notnull(out_rule):
        superset = set()
        for k in subset(frozenset(out_dict), out_rule):
            for set_member in out_dict[k]:
                superset.add(set_member)
        main_dict['byout'] = superset
    if pd.notnull(sets):
        byset = set()
        for s in set(sets.split(',')):
            byset = byset | sets_dict.get(s, set())
        main_dict['byset'] = byset
            
    if main_dict != {}:
        specified = list(main_dict.keys())
        if 'byset' in specified:
            if len(specified) > 1:
                specified.remove('byset')
                comb_set = main_dict[specified[0]]
                if andor_pch != 'OR':
                    for i in specified:
                        comb_set = comb_set & main_dict[i]
                else:
                    for i in specified:
                        comb_set = comb_set | main_dict[i]
                if andor_sp != 'OR':
                    return comb_set & main_dict['byset']
                else:
                    return comb_set | main_dict['byset']
            else:
                return main_dict['byset']
        else:
            comb_set = main_dict[specified[0]]
            if andor_pch != 'OR':
                for i in specified:
                    comb_set = comb_set & main_dict[i]
                return comb_set
            else:
                for i in specified:
                    comb_set = comb_set | main_dict[i]
                return comb_set 
    else:
        return set()


def df2dict(df, key_col, val_col):
    my_dict = dict()
    keyset = set(df[key_col].unique().tolist())
    for key in keyset:
        my_dict[key] = set(df[val_col].loc[df[key_col] == key].tolist())
    return my_dict
