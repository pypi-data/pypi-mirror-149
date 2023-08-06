from setuptools import setup, find_packages

setup(
  name = 'onelinerise',

  version = "1.0.0",
  packages = find_packages(), # What can I say I'm lazy

  author = "Jus-Codin",

  license="Unlicense",

  description = "Write oneline python code easily and have fun",
  long_description = open('README.md').read(),
  long_description_content_type="text/markdown",

  url = "https://github.com/Jus-Codin/OneLinerise",

  classifiers = [
    "Programming Language :: Python",
    "Development Status :: 5 - Production/Stable",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10"
  ],
  python_requires='>=3.8.0'
)
