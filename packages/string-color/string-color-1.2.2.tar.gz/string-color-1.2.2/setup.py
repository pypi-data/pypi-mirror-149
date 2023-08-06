import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="string-color",
    version="1.2.2",
    author="Andy Klier",
    author_email="andyklier@gmail.com",
    description="just another mod to print strings in 256 colors in the terminal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/shindagger/string-color",
    packages=['stringcolor'],
    install_requires=['setuptools', 'columnar>=1.3.1', 'colorama'],
    package_data={'stringcolor': ['*.json']},
    entry_points={
        'console_scripts': ['string-color=stringcolor.main:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
