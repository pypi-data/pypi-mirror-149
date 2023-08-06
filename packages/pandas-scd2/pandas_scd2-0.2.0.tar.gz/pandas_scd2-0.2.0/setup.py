from setuptools import setup


setup(
    name='pandas_scd2',
    version='0.2.0',
    description="slowly changing dimension with pandas",
    url="https://gitlab.com/liranc/pandas_scd",
    packages=['pandas_scd'],
    keywords='slowly changing dimention scd',
    python_requires='>=3.8',
    install_requires=[
          'pandas',
          'SQLAlchemy'
      ],
    extras_require = {
    'all': ['PyMySQL', 'psycopg2-binary'],
    'mysql': ['PyMySQL'],
    'postgres': ['psycopg2-binary']
    }
)
