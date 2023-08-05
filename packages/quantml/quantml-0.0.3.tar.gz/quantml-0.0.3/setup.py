from setuptools import setup, find_packages

"""
Build Info:

Commands:
---------
python setup.py sdist
twine upload dist/*
"""

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='quantml',
    version='0.0.3',
    license='MIT',
    author="Gacoka Mbui, Stevedavies Ndegwa",
    author_email='markgacoka@gmail.com, stevedaviesndegwa@gmail.com',
    description="Algorithmic Trading using Machine Learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['quantml'],
    include_package_data=True,
    url='https://github.com/markgacoka/quantml',
    keywords=['algorithmic trading', 'Crypto', 'Quantitative Finance', 'trading bot'],
    install_requires=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    entry_points={
        "console_scripts": [
            "quantml=quantml.__main__:main"
        ]
    },
    python_requires='>=3.9',
)