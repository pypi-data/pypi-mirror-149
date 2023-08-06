from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
      long_description = fh.read()

setup(name='plus_bi_main',
      version='0.4.9',
      description='Plus BI modules',
      long_description=long_description,
      url='https://gitlab.com/mvdg_dsc/nl-plus-bi-main-modules',
      author='Pascal van de Pol',
      author_email='pascal@vandepol.tweak.nl',
      license='MIT',
      package_dir={"":"plus_bi_main"},
      packages=find_packages(where="plus_bi_main"),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires=">=3.7"
      )