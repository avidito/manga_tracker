import os
import click
from terminaltables import AsciiTable

from .. import MangaTracker

# Constant
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
BOUNTY_DIR = os.path.join(PROJECT_DIR, 'params/bounty.json')
RESULT_DIR = 'result'

@click.group()
@click.version_option(version='1.0')
def cli():
    """
    CLI Program to Track Updated Manga using Web-Scraping (bs4) with customizeable Manga Targets (Bounty) List.
    """
    pass

@cli.command('crawl')
@click.option('--silent', is_flag=True,
                help="Flag to silence progress messages.")
def crawl(silent):
    """
    Start web-crawling process.
    """
    groups = MangaTracker.init_job(BOUNTY_DIR, RESULT_DIR, silent)
    MangaTracker.crawl(groups, RESULT_DIR, silent)
    MangaTracker.end_job(RESULT_DIR, silent)

@cli.command('show-bounty')
def show_bounty():
    """
    Show all targets in bounty list.
    """
    header = ['Title', 'Link']
    results = MangaTracker.show_bounty(BOUNTY_DIR)
    for group in results:
        tbl_website = AsciiTable([['Website: ' + group[0]]])
        click.echo(tbl_website.table)
        tbl_targets = AsciiTable([header] + group[1:])
        click.echo(tbl_targets.table)
        click.echo('')

@cli.command('add-target')
@click.option('--website', '-w',
                help="Target's website group.",
                prompt="Website")
@click.option('--alias', '-a',
                help="Target's alias (or title).",
                prompt="Manga Name (or Alias)")
@click.option('--link', '-l',
                help="Target's page URL",
                prompt="Manga Page URL")
def add_target(**kw):
    """
    Confirm user input and Add target to bounty list.
    """
    # Preview user input
    keys = ['website', 'alias', 'link']
    values = [kw[key] for key in keys]
    columns = ["Website", "Alias", "URL"]
    preview = [[col, val] for col, val in zip(columns, values)]
    preview_tbl = AsciiTable([['Key', 'Value']] + preview)
    click.echo(preview_tbl.table)

    # Confirmation
    if (click.confirm("Are these input correct?")):
        message = MangaTracker.add_target(**kw, path=BOUNTY_DIR)
        click.echo(message)

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
    message = MangaTracker.remove_target(**kw, path=BOUNTY_DIR)
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
    message = MangaTracker.update_target(**kw, path=BOUNTY_DIR)
    print(message)

@cli.command('show-log')
def show_log():
    """
    Get log from corresponding job.
    """
    MangaTracker.show_log(RESULT_DIR)

@cli.command('show-output')
def show_output():
    """
    Show full crawling result in table format.
    """
    MangaTracker.show_output(RESULT_DIR)

@cli.command('result')
def result():
    """
    Show crawling result summary.
    """
    MangaTracker.result(RESULT_DIR)


if __name__ == '__main__':
    cli()
