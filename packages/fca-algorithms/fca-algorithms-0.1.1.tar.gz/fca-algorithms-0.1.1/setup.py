import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fca-algorithms",
    version="0.1.1",
    author="Ramshell",
    author_email="ramshellcinox@gmail.com",
    license="CC By 4.0",
    description="FCA basic algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'apyori>=1.1.2',
        'networkx>=2.5',
        'matplotlib>=3.3',
    ],
    entry_points={
        'console_scripts': [
            'fca_cli=fca.scripts.fca_cli:main',
        ]
    },
)