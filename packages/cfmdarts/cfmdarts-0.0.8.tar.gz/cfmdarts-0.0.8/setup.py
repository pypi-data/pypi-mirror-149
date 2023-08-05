import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cfmdarts",
    version="0.0.8",
    author="Matthew Squire, Luke Sargent, Cameron Trew, Aron Russell",
    description="cfmdarts is a Python library that simulates the projectile motion of darts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Araphor0/cfmdarts",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)