import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
REQUIREMENTS = (HERE / "requirements.txt").read_text()

setup(name="dathas",
      version="0.0.3",
      description=" Enhance your Python dataclasses",
      long_description=README,
      long_description_content_type="text/markdown",
      author="Ziga Ivansek",
      author_email="ziga.ivansek@gmail.com",
      url="https://github.com/zigai/dathas",
      license="MIT",
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3 :: Only",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      package_dir={"": "dathas"},
      py_modules=["dathas"],
      install_requires=REQUIREMENTS)
