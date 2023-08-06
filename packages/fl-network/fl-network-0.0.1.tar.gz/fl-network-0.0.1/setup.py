from setuptools import find_packages, setup

setup(
    name="fl-network",
    description="Extensible network framework library for federated learning system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords=["FedML", "Redis", "Distribution"],
    license="MIT",
    version="0.0.1",
    url="https://github.com/Rostar-github/fedml-network",
    packages=find_packages(
        include=[
            "FLNetwork",
        ]
    ),
    author="Sida Luo",
    author_email="luosida@qq.com",
    python_requires=">=3.8",
    install_requires=[
        "redis>=4.2.2",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ]
)
