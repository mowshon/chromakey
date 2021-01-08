from setuptools import setup
import os
import chromakey

long_description = chromakey.__description__
if os.path.exists('README.md'):
    with open("README.md", "r") as fh:
        long_description = fh.read()

setup(
    name='chromakey',
    packages=['chromakey'],
    version=chromakey.__version__,
    license=chromakey.__license__,
    description=chromakey.__description__,
    long_description=long_description,
    author=chromakey.__author__,
    author_email=chromakey.__email__,
    url='https://github.com/mowshon/chromakey',
    download_url='https://github.com/mowshon/chromakey',
    keywords=['green screen', 'chroma key', 'remove green screen', 'remove background'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Multimedia :: Video',
        'Topic :: Scientific/Engineering :: Image Processing'
    ],
)