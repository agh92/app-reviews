from setuptools import setup

setup(
    name='app_reviews',
    version='0.1',
    py_modules=['app_reviews'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        app_reviews=app_reviews:cli
    ''',
)