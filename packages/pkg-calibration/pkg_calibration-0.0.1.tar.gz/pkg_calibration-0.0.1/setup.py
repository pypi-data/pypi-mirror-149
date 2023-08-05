import setuptools

setuptools.setup(
    name="pkg_calibration",
    version="0.0.1",
    author="Dieg Oatlib",
    description="Package To Calibrate Volatility Parameters",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    py_modules=["pkg_calibration"],
    package_dir={'': 'src'}
)
