from setuptools import setup

setup(name='dh-nlp',
      version='0.1',
      description='Natural language processing for DH',
      url='https://github.com/standoff-nlp/dh-nlp',
      author='David Lassner',
      author_email='lassner@tu-berlin.de',
      license='MIT',
      packages=['dhspacy'],
      install_requires=[
          'spacy',
          'standoffconverter'
      ],
      zip_safe=False)