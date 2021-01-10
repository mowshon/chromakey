from setuptools import setup
import os
import chromakey


def load_text(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()


long_description = chromakey.__description__
if os.path.exists('README.md'):
    long_description = load_text('README.md')

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
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Multimedia :: Video',
        'Topic :: Scientific/Engineering :: Image Processing'
    ],
    install_requires=load_text("requirements.txt").strip().split("\n"),
)