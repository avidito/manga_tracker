import requests
from bs4 import BeautifulSoup
from datetime import datetime

from .bounty import BountyHandler
from .log import LogHandler
from .output import OutputHandler

class MangaTracker:
    """
    [Static Class] Main interface to manga web crawling job.
    """

    @staticmethod
    def _preproccess(data):
        """
        Return preprocessed data.

        Parameters
        ----------
            data        : dict. Raw input data that needed to be processed.

        Returns
        -------
            processed   : dict. Proccesed data from preprocessing input data.
        """
        processed = data.copy()
        processed['ongoing'] = 1 if (processed['ongoing'].lower() == 'ongoing') else  0
        processed['updated_at'] = datetime.strptime(processed['updated_at'], '%b %d,%Y - %H:%M %p').strftime('%d-%m-%Y %H:%M')
        return processed

    @staticmethod
    def _scrape(url):
        """
        Start scraping page with inputted URL.

        Parameters
        ----------
            url     : str. Manga (target) main page URL.

        Returns
        -------
            data    : dict. Extracted data from web scraping in dictionary format.
            response: int. Request status code while trying to get web page.
        """
        # Get and parse page
        req = requests.get(url)
        page = BeautifulSoup(req.content, 'html.parser')

        # Extract block of data
        info_panel = page.find('div', class_="story-info-right")
        info_table = info_panel.table.tbody.find_all('tr')
        info_extent = info_panel.div.find_all("p")

        # Extract information
        extracted = {
            'title': info_panel.h1.text,
            'ongoing': info_table[2].find_all('td')[1].text,
            'updated_at': info_extent[0].find_all('span')[1].text,
            'latest_chapter': info_extent[3].find_all('span')[1].a.text,
            'latest_chapter_link': info_extent[3].find_all('span')[1].a['href'],
        }

        # Preprocess data
        data = MangaTracker._preproccess(extracted)
        return data, req.status_code

    @staticmethod
    def _load(alias, response, data, log_path, out_path):
        """
        Load data to database and log.

        Parameters
        ----------
            alias   : str. Defined manga alias for output and log result.
            response: int. Request status code while trying to get web page.
            data    : dict. Extracted data from web scraping in dictionary format.
            log_path: str. Pathname for log file (please insert fullpath to filename).
            out_path: str. Pathname for output file (please insert fullpath to filename).
        """
        LogHandler.log_scrape(log_path, alias, response)
        OutputHandler.load_data(out_path, alias, data)

    # Public Method
    @staticmethod
    def init_job(bounty_path='bounty.json', log_path='logs', out_path='outputs'):
        """
        Initiate job by reading bounty and define job metadata.

        Parameters
        ----------
            bounty_path : str (default='bounty.json'). Pathname for bounty file (please insert fullpath to filename and extension).
            log_path    : str (default='logs'). Pathname for log file (please insert fullpath to filename).
            out_path    : str (default='outputs'). Pathname for output file (please insert fullpath to filename).

        Returns
        -------
            meta        : dict. Dictionary of job metadata and extracted bounty target list.
        """
        LogHandler.log_start(log_path)

        groups = BountyHandler._read_bounty(bounty_path)
        LogHandler.logging(log_path, '[Init] Target aquired from bounty file. X target(s).')

        OutputHandler.init_output(out_path)
        LogHandler.logging(log_path, '[Init] Output file successfully created.')

        meta = {
            'groups': groups,
            'log_path': log_path,
            'out_path': out_path
        }
        return meta

    @staticmethod
    def crawl(groups, log_path, out_path):
        """
        Run the web-crawling process.

        Parameters
        ----------
            groups  : list. List of groups (website) and its Manga targets information.
            log_path: str. Pathname for log file (please insert fullpath to filename).
            out_path: str. Pathname for output file (please insert fullpath to filename).
        """
        for group in groups:
            website = group['website']
            targets = group['targets']
            for (title, url) in targets:
                data, response = MangaTracker._scrape(url)
                MangaTracker._load(title, response, data, log_path, out_path)

    @staticmethod
    def end_job(log_path='logs'):
        """
        End job.

        Parameters
        ----------
            log_path: str (default='logs'). Pathname for log file (please insert fullpath to filename).
        """
        LogHandler.log_end(log_path)

# Handler Utilization
MangaTracker.show_bounty = staticmethod(lambda: BountyHandler.show_bounty())
MangaTracker.add_target = staticmethod(lambda kw: BountyHandler.add_target(**kw))
MangaTracker.remove_target = staticmethod(lambda kw: BountyHandler.remove_target(**kw))
MangaTracker.update_target = staticmethod(lambda kw: BountyHandler.update_target(**kw))
MangaTracker.show_log = staticmethod(lambda: LogHandler.show_log())
MangaTracker.show_output = staticmethod(lambda: OutputHandler.show_output())
MangaTracker.result = staticmethod(lambda: OutputHandler.result())
