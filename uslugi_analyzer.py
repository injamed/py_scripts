# -*- coding: utf-8 -*-

import re
import os

import codecs
import sys
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

FILE_PATTERN = re.compile(r'uslugi_all_count_(\d{4})(\d{2})(\d{2})\.txt')

AGGREGATED_DICT = {}

def day_analyzer(filename):
    day_dict = {}
    with open(filename,'r') as f:
        contents = f.readlines()
    for ln in contents:
        ln = ln.rstrip()
        count, categories = ln.split('\t')
        category = re.split('(?<= \d), ', categories)
        for cat in category:
            sub_category = cat[:-2].decode('utf-8')
            meta_category = cat[-1]
            if sub_category not in day_dict:
                day_dict[sub_category] = int(count)
            else:
                day_dict[sub_category] += int(count)

            if meta_category not in day_dict:
                day_dict[meta_category] = int(count)
            else:
                day_dict[meta_category] += int(count)
    return day_dict

for f in os.listdir('./'):
    match = re.match(FILE_PATTERN, f)
    if match:
        file_year = match.group(1)
        file_month = match.group(2)
        file_day = match.group(3)

        if (file_year + file_month) not in AGGREGATED_DICT:
            AGGREGATED_DICT[file_year + file_month] = {}

        AGGREGATED_DICT[file_year + file_month][file_day] = day_analyzer(f)
        #print f, file_year, file_month, file_day

print AGGREGATED_DICT.values()

for month, month_dict in AGGREGATED_DICT.iteritems():
    category_columns = set()
    for day_dict in month_dict.values():
       for category in day_dict.keys():
           category_columns.add(category)
    category_columns = list(category_columns)
    with codecs.open(month + '.txt', 'w', encoding='utf-8') as resulted_file:
        resulted_file.write(';'+';'.join(category_columns) + os.linesep)
        for day, day_dict in month_dict.iteritems():
            resulted_file.write(day + ';' + ';'.join([str(day_dict.get(c, '')) for c in category_columns]) + os.linesep)



