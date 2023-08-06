import os
import setuptools

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setuptools.setup(
    name="egauge-python",
    version="0.5.8",
    packages=setuptools.find_namespace_packages(include="egauge.*"),
    install_requires=[
        "crcmod",
        "intelhex",
        "wheel",
        "pexpect",
        "requests>=2.4.2",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": ["ctid-encoder = egauge.ctid.encoder:main"]
    },
    license="MIT License",  # example license
    description=".",
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://bitbucket.org/egauge/python/",
    author="David Mosberger-Tang",
    author_email="davidm@egauge.net",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)
