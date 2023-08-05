import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyleaps",                     
    version="0.0.1",                        
    author="Fortunato Nucera",                     
    description="Simple porting of the LEAPS package on python. Not optimized yet.",
    long_description=long_description,      
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      
    python_requires='>=3.6',
    py_modules=["pyleaps"],
    package_dir={'':'pyleaps/src'},     
    install_requires=["numpy","statsmodels","pandas"]
)
