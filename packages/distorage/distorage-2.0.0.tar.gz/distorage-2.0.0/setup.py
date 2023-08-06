import setuptools

setuptools.setup(
    name="distorage",
    version="2.0.0",
    author="Sellig6792",
    author_email="sellig.dev@gmail.com",
    description="The system to host your files on the Discord application",
    url="https://github.com/Sellig6792/Distorage.py",
    packages=["distorage"],
    keywords=["discord", "storage", "file", "hosting", "upload", "server"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests~=2.26.0"
    ]
)
