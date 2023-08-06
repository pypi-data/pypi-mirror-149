# Import required functions
from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

# Call setup function
setup(
    author='Javad Ebadi',
    author_email="javad.ebadi.1990@gmail.com",
    description='Kucoin REST API v2 python implementation',
    name="py_kucoin_extra",
    packages=find_packages(include=["py_kucoin_extra", "py_kucoin_extra.*"]),
    version="1.2.1",
    install_requires=['requests', 'websockets'],
    python_requires='>=3.7',
    license='MIT',
    url='https://github.com/javadebadi/python-kucoin',
    long_description=long_description,
    long_description_content_type='text/markdown'
)