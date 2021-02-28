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
def google(appId, countryCode):
    revs = play_reviews(appId, countryCode)
    if not output:
        print_revs(revs)
    else:
        save(revs, path)


@cli.command()
@click.option('-id', '--app-id', 'appId', required=True, type=str)
@click.option('-cc', '--country-code', 'countryCode', required=True, type=click.Choice(code_choises))
@click.option('-o', '--output', 'output', required=False, type=click.Path())
def apple(appId, countryCode, output):
    revs = apple_reviews(appId, countryCode)
    # TODO remove print revs method and just write to std-out
    if not output:
        print_revs(revs)
    else:
        save(revs, path)


def print_revs(reviews):
    for review in reviews:
        print(review.to_json())


def save(reviews, path: click.Path):
    destination = get_destination(path)
    write(reviews, destination)


def get_destination(path: click.Path):
    if path.path_type == 'file':
        if path.exists:
            # TODO check if file is emty and use it if not emty throw error
            pass
    else:
        # TODO use appId as path name create file
        pass


def write(reviews, destination):
    pass
