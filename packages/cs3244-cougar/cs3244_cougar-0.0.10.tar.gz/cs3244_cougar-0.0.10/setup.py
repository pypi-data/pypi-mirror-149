import setuptools


setuptools.setup(
    name="cs3244_cougar", 
    version="0.0.10",
    author="Eugene Lim",
    author_email="elimwj@u.nus.edu",
    description="NUS CS3244 Assignment",
    long_description="Utilities for the assignments of NUS CS3244 Machine Learning",
    install_requires=["torch", "matplotlib"],
    keywords=["cs3244"],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)
