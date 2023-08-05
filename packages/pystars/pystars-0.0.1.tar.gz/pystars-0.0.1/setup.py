import setuptools


setuptools.setup(
    name="pystars",
    version="0.0.1",
    author="alex",
    author_email="baier.oleksandr@chnu.edu.ua",
    description="a short description.",
    long_description='Box simulator for Brawl Stars', # don't touch this, this is your README.md
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)