import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytello-hsu",
    version="3.0.0",
    author="Alexander Doyle",
    author_email="alexanderthegreat2025@gmail.com",
    description="A package to make it easier to fly your tello drone in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Suave101/Py-Tello",
    packages=setuptools.find_packages(),
    project_urls={
        "Documentation": "https://github.com/Suave101/Py-Tello/blob/master/Py-tello%203.0/readme.md",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
