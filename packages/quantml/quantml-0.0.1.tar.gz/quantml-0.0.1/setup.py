from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='quantml',
    version='0.0.1',
    license='MIT',
    author="Gacoka Mbui",
    author_email='markgacoka@gmail.com',
    description="Algorithmic Trading using Machine Learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/markgacoka/quantml',
    keywords='algorithmic trading',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)