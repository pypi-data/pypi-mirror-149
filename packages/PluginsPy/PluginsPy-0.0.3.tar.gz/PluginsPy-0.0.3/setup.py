import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PluginsPy",
    version="0.0.3",
    author="zengjf",
    author_email="zengjf42@163.com",
    description="Plugins Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZengjfOS/PluginsPy",
    project_urls={
        "Bug Tracker": "https://github.com/ZengjfOS/PluginsPy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.0",
)
