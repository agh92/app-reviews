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
    print('Get GooglePlay ' + appId + ' for ' + countryCode)


@cli.command()
@click.option('-id', '--app-id', 'appId', required=True, type=str)
@click.option('-cc', '--country-code', 'countryCode', required=True, type=click.Choice(code_choises))
@click.option('-o', '--output', 'output', required=False, type=click.Path())
def apple(appId, countryCode, output):
    if stores.VERBOSE and not output:
        print('Get GooglePlay ' + appId + ' for ' + countryCode)

    revs = apple_reviews(appId, 'us')
    for review in revs:
        print(review.to_json())