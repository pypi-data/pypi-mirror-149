import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Tiny_URL",
    version="0.1.3",
    author="orarange",
    author_email="arigatoudane@outlook.jp",
    description="this is an tiny url Python wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/minato37103710/Tiny-url-Wrapper",
    project_urls={
        "Bug Tracker": "https://github.com/minato37103710/Tiny-url-Wrapper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)