import setuptools

with open("README.md", "r") as f:
	long_description = f.read()

setuptools.setup(
	name="class-diagram-generator",
	version="2.0.7",
	author="Rokas Puzonas",
	author_email="rokas.puz@gmail.com",
	description="Generate standardized class diagrams based on C# source code",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/RokasPuzonas/class-diagram-generator",
	project_urls={
		"Source Code": "https://github.com/RokasPuzonas/class-diagram-generator",
	},
	license="GNU GPLv2",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"Topic :: Utilities",
		"Intended Audience :: Developers",
	],
	install_requires=["lark", "Pillow"],
	python_requires=">=3.10",
)
