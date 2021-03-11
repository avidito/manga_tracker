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
    Start crawling process.
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
    MangaTracker.add_target(kw)

if __name__ == '__main__':
    cli()
