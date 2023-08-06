from setuptools import setup, find_packages
from PokemonAnalysis import __version__

setup(
	name='PokemonAnalysis',
	version=__version__,

	url='https://github.com/bushlab-genomics/POKEMON',
	author='BowenJin',
	author_email='bxj139@case.edu',

	include_package_data=True,
	packages=find_packages(),

	install_requires=[
	'fastlmmclib>=0.0.1',
	'biopython>=1.77',
	'scikit-learn>=0.22.2'],

	extras_require={'figure': ['pymol']},

	entry_points={
	'console_scripts':['run_pokemon=PokemonAnalysis.run_pokemon:run_pokemon']
	},

	classifiers=[
	'Intended Audience :: Developers',
	'Programming Language :: Python',
	'Programming Language :: Python :: 3',
	],	

)


