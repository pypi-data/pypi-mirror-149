import setuptools

setuptools.setup(
    name="iginx",
    version="0.5.1",
    author="Zi Yuan",
    author_email="ziy20@outlook.com",
    description="IginX Python Client",
    long_description= "IginX Python Client",
    long_description_content_type="text/markdown",
    url="https://github.com/thulab/IginX",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)