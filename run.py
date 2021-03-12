import click

# OOP CLI format
from manga_tracker import MangaTracker

@click.group()
def cli():
    """
    CLI Program to Track Updated Manga using Web-Scraping (bs4).
    """
    pass

@cli.command('crawl')
def crawl():
    """
    Start web-crawling process.
    """
    handler = MangaTracker.init_job()
    MangaTracker.crawl(**handler)

@cli.command('show-bounty')
def show_bounty():
    """
    Show all targets in bounty list.
    """
    result = MangaTracker.show_bounty()
    print(result)

@cli.command('add-target')
@click.option('--website', '-w')
@click.option('--alias', '-a')
@click.option('--link', '-l')
def add_target(**kw):
    """
    Add target to bounty list.
    """
    message = MangaTracker.add_target(kw)
    print(message)

@cli.command('remove-target')
@click.option('--website', '-w')
@click.option('--alias', '-a')
def remove_target(**kw):
    """
    Remove target from bounty list.
    """
    message = MangaTracker.remove_target(kw)
    print(message)


if __name__ == '__main__':
    cli()
