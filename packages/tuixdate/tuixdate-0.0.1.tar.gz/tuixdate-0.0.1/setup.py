import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tuixdate",
    author="Ericson Joseph",
    author_email="ericson.estupinnan@tuix.ch",
    description="Tuix Timesheet",
    url="https://github.com/tuixdevelopment/tuixdate",
    license="MIT",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=["tabulate", "certifi"],
    classifiers=[
        # see https://pypi.org/classifiers/
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "tuixdate=tuixdate.main:main",
        ],
    },
)
