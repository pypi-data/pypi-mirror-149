from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="package_name_1",
    version="0.0.1",
    author="Rafael",
    author_email="rafaelsomr1@gmail.com",
    description="Desafio criação de pacotes",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rafaelsom",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)