import requests
from bs4 import BeautifulSoup
from datetime import datetime
from os import mkdir
import time

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
        Preprocessed data.

        Parameters
        ----------
            data        : dict. Raw input data that needed to be processed.

        Returns
        -------
            processed   : dict. Proccesed data from preprocessing input data.
        """
        ['website', 'alias', 'title', 'ongoing', 'updated_at', 'latest_chapter', 'latest_chapter_link']
        _pr = {
            'website': lambda x: x,
            'alias': lambda x: x,
            'title': lambda x: x,
            'ongoing': lambda x: 1 if (x.lower() == 'ongoing') else  0,
            'updated_at': lambda x: datetime.strptime(x, '%b %d,%Y - %H:%M %p').strftime('%d-%m-%Y %H:%M'),
            'latest_chapter': lambda x: x,
            'latest_chapter_link': lambda x: x,
        }
        processed = { k: _pr[k](data[k]) for k in data.keys()}
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
    def _load(path, website, alias, response, data, columns, delimiter, silent):
        """
        Load data to output and log file.

        Parameters
        ----------
            path        : str. Pathname for output and log directory.
            website     : str. Website's name of scraped data.
            alias       : str. Manga's alias of scraped data.
            response    : int. Request status code while trying to get web page.
            data        : dict. Extracted data from web scraping in dictionary format.
            delimiter   : str. Data delimiter in output file.
            silent      : boolean. Flag to silence progress messages.
        """
        LogHandler.log_scrape(path, alias, response, silent)
        OutputHandler.load_data(path, website, alias, data, columns, delimiter)

    # Public Method
    @staticmethod
    def init_job(bounty_path, result_path, columns, delimiter, silent=False):
        """
        Initiate job by reading bounty and define job metadata.

        Parameters
        ----------
            bounty_path : str. Pathname for bounty file (with extension).
            result_path : str. Pathname for output and log directory.
            columns     : list. List of columns name for output table.
            delimiter   : str. Delimiter for separating data.
            silent      : boolean (default=False). Flag to silence progress messages.
        Returns
        -------
            groups      : list. List of extracted bounty target list.
        """
        # Create folder if not exist
        try:
            mkdir(result_path)
        except FileExistsError:
            pass

        # Initiate job
        LogHandler.log_start(result_path, silent)

        groups = BountyHandler.read_bounty(bounty_path)
        w_count = sum([1 for group in groups])
        t_count = sum([1 for group in groups for target in group['targets']])
        LogHandler.logging(path=result_path, silent=silent,
                    message=f'[Init] Target aquired from bounty file from "{bounty_path}". {t_count} target(s) from {w_count} website(s)')

        OutputHandler.init_output(result_path, columns, delimiter)
        LogHandler.logging(path=result_path, silent=silent,
                    message=f'[Init] Output file successfully created at "{result_path}"')

        return groups

    @staticmethod
    def crawl(groups, result_path, columns, delimiter, silent):
        """
        Run the web-crawling process.

        Parameters
        ----------
            groups      : list. List of groups (website) and its Manga targets information.
            result_path : str. Relative pathname for output and log directory.
            columns     : list. List of columns name for output table.
            delimiter   : str. Delimiter for separating data.
            silent      : boolean (default=False). Flag to silence progress messages.
        """
        for group in groups:
            website = group['website']
            targets = group['targets']
            for (title, url) in targets:
                data, response = MangaTracker._scrape(url)
                MangaTracker._load(result_path, website, title, response, data, columns, delimiter, silent)
                time.sleep(10)
                
    @staticmethod
    def end_job(result_path, silent):
        """
        Logging job's end time.

        Parameters
        ----------
            result_path : str. Pathname for output and log directory.
            silent      : boolean (default=False). Flag to silence progress messages.
        """
        LogHandler.log_end(result_path, silent)

# Handler Utilization
MangaTracker.show_bounty = staticmethod(BountyHandler.show_bounty)
MangaTracker.check_target = staticmethod(BountyHandler.check_target)
MangaTracker.add_target = staticmethod(BountyHandler.add_target)
MangaTracker.remove_target = staticmethod(BountyHandler.remove_target)
MangaTracker.update_target = staticmethod(BountyHandler.update_target)
MangaTracker.show_log = staticmethod(LogHandler.show_log)
MangaTracker.show_output = staticmethod(OutputHandler.show_output)
MangaTracker.result = staticmethod(OutputHandler.result)
MangaTracker.extract_meta = staticmethod(LogHandler.extract_meta)
