import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read();fh.close()

setuptools.setup(
    name="lrspy",
    version="1.0.0",
    author="Liu RongShuo",
    author_email="lrs2022win@outlook.com",
    description="This is PYLRS lib.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://lrsgzs.top",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "lrspy"},
    packages=setuptools.find_packages(where="lrspy"),
    python_requires=">=3.7",
)