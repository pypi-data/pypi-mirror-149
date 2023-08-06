from setuptools import setup

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="pons.py",
    packages=["pons"],
    version="1.1.0",
    license="MIT",
    description="An API wrapper for the PONS dictionary",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Dorukyum",
    url="https://github.com/Dorukyum/pons.py",
    keywords="API, dictionary",
    install_requires=["requests"],
    classifiers=classifiers,
    project_urls={"Source": "https://github.com/Dorukyum/pons.py"},
)
