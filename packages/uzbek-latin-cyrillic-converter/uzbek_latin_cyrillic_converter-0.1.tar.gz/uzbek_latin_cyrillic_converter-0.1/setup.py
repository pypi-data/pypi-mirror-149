from setuptools import setup, find_packages


setup(
    name='uzbek_latin_cyrillic_converter',
    version='0.1',
    license='MIT',
    author="Sirojiddin Komolov",
    author_email='rhtyme@gmail.com',
    packages=find_packages('script'),
    package_dir={'': 'script'},
    url='https://github.com/Rhtyme/uzbek_latin_cyrillic_converter',
    keywords='converter, uzbek-latin-cyrillic-converter',
    install_requires=[
          'pytest',
      ],

)