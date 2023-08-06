import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hiscovid",
    version="0.0.1",
    author="yoshiyasu takefuji",
    author_email="takefuji@keio.jp",
    description="A package for calculating time transition policy scores against COVID-19",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ytakefuji/hiscovid",
    project_urls={
        "Bug Tracker": "https://github.com/ytakefuji/hiscovid",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['hiscovid'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'hiscovid = hiscovid:main'
        ]
    },
)
