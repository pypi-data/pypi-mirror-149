import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cfmdarts",
    version="0.2.0",
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
    include_package_data=True,    # include everything in source control
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={"": ["src/cfmdarts/*.png"]},
    python_requires=">=3.6",
)