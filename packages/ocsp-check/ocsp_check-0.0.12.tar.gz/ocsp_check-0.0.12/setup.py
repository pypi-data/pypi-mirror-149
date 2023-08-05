from distutils.core import setup
import os

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    dependencies = f.read().splitlines()

setup(
    name='ocsp_check',
    version='0.0.12',
    url='https://github.com/MKaterbarg/ocsp_check',
    license='MIT',
    author='Martijn Katerbarg',
    packages=['ocsp_check'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='martijnkaterbarg@gmail.com',
    description='Perform GET and POST OCSP checks.',
    install_requires=[
        'requests',
        'cryptography'
    ],
    entry_points={
        'console_scripts': [
            'ocsp_check = ocsp_check.main:main',
        ],
    },
)