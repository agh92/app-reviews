import os
import sys
from typing import Callable

import click

import stores
from stores.Model.review import Review
from stores.itunes.App import App
from stores.itunes.functions import reviews as apple_reviews
from stores.google_play import reviews as play_reviews
from stores import code_choices


@click.group()
@click.option("-v", "--verbose", "verbose", is_flag=True)
def cli(verbose: bool):
    stores.VERBOSE = verbose


@cli.command()
@click.option("-id", "--app-id", "app_id", required=True, type=str)
@click.option(
    "-cc",
    "--country-code",
    "country_code",
    required=True,
    type=click.Choice(code_choices),
)
@click.option(
    "-o",
    "--output",
    "output",
    required=False,
    type=click.Path(file_okay=True, dir_okay=False, writable=True, resolve_path=True),
)
def play(app_id: str, country_code: str, output: str):
    download_reviews(app_id, country_code, play_reviews, output)


@cli.command()
@click.option("-id", "--app-id", "app_id", required=True, type=str)
@click.option(
    "-cc",
    "--country-code",
    "country_code",
    required=True,
    type=click.Choice(code_choices),
)
@click.option(
    "-o",
    "--output",
    "output",
    required=False,
    type=click.Path(file_okay=True, dir_okay=False, writable=True, resolve_path=True),
)
def itunes(app_id: str, country_code: str, output: str):
    download_reviews(app_id, country_code, apple_reviews, output)


@cli.command()
@click.option("-id", "--app-id", "app_id", required=True, type=str)
@click.option(
    "-cc",
    "--country-code",
    "country_code",
    required=True,
    type=click.Choice(code_choices),
)
@click.option(
    "-o",
    "--output",
    "output",
    required=False,
    type=click.Path(file_okay=True, dir_okay=False, writable=True, resolve_path=True),
)
def temp(app_id: str, country_code: str, output: str):
    App(app_id, country_code).reviews.subscribe(lambda value: print(value.to_json()))


def download_reviews(
    app_id: str,
    country_code: str,
    download_fn: Callable[[str, str], list[Review]],
    output: str,
):
    if output is not None and os.path.isfile(output) and os.stat(output).st_size > 0:
        raise click.BadOptionUsage("output", "destination file is not empty!")

    reviews = download_fn(app_id, country_code)

    if len(reviews) > 0:
        with open(output, "w") if output is not None else sys.stdout as file:
            print(
                "[", ",".join([review.to_json() for review in reviews]), "]", file=file
            )
    else:
        print("No reviews found!")
