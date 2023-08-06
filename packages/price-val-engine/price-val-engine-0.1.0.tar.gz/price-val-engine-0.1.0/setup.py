from setuptools import find_packages, setup

with open('README.md') as f:
    README = f.read()
    
setup(
    name='price-val-engine',
    packages=find_packages(),
    version='0.1.0',
    description='last price revision validation rules',
    # long_description=README,
    author='Chandan Kumar Ojha',
    author_email="mr.chandanojha@gmail.com",
    license='MIT',
    python_requires=">=3.0",
    install_requires=[
        'boto3==1.21.45',
        'botocore==1.24.45'
    ]
)