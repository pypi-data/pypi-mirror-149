from setuptools import setup, find_packages

setup(
    name="ddd_objects",
    version="0.3.18",
    author="wangziling100",
    author_email="wangziling100@163.com",
    description="In this lib some base objects under concept ddd are defined",
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)