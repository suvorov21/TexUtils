# TeX utils

Package with few TeX utils:
1. Parse bib file and transform some Unicode symbols to TeX formulas. Useful for parsing files exported from Mendeley/Zotero. In addition, remove abstract field that is not used in citations 
2. Parse TeX file and extract plain text content for further feeding into spell checker e.g. Grammarly
3. Find unused figures in the TeX project

## Usage

Install with 
```bash
python3 -m pip install -e .
```

Usage:
```bash
# cleanup bib file
bibparser library.bib library_new.bib
# extract plain text from TeX file
delatex input.tex output.txt 
# print unused figures
figunused /path/to/tex/project 
```