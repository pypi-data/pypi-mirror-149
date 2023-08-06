import setuptools
 
with open("README.md", "r") as fh:
  long_description = fh.read()
 
setuptools.setup(
  name="openfc",
  version="0.0.1",
  author="Daniel Chen",
  author_email="danielcxh@icloud.com",
  description="An Open Financial Database",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://gitee.com/danielcxh/openfc",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)