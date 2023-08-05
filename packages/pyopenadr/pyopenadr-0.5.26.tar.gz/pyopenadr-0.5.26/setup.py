from setuptools import setup

long_description="""# PyOpenADR

PyOpenADR has changed its name to [OpenLEADR](https://pypi.org/project/openleadr). You can still use pyopenadr as an alias to openleadr if you want.

Please update your dependencies, and please take a look [here](https://pypi.org/project/openleadr). Thanks.
"""

setup(name="pyopenadr",
      description="Python3 library for building OpenADR Clients (VENs) and Servers (VTNs). Renamed to OpenLEADR.",
      version='0.5.26',
      url='https://openleadr.org',
      packages=['pyopenadr'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      install_requires=['openleadr==0.5.26'])
