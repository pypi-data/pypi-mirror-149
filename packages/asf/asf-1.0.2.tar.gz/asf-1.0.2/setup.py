from distutils.core import setup

import setuptools

import asf

setup(
    name='asf',  # How you named your package folder (MyLib)
    version=asf.__version__,  # Start with a small number and increase it with every change you make
    description='Python Base Library for AWS Serverless Framework',  # Give a short description about your library
    author='Brusco Lorenzo',  # Type in your name
    author_email='bruscolorenzo92@cgmail.com',  # Type in your E-Mail
    packages=setuptools.find_packages(),
    package_data={
        "": ["py.typed"]
    },
    install_requires=[line.strip() for line in open("requirements.txt").readlines() if line.strip()],
    classifiers=[
        'Development Status :: 5 - Production/Stable',  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6, <=3.10',
)
