import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wordtriepy",
    version="0.0.1",
    author="Christian Vorhemus",
    author_email="",
    description="A trie filled with words from several languages (English - en, German - de , French - fr, Spanish - es, Portuguese - pt)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/christian-vorhemus/wordtrie",
    project_urls={
        "Bug Tracker": "https://github.com/christian-vorhemus/wordtrie/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["wordtriepy"],
    package_dir={"wordtriepy": "wordtriepy"},
    package_data={"wordtriepy": ["assets/*"]},
    python_requires=">=3.5",
)
