from setuptools import setup, find_packages

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Intended Audience :: Science/Research"
]

with open("README.md", "r") as rm:
    descrip = rm.read()

setup(name="grprec",
      version='0.0.2',
      description='grprec is a python library for analizing, building, testing group recommendation system approaches',
      py_modules=["group_generation", "evaluate",
                  "preprocessing", "score_agregation", "model"],
      package_dir={'': '.'},
      url='',
      license='MIT',
      author='Rezgui Abdelkader',
      author_email='ha_rezgui@esi.dz',
      classifiers=classifiers,
      long_description=descrip,
      long_description_content_type="text/markdown",
      keywords='group recommendation',
      packages=find_packages(),
      install_requires=["numpy ~=  1.22.3",
                        "pandas ~= 1.4.2", "surprise ~= 0.1"]
      )
