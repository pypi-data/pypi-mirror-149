import setuptools

# Read in the requirements.txt file
with open("requirements.txt") as f:
    requirements = []
    for library in f.read().splitlines():
        if "hypothesis" not in library:  # Skip: used only for dev
            requirements.append(library)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cfmdarts",
    version="0.1.4",
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
    package_data={"": ["cfmdarts/data/*"]},
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)