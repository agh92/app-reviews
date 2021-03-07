from setuptools import setup

setup(
    name="reviews",
    version="0.1",
    py_modules=["cli", "reviews"],
    install_requires=["Click", "requests", "pyquery", "lxml", "Rx", "feedparser"],
    entry_points="""
        [console_scripts]
        reviews=cli.reviews:cli
    """,
)
