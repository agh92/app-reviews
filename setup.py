from setuptools import setup

setup(
    name='reviews',
    version='0.1',
    py_modules=['reviews'],
    install_requires=[
        'Click', 'requests', 'pyquery', 'lxml'
    ],
    entry_points='''
        [console_scripts]
        reviews=reviews:cli
    ''',
)