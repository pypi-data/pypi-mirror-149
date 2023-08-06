import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

p = setuptools.find_packages()
print(p)

setuptools.setup(
    name                          = "langur", 
    version                       = "0.0.1",
    author                        = "Russell Ngo",
    author_email                  = "russellnjk@gmail.com",
    description                   = "A simple markup language with high-level abstraction.",
    long_description              = long_description,
    long_description_content_type = "text/markdown",
    url                           = "",
    packages                      = setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
    include_package_data = True,
    package_dir          = {'langur': 'langur'},
    package_data         = {'langur': ['_test/*.lngr',]}
)
