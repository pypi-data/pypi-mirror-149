import setuptools 
import pathlib
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="zapper",
    version='0.0.1',
    description="Zapper is a utility to help download files concurrently",
    long_description=README,
    long_description_content_type="text/markdown",
    py_modules=['zapper'],
    include_package_data=True,
    author="Abhinay Yadav",
    author_email="abhinayy0@gmail.com",
    url="https://github.com/abhinayy0/zapper.git",
    packages=setuptools.find_packages(exclude=("tests", )),
    install_requires=[
        'Click',"requests", 
    ],
    entry_points='''
        [console_scripts]
        zapper=zapper.zapper:main
    ''',
    classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
]
)
