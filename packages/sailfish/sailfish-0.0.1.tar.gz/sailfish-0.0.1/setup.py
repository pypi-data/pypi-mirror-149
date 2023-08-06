import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sailfish',
    version='0.0.1',
    author='Justin Chae',
    author_email='justin.chae@dyna-lab.com',
    description='Sailfish provides helpful utilities and pipelines to optimize Pandas dataframes. This Sailfish project'
                'replaces pd-helper 1.0.0 which is deprecated with sailfish 1.0.0.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/justinhchae/sailfish",
    project_urls={
        "Download URL": "https://github.com/justinhchae/sailfish/archive/refs/tags/0.0.2.tar.gz",
    },
    classifiers=[
        # "Development Status :: 5 - Production/Stable",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=['pandas', 'numpy', 'tqdm', 'shortuuid'],
    python_requires=">=3.7",
)
