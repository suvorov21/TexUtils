#!/usr/bin/env python

import re
from termcolor import colored as col

class DeLaTeX:
    def __init__(self, file_in="", file_out=""):
        self.file_in    = file_in
        self.file_out   = file_out
        self.replace    = []
        
    def AddReplacement(self, l):
        for pair in l:
            self.replace.append(pair)

    def DoParse(self):
        print("Parsing TeX.........", end='')
        
        fo = open(self.file_out, 'w')

        # citations anf ref commands
        # citations prefixes
        cite = 'cite'
        # reference prefixes
        ref = 'ref|autoref|nameref'

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

                # skip/replace inline equations
                # remove symbol which is a prefix, e.g. $\beta$-particle
                line = re.sub(r'\$[^\$]+\$-', '', line)
                # replace the equations
                line = re.sub(r'\$[^\$]+\$', 'X', line)
                # keep percentage sign
                line = re.sub(r'\\(%)', r'\1', line)

                # remove citations and references
                # cite
                line = re.sub(r'in.\\(' + cite + '){[^}]+}', 'in the paper', line)
                line = re.sub(r'(~|)\\(' + cite + '){[^}]+}', '', line)

                # ref
                # replace the direct references with the keywords to keep consistancy
                line = re.sub(r'in (the |)(\\(' + ref + '){fig:[^}]+})', 'in the figure', line)
                line = re.sub(r'in (the |)(\\(' + ref + '){tbl:[^}]+})', 'in the table', line)
                line = re.sub(r'in (the |)(\\(' + ref + '){eq:[^}]+})', 'in the equation', line)
                line = re.sub(r'in (the |)(\\(' + ref + '){(sec|ch):[^}]+})', 'in the section', line)

                # remove all the rest references
                line = re.sub(r'( \\(' + ref + '){[^}]+})', '', line)
                line = re.sub(r'(~\\(' + ref + '){[^}]+})', '', line)
                line = re.sub(r'( \(\\(' + ref + '){[^}]+}\))', '', line)
                line = re.sub(r'(\\(' + ref + '){[^}]+})', '', line)

                # extract sections' headers
                line = re.sub(r'\\part{(.+)}',r'\1',line)
                line = re.sub(r'\\chapter{(.+)}',r'\1',line)
                line = re.sub(r'\\section{(.+)}',r'\1',line)
                line = re.sub(r'\\subsection{(.+)}',r'\1',line)
                line = re.sub(r'\\subsubsection{(.+)}',r'\1',line)
                line = re.sub(r'\\subsubsubsection{(.+)}',r'\1',line)

                for pair in self.replace:
                    line = re.sub(pair[0], pair[1], line)
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
    parser.DoParse()

if __name__ == '__main__':
    main()