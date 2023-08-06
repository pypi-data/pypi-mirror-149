from setuptools import setup, find_packages


setup(
    name='urlToHTML',
    version='0.1',
    license='MIT',
    author="Ronnie Atuhaire",
    author_email='ronlinx6@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Ronlin1/urlToHTML',
    keywords='URL HTML Save',
    install_requires=[
          'requests',
      ],

)