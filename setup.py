import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pawnshop",  # Replace with your own username
<<<<<<< HEAD
    version="0.0.1",
    author="Nils Forssén",
    author_email="forssennils@gmail.com",
    description="Simple chess module",
=======
    version="0.0.3",
    author="Nils Forssén",
    author_email="forssennils@gmail.com",
    description="A simple chess library as hobby project.",
>>>>>>> commenting
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NilsForssen/pawnshop",
    packages=setuptools.find_packages(),
    package_data={
        "pawnshop": ["configurations\\*.JSON"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
