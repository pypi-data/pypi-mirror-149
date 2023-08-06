# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

# python setup.py sdist bdist_wheel
# python -m twine upload dist/*
# python -m twine upload --repository testpypi dist/*
# pip install -i https://test.pypi.org/simple/ PyPlcnextRsc
import os

import setuptools

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'PyPlcnextRsc', 'about.py'), 'r') as f:
    exec(f.read(), about)

with open('README.md', 'r') as f:
    readme = f.read()

packages = setuptools.find_packages()

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    license=about['__license__'],
    # packages=setuptools.find_packages(),
    packages=packages,
    # packages=[
    #     'PyPlcnextRsc',
    # ],
    python_requires=">=3.7.6",
    # install_requires=[],
    classifiers=[
        'Topic :: Scientific/Engineering',

        'Development Status :: 2 - Pre-Alpha',

        "Operating System :: OS Independent",

        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Information Technology',

        'Natural Language :: English',
        'Natural Language :: Chinese (Simplified)',

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3 :: Only",
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
    ]
)
