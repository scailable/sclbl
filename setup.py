import setuptools

# get long description
with open("README.md", "r") as fh:
    long_description = fh.read()

exec(open('sclbl/version.py').read())

setuptools.setup(
    name="sclbl",
    version=__version__,
    author="Maurits Kaptein",
    author_email="maurits.kaptein@scailable.net",
    description="Python package for uploading sklearn and onnx models to Scailable toolchain.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://www.scailable.net",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'sclbl = sclbl.cli:main'
        ]
    },
    python_requires='>=3.7',
    install_requires=['click', 'sclblpy']
)
