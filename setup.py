
from setuptools import setup
from PyRus import version

setup(
	name = 'Rss Filterer',
	version = version,
	description = 'TODO',
	author = "None",
	author_email = "None",
	scripts = ['PyRus.py'],
	packages = ['PyRus'],
	install_requires = ["setuptools", 'feedreader', 'future'])
