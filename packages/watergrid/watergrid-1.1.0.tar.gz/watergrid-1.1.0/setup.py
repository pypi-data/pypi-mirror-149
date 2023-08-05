import setuptools
import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="watergrid",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Joshua Zenn",
    description="Lightweight framework for building ETL pipelines.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ARMmaster17/watergrid-python",
    packages=setuptools.find_packages(),
    package_dir={"watergrid": "watergrid"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pycron==3.0.0",
    ],
    extras_require={
        "lock-redis": ["redis==4.2.2"],
        "metrics-elasticsearch": ["elastic-apm==6.9.1"],
    },
    setup_requires=["black==22.3.0"],
)
