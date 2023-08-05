from setuptools import setup, find_packages

setup(name='psuedologger',
      version='0.0.1',
      description='Simple logger replacement, can be replaced in a program '+\
                  'the true Python logger.',
      url='https://github.com/StephenMal/psuedologger',
      author='Stephen Maldonado',
      author_email='psuedologger@stephenmal.com',
      packages=find_packages(),
      install_requires=[],
      extras_require={},
      classifiers=['Development Status :: 1 - Planning',
                   'Programming Language :: Python :: 3 :: Only',
                   'Topic :: Utilities']
)
