from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='pubmad',
    version='0.11',
    description='Useful tools to work with biology',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Jacopo Bandoni, Pierpaolo Tarasco, William Simoni, Marco Natali',
    author_email='bandoni.jacopo@gmail.com',
    keywords=['biopyhon'],
    url='https://github.com/Pier297/ProgettoBIO',
    download_url='https://pypi.org/project/pubmad/'
)

setup_requires=[
    'setuptools>=41.0.1',
    'wheel>=0.33.4'
]

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

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)