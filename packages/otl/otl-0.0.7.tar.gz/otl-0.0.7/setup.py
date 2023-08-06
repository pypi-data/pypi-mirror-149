import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as requires:
    requires_list = []
    for line in requires.readlines():
        requires_list.append(line.strip())
    # requirements = ','.join(requires_list)
from otl.__version__ import __title__, __version__

setuptools.setup(
    name=__title__,
    version=__version__,
    author="waqu",
    author_email="author@example.com",
    description="A ops tools package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    install_requires=requires_list,
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
