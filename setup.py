import setuptools
import sys

if sys.version_info[:2] < (3, 6):
    raise RuntimeError("Python version must be >= 3.6")

setuptools.setup(
	name='TeXutils',
    version='0.1',
    author="Sergey",
    author_email="suvorov a_t inr ru",
    packages=setuptools.find_packages(),
    install_requires=[
        'Click',
        'termcolor'
    ],
    entry_points='''
        [console_scripts]
        bibparser=TeXutils.BibParser:main
        delatex=TeXutils.DeLaTeX:main
    ''',
    )
