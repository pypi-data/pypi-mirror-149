import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vmhw",
    version="0.0.1",
    author="Zhirong (Kevin) Guo",
    author_email="zguo22@gsb.columbia.edu",
    description="A small example VM package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Julian-Spring-2022/stack-machine-kevingzr-gsb",
    project_urls={
        "Bug Tracker": "https://github.com/Julian-Spring-2022/stack-machine-kevingzr-gsb",
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