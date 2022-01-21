from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in stock_entry_auto/__init__.py
from stock_entry_auto import __version__ as version

setup(
	name="stock_entry_auto",
	version=version,
	description="stock entry",
	author="Matiyas Solutions",
	author_email="develop.matiyas@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
