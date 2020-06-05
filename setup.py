import setuptools

setuptools.setup(
    name='TeXutils',
    version='0.1',
    author="Sergey",
    author_email="suvorov a_t inr ru",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
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
