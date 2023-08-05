from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='uzbek_latin_cyrillic_converter',
    version='0.2',
    license='MIT',
    author="Sirojiddin Komolov",
    author_email='rhtyme@gmail.com',
    description="A set of tools to convert the text in uzbek between latin and cyrillic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['uzbek_latin_cyrillic_converter'],
    url='https://github.com/Rhtyme/uzbek_latin_cyrillic_converter',
    keywords='converter, uzbek-latin-cyrillic-converter',
    install_requires=[
        'pytest',
    ],
)
