import setuptools

# To publish to private pypi repo, run the following cmds:
# python setup.py sdist bdist_wheel
# pip install -e .
# twine upload --skip-existing dist/*

setuptools.setup(
    name="pkg_calibration",
    version="0.1.2",
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
    py_modules=["pkg_calibration",
                "pkg_calibration.time_series",
                "pkg_calibration.volatility_flat_price",
                "pkg_calibration.volatility_spread",
                "pkg_calibration.volatility_time_spread",
                "pkg_calibration.volatility_underlying"],
    package_dir={'': 'src'},
    install_requires=["numpy", "pandas", "numbers_parser"]
)
