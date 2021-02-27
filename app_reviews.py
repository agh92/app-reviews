import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('-id', '--app-id', 'appId')
@click.option('-cc', '--country-code', 'countryCode')
def google(appId, countryCode):
    print('Get GooglePlay ' + appId + ' for ' + countryCode)


@cli.command()
@click.option('-id', '--app-id', 'appId')
@click.option('-cc', '--country-code', 'countryCode')
def apple(appId, countryCode):
    print('Get GooglePlay ' + appId + ' for ' + countryCode)


if __name__ == '__main__':
    cli()
