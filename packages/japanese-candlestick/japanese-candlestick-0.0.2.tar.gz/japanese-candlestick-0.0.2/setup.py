import setuptools
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = list(parse_requirements("requirements.txt", session='hack'))
# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="japanese-candlestick",
    version="0.0.2",
    author="Vincent Vandenbussche",
    author_email="vandenbussche.vincent@gmail.com",
    license="MIT",
    description="Japanese candlestick pattern",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vincent-vdb/japanese-candlestick-pattern",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    keywords="trading candlestick analysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    install_requires=reqs,
)
