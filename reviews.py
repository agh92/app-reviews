import os

import click

import stores
from stores.itunes_store import reviews as apple_reviews
from stores.google_play import reviews as play_reviews
from stores import code_choises


@click.group()
@click.option('-v', '--verbose', 'verbose', is_flag=True)
def cli(verbose):
    stores.VERBOSE = verbose


@cli.command()
@click.option('-id', '--app-id', 'appId', required=True, type=str)
@click.option('-cc', '--country-code', 'countryCode', required=True, type=click.Choice(code_choises))
@click.option('-o', '--output', 'output',
              required=False, type=click.Path(file_okay=True, dir_okay=False, writable=True, resolve_path=True))
def play(app_id, country_code, output):
    check_output(output)
    download_revs(app_id, country_code, play_reviews, output)


@cli.command()
@click.option('-id', '--app-id', 'appId', required=True, type=str)
@click.option('-cc', '--country-code', 'countryCode', required=True, type=click.Choice(code_choises))
@click.option('-o', '--output', 'output',
              required=False, type=click.Path(file_okay=True, dir_okay=False, writable=True, resolve_path=True))
def itunes(app_id, country_code, output):
    check_output(output)
    download_revs(app_id, country_code, apple_reviews, output)


def check_output(output):
    if output:
        if os.path.isfile(output) and os.stat(output).st_size > 0:
            raise click.BadOptionUsage(
                'output', 'destination file is not empty!')


def download_revs(app_id, country_code, download_function, output):
    revs = download_function(app_id, country_code)
    if len(revs) == 0:
        print('No reviews found!')
        return
    save(revs, output)


def save(reviews, output):
    if not output:
        print_revs(reviews)
        return
    write(reviews, output)


def print_revs(reviews):
    for review in reviews:
        print(review.to_json())


def write(reviews, output):
    with open(output, 'w') as file:
        file.write('[' + ','.join([review.to_json()
                                   for review in reviews]) + ']')
