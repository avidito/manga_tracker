import click
from manga_tracker import MangaTracker

@click.group()
@click.version_option(version='1.0', prog_name='mantrack')
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
    meta = MangaTracker.init_job()
    MangaTracker.crawl(**meta)
    MangaTracker.end_job()

@cli.command('show-bounty')
def show_bounty():
    """
    Show all targets in bounty list.
    """
    result = MangaTracker.show_bounty()
    print(result)

@cli.command('add-target')
@click.option('--website', '-w',
                help="Target's website group.",
                prompt="Website")
@click.option('--alias', '-a',
                help="Target's alias (or title).",
                prompt="Manga Name (or Alias)")
@click.option('--link', '-l',
                help="Target's page URL.",
                prompt="Manga Page URL")
def add_target(**kw):
    """
    Add target to bounty list.
    """
    message = MangaTracker.add_target(kw)
    print(message)

@cli.command('remove-target')
@click.option('--website', '-w',
                help="Target's website group.",
                prompt="Website")
@click.option('--alias', '-a',
                help="Target's alias (or title).",
                prompt="Manga Name (or Alias)")
def remove_target(**kw):
    """
    Remove target from bounty list.
    """
    message = MangaTracker.remove_target(kw)
    print(message)

@cli.command('update-target')
@click.option('--website', '-w',
                help="Target's website group.",
                prompt="Website")
@click.option('--alias', '-a',
                help="Target's alias (or title).",
                prompt="Manga Name (or Alias)")
@click.option('--newalias', '-na',
                default='',
                help="Target's new alias (or title).",
                prompt="New Manga Name (or Alias)")
@click.option('--newlink', '-nl',
                default='',
                help="Target's new page URL.",
                prompt="New Manga Page URL")
def update_target(**kw):
    """
    Update existing target in bounty list.
    """
    if ((kw.get('newalias') == '') and (kw.get('newlink') == '')):
        print("Both newalias and newlink can't be empty at the same time!")
        return
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
