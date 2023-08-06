import setuptools

with open("src/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Olympics",
    version="1.2022",
    author="Guo Jiarong",
    author_email="1950955951@qq.com",
    description="Something about olympic games.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["turtle>=0.0.1"]
)
