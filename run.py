import click

# Basic OOP Format
from manga_tracker.log import Logger
from manga_tracker.bounty import BountyHandler
from manga_tracker.database import DatabaseEngine

# OOP CLI format
from manga_tracker import MangaTracker

@click.group()
def cli():
    pass

@cli.command('crawl')
def crawl():
    handler = MangaTracker.init_job()
    MangaTracker.crawl(**handler)

if __name__ == '__main__':
    cli()
