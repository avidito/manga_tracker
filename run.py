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
    MangaTracker.end_job()

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

@cli.command('update-target')
@click.option('--website', '-w')
@click.option('--alias', '-a')
@click.option('--newalias', '-na')
@click.option('--newlink', '-nl')
def update_target(**kw):
    """
    Update existing target in bounty list.
    """
    message = MangaTracker.update_target(kw)
    print(message)

@cli.command('show-log')
def show_log():
    """
    Get log from corresponding job.
    """
    MangaTracker.show_log()

@cli.command('show-output')
def show_output():
    """
    Show full crawling result in table format.
    """
    MangaTracker.show_output()

@cli.command('result')
def result():
    """
    Show crawling result summary.
    """
    MangaTracker.result()


if __name__ == '__main__':
    cli()
