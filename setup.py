import sys
from setuptools import setup, find_packages

long_description = open('README.md').read()

setup(
    name='ninesix',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version="0.0.3",
    description='Easy-to-use unified tools for NN logging and managing.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Jogle Lew',
    author_email='author@example.com',
    url='https://github.com/JogleLew/nine-six',
    license='AGPLv3+',
    python_requires='>=3.0',
    keywords=['Nine Six', 'nine-six', 'Logging', 'Logger', 'Grid Search'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Utilities"
    ],
    install_requires=[
       'more_itertools'
    ],
    entry_points={
        "console_scripts": [
            '96grid = ninesix.tool.grid:main'
        ]
    }
)
