import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zpy-api-core",
    version="1.0.12",
    author="Noé Cruz | linkedin.com/in/zurckz/",
    author_email="zurckz.services@gmail.com",
    description="Helper layer for apis development with Python and Flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NoeCruzMW",
    packages=setuptools.find_packages(),
    install_requires=[
        "Flask",
        "flask_cors",
        "marshmallow",
        "marshmallow_objects",
        "aws-lambda-wsgi",
        "requests",
        "Click",
        "python-dateutil"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=['zpy.cli'],
    entry_points={
        'console_scripts': [
            'zpy = zpy.cli:cli',
        ],
    },
    python_requires=">=3.6",
)
