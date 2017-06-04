from distutils.core import setup

setup(
    name='TheAnnotatedLife',
    version='0.1.0',
    author='J. Mann',
    author_email='jackarthurm@gmail.com',
    packages=['tal', 
              'tal.api',
              'taltest'],
    scripts=[],
    url=None,
    license='LICENSE.txt',
    description='A blogging platform API.',
    long_description=open('README.txt').read(),
    install_requires=[
        "Flask>=0.12",
        "SQLAlchemy==1.1.6",
        "Flask-SQLAlchemy>=2.2",
        "marshmallow-sqlalchemy>=0.13.1",
        "psycopg2>=2.7.1"
        ]
    )