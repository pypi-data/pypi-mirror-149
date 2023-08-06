from setuptools import setup

name = "types-pytz"
description = "Typing stubs for pytz"
long_description = '''
## Typing stubs for pytz

This is a PEP 561 type stub package for the `pytz` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `pytz`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/pytz. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `4e946b74bf18dc932caf41d0257957d85bbabe91`.
'''.lstrip()

setup(name=name,
      version="2021.3.8",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pytz.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pytz-stubs'],
      package_data={'pytz-stubs': ['__init__.pyi', 'exceptions.pyi', 'tzinfo.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
