import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Oxford.py-Rewrite",
    version="1.0.1",
    authors=["Haider Ali", "Oskar Manhart | PixelAgent007", "Golder06"],
    author_email="hello@oskar.global",
    description="Oxford API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PixelAgent007/Oxford.py",
    project_urls={
        "Bug Tracker": "https://github.com/PixelAgent007/Oxford.py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['aiohttp', 'requests']
)