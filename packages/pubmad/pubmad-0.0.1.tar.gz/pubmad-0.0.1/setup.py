from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

# with open('HISTORY.md') as history_file:
#     HISTORY = history_file.read()

setup_args = dict(
    name='pubmad',
    version='0.14',
    description='Useful tools to work with biology',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n',
    license='MIT',
    packages=find_packages(),
    author='Jacopo Bandoni, Pierpaolo Tarasco, William Simoni, Marco Natali',
    author_email='bandoni.jacopo@gmail.com',
    keywords=['biopyhon'],
    url='https://github.com/Pier297/ProgettoBIO',
    download_url='https://pypi.org/project/pubmad/'
)

setup(
    name="pubmad",
    version="0.0.1",
    author='Jacopo Bandoni, Pierpaolo Tarasco, William Simoni, Marco Natali',
    author_email="bandoni.jacopo@gmail.com",
    description="Useful tools to work with biology",
    long_description=README + '\n\n',
    long_description_content_type="text/markdown",
    url="https://github.com/Pier297/ProgettoBIO",
    package_dir={"": "pubmad"},
    packages=find_packages(where="pubmad"),
    python_requires=">=3.6",
)