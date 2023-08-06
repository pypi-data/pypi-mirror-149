from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="alphaturtle",
    version="1.2",
    description="To Draw Alphabet And Number Using Turtle Module",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/C0DE-SLAYER/alphaturtle",
    author="Faisal Ali Sayyed",
    author_email="fsali315@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["alphaturtle"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "alphaturtle=alphaturtle.alphaturtle_cli:main",
        ]
    },
)