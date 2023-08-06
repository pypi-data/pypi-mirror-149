from setuptools import setup, find_packages
# python setup.py sdist bdist_wheel
# twine upload dist/*
with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
setup(
    name="srf_hdkj",
    version="0.5.7",
    author="hdkj",
    author_email="",
    description="sanic view Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    install_requires=['ujson==5.1.0', 'openpyxl==3.0.9', 'sanic-jwt'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
