import setuptools

# with open("README.md", "r",encoding="utf8") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="threed4t",
    version="0.0.5",
    author="Wen-Hung, Chang 張文宏",
    author_email="beardad1975@nmes.tyc.edu.tw",
    description="3d learning module for Teenagers",
    long_description="3d learning module for Teenagers",
    long_description_content_type="text/markdown",
    url="https://github.com/beardad1975/threed4t",
    #packages=setuptools.find_packages(),
    platforms=["Windows"],
    python_requires=">=3.5",
    packages=['threed4t','模擬3D模組'],
    package_data={'threed4t': ['model4t/*','texture4t/*']},
    install_requires = ['ursina == 4.1.1', ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Microsoft :: Windows",
            #"Operating System :: MacOS",
            #"Operating System :: POSIX :: Linux",
            "Natural Language :: Chinese (Traditional)",
        ],
)