from setuptools import setup,find_packages

setup(
    name='Richdata',
    version='0.5.1',
    packages=find_packages(),
    install_requires=['pandas'],  # add any additional packages that
    extras_require={
        'sqlserver': ['pyodbc'],
        'postgres': ['psycopg2-binary','SQLAlchemy'],
        'bigquery': ['google.cloud.bigquery','google.oauth2'],
        'all':['pyodbc','psycopg2-binary','google.cloud.bigquery','google.oauth2','SQLAlchemy'],
    },
    url='https://github.com/rimedinaz/richdata',
    license='Apache License 2.0',
    author='Richard Medina',
    author_email='rimedinaz@gmail.com',
    description='Rich data and Data Engineering',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.3",
)
