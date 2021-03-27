import os
import click
from terminaltables import AsciiTable

from .. import MangaTracker
from .utils import (cvt_group_to_table,
                    cvt_target_to_table,
                    cvt_header_to_table,
                    cvt_idx_to_target,
                    cvt_output_to_table)

PROJECT_DIR = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
BOUNTY_DIR = os.path.join(os.path.join(PROJECT_DIR, 'params'), 'bounty.json')
RESULT_DIR = os.path.join(os.getcwd(), 'result')
COLUMNS = ['website', 'alias', 'title', 'ongoing', 'updated_at', 'latest_chapter', 'latest_chapter_link']
DELIMITER = '|'

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
    Start web-crawling process with targets from bounty list.
    """
    groups = MangaTracker.init_job(BOUNTY_DIR, RESULT_DIR, COLUMNS, DELIMITER, silent)
    MangaTracker.crawl(groups, RESULT_DIR, COLUMNS, DELIMITER, silent)
    MangaTracker.end_job(RESULT_DIR, silent)

@cli.command('show-bounty')
def show_bounty():
    """
    Show all groups and targets in bounty list.
    """
    results = MangaTracker.show_bounty(BOUNTY_DIR)
    for group in results:
        website, targets = cvt_group_to_table(group)
        click.echo(website.table)
        click.echo(targets.table)
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
    Add target to bounty list.
    """
    meta = { k: kw[k] for k in ('website', 'alias') }
    result = MangaTracker.check_target(**meta, path=BOUNTY_DIR, duplicate=True)
    if (result[0] == -1):
        click.echo(result[1])
    else:
        preview_tbl = cvt_target_to_table(kw)
        click.echo(preview_tbl.table)
        if (click.confirm("Are these input correct?")):
            message = MangaTracker.add_target(*result, **kw, path=BOUNTY_DIR)
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
    result = MangaTracker.check_target(**kw, path=BOUNTY_DIR)
    if (result[0] == -1):
        click.echo(result[1])
    else:
        bl, gid, tid = result
        target = {
            'website': bl[gid]['website'],
            'alias': bl[gid]['targets'][tid][0],
            'link': bl[gid]['targets'][tid][1]
        }
        preview_tbl = cvt_target_to_table(target)
        click.echo(preview_tbl.table)

        if (click.confirm("Are these input correct?")):
            message = MangaTracker.remove_target(*result, path=BOUNTY_DIR)
            click.echo(message)

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
        click.echo("Both newalias and newlink can't be empty at the same time!")
        return

    meta = { k: kw[k] for k in ('website', 'alias') }
    result = MangaTracker.check_target(**meta, path=BOUNTY_DIR)
    if (result[0] == -1):
        click.echo(result[1])
    else:
        old_target = cvt_idx_to_target(*result)
        preview_old_tbl = cvt_target_to_table(old_target)
        click.echo(cvt_header_to_table('Old Target').table)
        click.echo(preview_old_tbl.table)
        click.echo('')

        new_target = {k: kw[k] for k in ('website', 'newalias', 'newlink')}
        preview_new_tbl = cvt_target_to_table(new_target, new=True)
        click.echo(cvt_header_to_table('New Target').table)
        click.echo(preview_new_tbl.table)

        if (click.confirm("Are you sure want to change old target into new target?")):
            meta = {
                'website': new_target['website'],
                'alias': new_target['newalias']
            }
            check = MangaTracker.check_target(**meta, path=BOUNTY_DIR, duplicate=True)
            if (check[0] == -1):
                message = check[1]
            else:
                message = MangaTracker.update_target(*result, **new_target, path=BOUNTY_DIR)
            click.echo(message)

@cli.command('show-log')
def show_log():
    """
    Get job's logs.
    """
    logs = MangaTracker.show_log(RESULT_DIR)
    click.echo(logs)

@cli.command('show-output')
def show_output():
    """
    Show full crawling output in table format.
    """
    output = MangaTracker.show_output(RESULT_DIR, DELIMITER)
    click.echo(cvt_output_to_table(output).table)

@cli.command('result')
def result():
    """
    Show crawling result summary.
    """
    result = MangaTracker.result(RESULT_DIR, DELIMITER)
    meta = MangaTracker.extract_meta(RESULT_DIR)
    tcount = int(meta['counter'][0])
    scount = int(meta['success'])
    report = (f"{'Job ID':12}: {meta['job_id']}\n"
              f"{'Start Time':12}: {meta['start_time']}\n"
              f"{'End Time':12}: {meta['end_time']}\n"
              f"{'Bounty Path':12}: {meta['bounty_path']}\n"
              f"{'Result Path':12}: {meta['result_path']}\n"
              f"{'Counter':12}: {meta['counter']}\n"
              f"{'Success':12}: {scount} ({(tcount/scount)*100:.0f}%)\n")
    click.echo(report)
    click.echo(cvt_output_to_table(result).table)

if __name__ == '__main__':
    cli()
