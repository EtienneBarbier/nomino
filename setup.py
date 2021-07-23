from setuptools import setup, find_packages
import nomino

# This call to setup() does all the work
setup(
    name="nomino",
    version=nomino.__version__,
    packages=find_packages(),
    author="Etienne Barbier",
    author_email="barbier.dev@gmail.com",
    description="Generate words based on number of syllables",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/EtienneBarbier/nomino",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "nomino=nomino.__main__:main",
        ]
    },
)