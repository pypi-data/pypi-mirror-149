import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sequential_rename",
    version="1.0.2",
    author="Stefan Mladenovic (Gizmotechy)",
    author_email="stefan.mladenovic@live.com",
    description="A small package for sequentially renaming files with the same name.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GizmoTechy/Sequential-Rename",
    project_urls={
        "Bug Tracker": "https://github.com/GizmoTechy/Sequential-Rename/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
