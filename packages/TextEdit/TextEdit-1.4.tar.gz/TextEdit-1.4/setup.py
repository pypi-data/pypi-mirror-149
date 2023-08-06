from codecs     import open
from inspect    import getsource
from os.path    import abspath, dirname, join
import setuptools

here = abspath(dirname(getsource(lambda:0)))

with open(join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="TextEdit",
    version="1.4",
    author="Corentin Perdry",
    author_email="corentin.perdry@gmail.com",
    description="A small module for to display the letters at the sequence.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/C0rent1Perdry/TextEdit-1.4",
    project_urls={
        "Bug Tracker": "https://github.com/C0rent1Perdry/TextEdit-1.4/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['sound/*.wav']},
    python_requires=">=3.6",
)