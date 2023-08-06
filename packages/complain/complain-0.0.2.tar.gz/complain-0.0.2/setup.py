import setuptools

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

setuptools.setup(
    name="complain",
    version="0.0.2",
    author="Leg3ndary",
    author_email="bleg3ndary@gmail.com",
    description="A python wrapper for Scott Pakins complaint generator",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/Leg3ndary/complain",
    project_urls={
        "Bug Tracker": "https://github.com/Leg3ndary/complain/issues",
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    package_dir={"": "complain"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)