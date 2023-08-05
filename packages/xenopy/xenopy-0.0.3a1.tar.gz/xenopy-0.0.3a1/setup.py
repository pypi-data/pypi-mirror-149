import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xenopy",
    version="0.0.3a1",
    author="Ziang Zhou",
    author_email="ziang.zhou518@gmail.com",
    description="The most straightforward and efficient python wrapper for xeno-canto API 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/realzza/xenopy",
    project_urls={
        "Bug Tracker": "https://github.com/realzza/xenopy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires = [
        'tqdm',
        'multiprocess'
    ],
    python_requires=">=3.6",
)