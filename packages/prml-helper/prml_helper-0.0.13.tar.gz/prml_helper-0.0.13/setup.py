from setuptools import setup, find_packages

setup(
    name="prml_helper",
    version="0.0.13",
    author="qwertykid",
    author_email="qwertykid583@gmail.com",
    description="Helper functions for prml",
    packages=find_packages(),
    install_requires=["nltk","numpy", "pandas", "scikit-learn",],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)