from setuptools import setup
from pathlib import Path


with open(Path(__file__).parent / "appstream_python" / "version.txt", "r", encoding="utf-8") as f:
    version = f.read().strip()

with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

setup(name="appstream-python",
      version=version,
      description="A library for dealing with Freedesktop Appstream data",
      long_description=description,
      long_description_content_type="text/markdown",
      author="JakobDev",
      author_email="jakobdev@gmx.de",
      url="https://gitlab.com/JakobDev/appstream-python",
      python_requires=">=3.9",
      include_package_data=True,
      install_requires=[
          "lxml",
      ],
      packages=["appstream_python"],
      license="BSD",
      keywords=["JakobDev", "Appstream", "Freedesktop", "Linux"],
      project_urls={
          "Issue tracker": "https://gitlab.com/JakobDev/appstream-python/-/issues",
          "Documentation": "https://appstream-python.readthedocs.io/en/latest/index.html"
      },
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "Environment :: Other Environment",
          "License :: OSI Approved :: BSD License",
          "Topic :: Games/Entertainment",
          "Operating System :: POSIX",
          "Operating System :: POSIX :: BSD",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3 :: Only",
          "Programming Language :: Python :: Implementation :: CPython"
      ]
)
