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
        # TODO save to gile
        pass


@cli.command()
@click.option('-id', '--app-id', 'appId', required=True, type=str)
@click.option('-cc', '--country-code', 'countryCode', required=True, type=click.Choice(code_choises))
@click.option('-o', '--output', 'output', required=False, type=click.Path())
def apple(appId, countryCode, output):
    revs = apple_reviews(appId, countryCode)
    if not output:
        print_revs(revs)
    else:
        # TODO save to gile
        pass


def print_revs(reviews):
    for review in reviews:
        print(review.to_json())


def SaveToFile(reviews, file):
    pass