from setuptools import find_packages, setup

setup(
    name="wkhtmltopdf-proxy",
    version="1.0.0",
    description="A lightweight drop-in replacement for wkhtmltopdf that proxies PDF generation requests to a remote API. It mimics the original CLI interface while transparently offloading the rendering process to a remote service.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/apikcloud/wkhtmltopdf-proxy",
    author="Aurelien ROY",
    author_email="aro@apik.cloud",
    license="BSD 2-clause",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "wkhtmltopdf-proxy = src.main:main",
        ],
    },
)
