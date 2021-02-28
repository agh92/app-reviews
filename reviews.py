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
@click.option('-id', '--app-id', 'appId', required=True, type=int)
@click.option('-cc', '--country-code', 'countryCode', required=True, type=click.Choice(code_choises))
@click.option('-o', '--output', 'output', required=False, type=click.Path())
def google(appId, countryCode, output):
    revs = play_reviews(appId, countryCode)
    # TODO remove print revs method and just write to std-out
    if not output:
        print_revs(revs)
    else:
        save(revs, output)


@cli.command()
@click.option('-id', '--app-id', 'appId', required=True, type=str)
@click.option('-cc', '--country-code', 'countryCode', required=True, type=click.Choice(code_choises))
@click.option('-o', '--output', 'output', required=False, type=click.Path())
def apple(appId, countryCode, output):
    revs = apple_reviews(appId, countryCode)
    if len(revs) == 0:
        print('No reviews found!')
        return
    # TODO remove print revs method and just write to std-out
    if output is None:
        print_revs(revs)
    else:
        save(revs, output)


def print_revs(reviews):
    for review in reviews:
        print(review.to_json())


def save(reviews, output: click.Path):
    destination = get_destination(output)
    write(reviews, destination)


def get_destination(output: click.Path):
    if output.path_type == 'file':
        return handle_file(output)
    else:
        # TODO use appId as path name create file
        print('Create file in ' + output.name)


def handle_file(output: click.Path):
    if output.exists:
        if os.stat(output.path).st_size > 0:
            raise click.BadOptionUsage(
                'output', 'destination file is not empty!')
        if output.writable is not True:
            raise click.BadOptionUsage(
                'output', 'destination file is not writable!')
    return open(output.name, 'w')


def write(reviews, output):
    # TODO implement writing
    print('Write!')
    print_revs(reviews)
