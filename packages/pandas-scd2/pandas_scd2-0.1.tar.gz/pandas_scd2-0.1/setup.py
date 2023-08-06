from setuptools import setup


setup(
    name='pandas_scd2',
    version='0.1',
    packages=['pandas_scd'],
    keywords='slowly changing dimention scd',
    install_requires=[
          'pandas',
          'SQLAlchemy'
      ],
    extras_require = {
    'full': ['PyMySQL', 'psycopg2-binary'],
    'mysql': ['PyMySQL'],
    'postgres': ['psycopg2-binary']
    }
)