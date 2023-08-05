from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='theory_game',
    version='1.8',
    packages=find_packages(),
    url = 'https://pypi.org/',
    author = 'Denis Perkov',
    author_email = 'denisperkov0@gmail.com',
    description="A package for EGE 19-21 tasks in computer science dedicated to game theory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)