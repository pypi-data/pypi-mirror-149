from setuptools import setup, find_packages


setup(
    name='dynamo-crud',
    version='1.0.1.1-alpha',
    license='GPL3',
    author="Stuart Anderson",
    author_email='stuart@tobupengin.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Pengin-Open-Source/dynamo-crud',
    keywords='DynamoDB CRUD',
    install_requires=['boto3','python-decouple']
)
