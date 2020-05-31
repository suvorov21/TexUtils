#!/usr/bin/env python

import re

class DeLaTeX:
    def __init__(self, file_in="", file_out=""):
        self.file_in    = file_in
        self.file_out   = file_out

        # citations anf ref commands
        # citations prefixes
        self.cite = 'cite'
        # reference prefixes
        self.ref = 'ref|autoref|nameref'

        # fill the replacement list with:
        # [regex,       replacement]
        self.replace    = ([
            # remove symbol which is a prefix, e.g. $\beta$-particle
            [r'\$[^\$]+\$-',            ''],
            # replace the equations
            [r'\$[^\$]+\$',             'X'],
            # keep percentage sign
            [r'\\(%)',                  r'\1'],
            # replace all the dashes
            [r'(---|--|-)',             '-'],

            # remove citations and references
            [r'in.(Ref\..|)\\(' + self.cite + '){[^}]+}', '  in the paper'],
            [r'(~|)\\(' + self.cite + '){[^}]+}',            ''],
            # references
            # replace the direct references with the keywords to keep consistancy
            [r'in (the |)(\\(' + self.ref + '){fig:[^}]+})', 'in the figure'],
            [r'in (the |)(\\(' + self.ref + '){tbl:[^}]+})', 'in the table'],
            [r'in (the |)(\\(' + self.ref + '){eq:[^}]+})',  'in the equation'],
            [r'in (the |)(\\(' + self.ref + '){(sec|ch):[^}]+})', 'in the section'],

            # remove all the rest references
            [r'( \\(' + self.ref + '){[^}]+})',      ''],
            [r'(~\\(' + self.ref + '){[^}]+})',      ''],
            [r'( \(\\(' + self.ref + '){[^}]+}\))',  ''],
            [r'(\\(' + self.ref + '){[^}]+})',       ''],

            # extract sections' headers
            [r'\\part{(.+)}',                   r'\1'],
            [r'\\chapter{(.+)}',                r'\1'],
            [r'\\section{(.+)}',                r'\1'],
            [r'\\subsection{(.+)}',             r'\1'],
            [r'\\subsubsection{(.+)}',          r'\1'],
            [r'\\subsubsubsection{(.+)}',       r'\1']
            ])

    def add_replacement(self, l):
        for pair in l:
            self.replace.append(pair)

    def do_parse(self):
        print("Parsing TeX.........", end='')

        fo = open(self.file_out, 'w')

        with open(self.file_in) as f:
            i = 0
            block = ''
            # skip headers
            for line in f:
                if r'\begin{document}' in line:
                    break
            f.readline()

            # read body
            for line in f:
                # EOF
                if r'\end{document}' in line:
                    break
                # service tags
                if r'\maketitle' in line or r'\clearpage' in line or \
                r'\tableofcontents' in line or r'\linenumbers' in line:
                    continue
                # skip labels
                if r'\label' in line:
                    continue
                # skip all equation/figures/tables/comments  blocks
                if r'\begin' in line and block == '':
                    block = re.sub(r'\\begin{([^}]+)}.*\n',r'\1',line)

                if block != '' and block != 'itemize' and block != 'enumerate':
                    end_block = r'\end{' + block + "}"
                    if end_block in line:
                        block = ''
                        continue
                    else:
                        continue

                # parse item or numerate lists
                if block == 'itemize' or block == 'enumerate':
                    if r'\begin' in line:
                        continue;
                    line = re.sub(r'\\item', '', line)
                    if r'\end' in line:
                        block = ''
                        continue;

                # do the replacements from self.replace
                for pair in self.replace:
                    try:
                        line = re.sub(pair[0], pair[1], line)
                    except:
                        print(f'[{col("FAIL", color="red")}]')
                        print(f'Error while parsing with regex: {pair[0]}')
                        return False

                fo.write(line)

        fo.close()
        if block == '':
            print(f'[{col("OK", color="green")}]')
            return True
        else:
            print(f'[{col("FAIL", color="red")}]')
            print(f'Some begin//end block remained unparsed')
            print('Some part of the file could be missed')
            return False

import click
from termcolor import colored as col
@click.command()
@click.argument('input_file')
@click.argument('output_file')
def main(input_file, output_file):
    parser =  DeLaTeX(input_file, output_file)
    parser.do_parse()

if __name__ == '__main__':
    main()
