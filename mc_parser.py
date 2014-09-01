__author__ = 'Tatta'

from urllib2 import urlopen
import re
import os

with open('urls.txt', 'r') as input_file:
    with open('urls_and_mcounters', 'w') as output_file:
        for url in input_file:
            url = url.rstrip()
            response = urlopen(url)
            page_content = response.read()
            match = re.search(r'mc\.yandex\.ru/watch/(\d+)', page_content)
            if match:
                counter_num = match.group(1)
            else:
                counter_num = 'no metrika counter'
            print url, counter_num
            output_file.write('"%s", "%s" %s' % (url, counter_num, os.linesep))
