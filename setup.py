import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vb2html-benland100",
    version="0.0.1",
    author="Benjamin J. Land",
    author_email="benland100@gmail.com",
    description="A tool to convert (the SRL Forums) VBulletin 4 databases to a static website.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GNU General Public License v3 (GPLv3)",
    platforms="any",
    url="https://github.com/BenLand100/vb2html",
    project_urls={
        "Bug Tracker": "https://github.com/BenLand100/vb2html/issues"
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
    packages=['vb2html'],
    scripts=[],
    python_requires=">=3.7",
    install_requires=[
        "MySQLdb",
        "pandas",
        "bbcode",
    ]
)
