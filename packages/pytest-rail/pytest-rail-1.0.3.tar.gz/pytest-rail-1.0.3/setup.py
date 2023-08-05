from setuptools import setup


def read_file(fname):
    with open(fname) as f:
        return f.read()


setup(
    name='pytest-rail',
    description='pytest plugin for creating TestRail runs and adding results',
    long_description=read_file('README.rst'),
    version='1.0.3',
    author='Anukool Chaturvedi',
    author_email='chaturvedianukool@gmail.com',
    url='http://github.com/anukchat/pytest-rail/',
    packages=[
        'pytest_testrail',
    ],
    package_dir={'pytest_rail': 'pytest_rail'},
    install_requires=[
        'pytest>=3.6',
        'requests>=2.20.0',
    ],
    include_package_data=True,
    entry_points={'pytest11': ['pytest-rail = pytest_rail.conftest']},
)
