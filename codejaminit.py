#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

from lxml import etree


BASE_CODE = r"""#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import difflib


class Case(object):

    def __init__(self, f_out, i, n, a, b):
        self.f_out = f_out
        self.i = i
        self.n = n
        self.a = a
        self.b = b

    ###################### modify here #####################
    def get_result(self):
        pass
    ########################################################

    def run(self):
        result = self.get_result()
        ###################### modify here #####################
        self.f_out.write('Case #%d: ' % self.i)
        self.f_out.write('%d\n' % result)
        ########################################################
        return None


def parse_cmd_args():
    parser = argparse.ArgumentParser(description='initiate a Google code jam contest problem')
    parser.add_argument('input', help='input file path')
    args = parser.parse_args()
    input_path = os.path.abspath(args.input)
    return input_path


def read_line(f_in, typ=None):
    if isinstance(f_in, file):
        line = f_in.readline()
    elif isinstance(f_in, (str, unicode)):
        line = f_in
    else:
        raise TypeError('unknown parameter type: %s' % type(f_in))

    tokens = line.strip().split()
    if typ:
        r = [typ(e) for e in tokens]
    else:
        r = tokens
    return r


def read_a_case(f_in, m, func_list):
    r = []
    for i in range(m):
        line = f_in.readline().strip()
        func = func_list[i]
        r.append(func(line))
    return r


def sample_diff(path_a, path_b):
    with open(path_a) as f_a, open(path_b) as f_b:
        a = f_a.readlines()
        b = f_b.readlines()

    d = difflib.Differ()
    diff = d.compare(a, b)
    print ''.join(list(diff))
    return None


def check_result(in_path, an_path, out_path):
    if os.path.basename(in_path) == 'sample.in':
        # comparing sample answers and output
        print '######### comparing sample answers and output #######'
        sample_diff(an_path, out_path)
    else:
        # print the first k lines in output file
        k = 5
        print '######## the fist %d lines of %s #######' % (k, out_path)
        with open(out_path) as out:
            for i in range(k):
                print out.readline(),
    return None


def main():
    in_path = parse_cmd_args()
    out_path = in_path.rstrip('.in') + '.out'
    an_path = in_path.rstrip('.in') + '.an'

    f_in = open(in_path)
    f_out = open(out_path, 'wb')

    T = read_line(f_in, int)
    print T

    for i in range(T):
        ############### modify here #######################

        # n, a, b = read_a_case(f_in, 3, [int, split_line, split_line])

        # c = Case(f_out, i + 1, n, a, b)
        ##################################################
        c.run()
        del c
    f_in.close()
    f_out.close()

    check_result(in_path, an_path, out_path)

    return None


if __name__ == '__main__':
    main()

"""


class Contest(object):
    def __init__(self, info):
        self.title = info['contest_title']
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '%s/' % self.title)
        self.problems = self.create_problem(info['problems'])

    def create_problem(self, problems):
        return [Problem(pro_info, self.path) for pro_info in problems]

    def mkdir(self):
        try:
            os.mkdir(self.path)
            print 'finish making contest directory: %s' % self.path
        # directory maybe exists
        except OSError, e:
            print e
        return None

    def run(self):
        self.mkdir()
        for p in self.problems:
            p.run()
        return None


class Problem(object):
    def __init__(self, pro_info, contest_path):
        self.contest_path = contest_path
        self.name = pro_info['name']
        self.order = pro_info['order']
        self.sample_in = pro_info['sample_in']
        self.sample_an = pro_info['sample_an']
        self.path = os.path.join(contest_path, '%s/' % self.name)

    def init_code_file(self):
        code_path = os.path.join(self.path, self.name + '.py')
        with open(code_path, 'wb') as f_code:
            global BASE_CODE
            f_code.write(BASE_CODE)
        os.chmod(code_path, 0777)    # the leading zero means it is octal
        print 'finish create source code file: %s' % code_path
        return None

    def write_sample(self):
        sample_in_path = os.path.join(self.path, 'sample.in')
        # standard answers of sample.in
        sample_an_path = os.path.join(self.path, 'sample.an')

        with open(sample_in_path, 'wb') as f_in:
            f_in.writelines([line + '\n' for line in self.sample_in])
        with open(sample_an_path, 'wb') as f_an:
            f_an.writelines([line + '\n' for line in self.sample_an])
        print 'finish writing sample input file: %s' % sample_in_path
        print 'finish writing sample answers file: %s' % sample_an_path
        return None

    def mkdir(self):
        try:
            os.mkdir(self.path)
            print 'finish making problem directory: %s' % self.path
        # directory maybe exists
        except OSError, e:
            print e
        return None

    def run(self):
        self.mkdir()
        self.init_code_file()
        self.write_sample()
        return None


def parse_cmd_args():
    parser = argparse.ArgumentParser(description='initiate a Google code jam contest')
    parser.add_argument('html', help='Contest HTML file')
    args = parser.parse_args()
    html_path = os.path.abspath(args.html)
    return html_path


def parse_html(html_path):
    with open(html_path) as html:
        root = etree.HTML(html.read())
    info = {}
    contest_title = root.xpath('.//div[@id="dsb-contest-title"]/text()')[0].strip().replace(' ', '_')
    info['contest_title'] = contest_title
    problem_list = root.xpath('.//*[@id="dsb-problem-selection-list"]/div/div/div/text()')
    problem_list = [p.strip().replace(' ', '_').replace('.', '') for p in problem_list]
    info['problems'] = []
    for i, name in enumerate(problem_list):
        problem = {}
        lines = root.xpath('//*[@id="dsb-problem-content-div%d"]/div[@class="problem-io-wrapper"]/table/tbody/tr[2]/td[1]/code/text()' % i)
        sample_in = [e.strip() for e in lines]
        problem['sample_in'] = sample_in
        lines = root.xpath('//*[@id="dsb-problem-content-div%d"]/div[@class="problem-io-wrapper"]/table/tbody/tr[2]/td[2]/code/text()' % i)
        sample_an = [e.strip() for e in lines]
        problem['sample_an'] = sample_an
        problem['order'] = i
        problem['name'] = name
        info['problems'].append(problem)
    return info


def main():
    html_path = parse_cmd_args()
    info = parse_html(html_path)
    c = Contest(info)
    c.run()
    return None


if __name__ == '__main__':
    main()
