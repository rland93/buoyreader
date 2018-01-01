try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    "description": "NOAA buoy data in pandas",
    "author":"Mike Sutherland",
    "url":"https://github.com/rland93/buoyreader",
    "download_url":"https://github.com/rland93/buoyreader.git",
    "author_email":"msutherland@fastmail.com",
    "version":"0.1",
    "install_requires":["nose","pandas","numpy","seaborn","matplotlib"],
    "packages":["buoyreader"],
    "scripts":[],
    "name":"buoyreader"
}
setup(**config)