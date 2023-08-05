from setuptools import setup

with open("instructions.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='hubs_predictor',
    version='0.1.2',
    packages=['hubs_predictor'],
    url='https://github.com/3DHubs/ml-engineer-assignment-bendangnuksung/',
    author='bendangnuksung',
    author_email='bendangnuksungimsong@gmail.com',
    description='Price predictions for 3DHubs',
    install_requires=required,
    long_description_content_type="text/markdown",
    long_description=long_description,
    classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],

)