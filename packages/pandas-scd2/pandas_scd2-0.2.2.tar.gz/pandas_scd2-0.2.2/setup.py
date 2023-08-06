from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pandas_scd2',
    version='0.2.2',
    description="slowly changing dimension with pandas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/liranc/pandas_scd",
    packages=find_packages(),
    keywords='slowly changing dimention scd',
    py_modules=["pandas_scd"],
    package_dir={'':'src'},
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
