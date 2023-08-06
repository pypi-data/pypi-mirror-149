import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-tfvars",
    version="0.1.0",
    author="Andy Klier",
    author_email="andyklier@gmail.com",
    description="read secrets from terraform tfvars files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/shindagger/python-tfvars",
    packages = ['tfvars'],
    install_requires= ['setuptools'], 
    python_requires='>=3.6',
#    entry_points = {
#        'console_scripts': ['nef=nef.main:main'],
#    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
