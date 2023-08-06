import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pq-json",
    version="0.0.3.1",
    author="mumubebe",
    description="pq is a Python command-line JSON processor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mumubebe/pq/",
    project_urls={
        "Bug Tracker": "https://github.com/mumubebe/pq/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    setup_requires=["wheel"],
    install_requires=[
          'rich',
      ],
    entry_points={
        "console_scripts": [
            "pq=pq.cli:main",
        ],
    },
)