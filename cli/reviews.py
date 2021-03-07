import os
import sys
from rx import operators as ops

import click

import stores
from stores.app_store.app import App
from stores.google_play.parsing_functions import reviews as play_reviews
from stores import country_codes

code_choices = [key for key in country_codes.keys()]


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
    validate_output(output)
    reviews = play_reviews(app_id, country_code)

    if len(reviews) > 0:
        with open(output, "w") if output is not None else sys.stdout as file_handle:
            print(
                "[",
                ",".join([review.to_json() for review in reviews]),
                "]",
                file=file_handle,
            )
    else:
        print("No reviews found!")


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
    validate_output(output)
    app = App(app_id, country_code)
    with open(output, "w") if output is not None else sys.stdout as file_handle:
        print("[", file=file_handle)
        container = []
        app.reviews.pipe(ops.map(lambda review: review.to_json())).subscribe(
            on_next=lambda review: container.append(review),
            on_completed=lambda: print(
                ",".join([review for review in container]), "]", file=file_handle
            ),
        )


def validate_output(output):
    if output is not None and os.path.isfile(output) and os.stat(output).st_size > 0:
        raise click.BadOptionUsage("output", "destination file is not empty!")
