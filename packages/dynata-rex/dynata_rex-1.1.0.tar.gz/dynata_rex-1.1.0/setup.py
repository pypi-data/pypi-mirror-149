import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setuptools.setup(
    name="dynata_rex",
    version="1.1.0",
    author="REX Maintainers",
    author_email="tech.supply@Dynata.com",
    description=("Package for building and interacting with the "
                 "Dynata Respondent Exchange (REX)"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dynata/rex-sdk-python",
    packages=setuptools.find_packages(exclude=('tests', )),
    platforms=['Any'],
    install_requires=requirements,
    setup_requires=['pytest-runner'],
    extras_require={
        # pip install -e ".[testing]"
        "testing": ['pytest'],
        ':python_version == "3.6"': [
            "typing-extensions==4.0.1",
            'dataclasses==0.8'
        ],
        ':python_version == "3.7"': [
            "typing-extensions==4.0.1"
        ]
    },
    tests_require=['pytest'],
    keywords='respondent exchange rex smor dynata python',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
