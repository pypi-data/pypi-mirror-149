from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'distributions_for_dsnd/README.md').read_text(encoding='utf-8')

setup(name='distributions_for_dsnd',
      version='0.5',
      description='Gaussian and Binomial distributions',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['distributions_for_dsnd'],
      author = 'Mona Anderssen',
      zip_safe=False)
