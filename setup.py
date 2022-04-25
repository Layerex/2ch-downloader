import setuptools

from _2ch_downloader import __desc__, __version__


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="2ch-downloader",
    version=__version__,
    py_modules=["_2ch_downloader"],
    author="Layerex",
    author_email="layerex@dismail.de",
    description=__desc__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Layerex/2ch-downloader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    entry_points={
        "console_scripts": [
            "2ch-downloader = _2ch_downloader:main",
        ],
    },
    install_requires=["requests"],
)
