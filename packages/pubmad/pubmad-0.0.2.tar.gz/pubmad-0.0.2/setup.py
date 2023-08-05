from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

# with open('HISTORY.md') as history_file:
#     HISTORY = history_file.read()

setup(
    name="pubmad",
    version="0.0.2",
    author='Jacopo Bandoni, Pierpaolo Tarasco, William Simoni, Marco Natali',
    author_email="bandoni.jacopo@gmail.com",
    description="Useful tools to work with biology",
    long_description=README + '\n\n',
    long_description_content_type="text/markdown",
    url="https://github.com/Pier297/ProgettoBIO",
    packages=['pubmad'],
    python_requires=">=3.6",
    install_requires = [
    'biopython'
    'certifi'
    'charset-normalizer'
    'click'
    'cycler'
    'filelock'
    'fonttools'
    'huggingface-hub'
    'idna'
    'joblib'
    'kiwisolver'
    'matplotlib'
    'networkx'
    'nltk'
    'numpy'
    'packaging'
    'Pillow'
    'pymed'
    'pyparsing'
    'python-dateutil'
    'PyYAML'
    'regex'
    'requests'
    'sacremoses'
    'six'
    'tokenizers'
    'torch'
    'tqdm'
    'transformers'
    'typing-extensions'
    'urllib3'
]
)