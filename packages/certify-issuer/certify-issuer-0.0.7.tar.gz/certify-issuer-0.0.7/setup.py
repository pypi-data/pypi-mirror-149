import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="certify-issuer",
    version="0.0.7",
    author="Surenbayar Doloonjin",
    author_email="suugii.sd@gmail.com",
    description="Issue certificates using blockchain and smart contract",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/corex-mn/certify-issuer",
    project_urls={
        "Bug Tracker": "https://github.com/corex-mn/certify-issuer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
