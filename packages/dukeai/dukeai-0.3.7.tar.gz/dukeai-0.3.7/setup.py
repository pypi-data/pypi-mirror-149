from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

if __name__ == "__main__":
    setup(
        name="dukeai",
        version="0.3.7",
        description="Dukeai Development Package",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Shubham Kothari",
        author_email="shubham@duke.ai",
        url="https://duke.ai",
        license="Apache License",
        packages=find_packages(),
        include_package_data=True,
        install_requires=['boto3', 'requests', 'colorama'],
        platforms=["linux", "unix"],
        python_requires=">3.5.2",
        classifiers=["Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent"]
    )

# pip install twine
# python setup.py sdist bdist_wheel
# twine upload dist/*
