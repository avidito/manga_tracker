import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

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
    def _load(path, alias, response, data, silent):
        """
        Load data to database and log.

        Parameters
        ----------
            path    : str. Relative pathname for output and log directory.
            alias   : str. Defined manga alias for output and log result.
            response: int. Request status code while trying to get web page.
            data    : dict. Extracted data from web scraping in dictionary format.
            silent  : boolean (default=False). Flag to silence progress messages.
        """
        LogHandler.log_scrape(path, alias, response, silent)
        OutputHandler.load_data(path, alias, data)

    # Public Method
    @staticmethod
    def init_job(bounty_path, result_path, silent=False):
        """
        Initiate job by reading bounty and define job metadata.

        Parameters
        ----------
            bounty_path : str. Pathname for bounty file (with extension).
            result_path : str (default='result'). Relative pathname for output and log directory.
            silent      : boolean (default=False). Flag to silence progress messages.
        Returns
        -------
            groups      : list. List of extracted bounty target list.
        """
        # Create folder if not exist
        try:
            os.mkdir(result_path)
        except FileExistsError:
            pass

        # Initiate job
        LogHandler.log_start(result_path, silent)

        groups = BountyHandler.read_bounty(bounty_path)
        LogHandler.logging(result_path, '[Init] Target aquired from bounty file. X target(s).', silent)

        OutputHandler.init_output(result_path)
        LogHandler.logging(result_path, '[Init] Output file successfully created.', silent)

        return groups

    @staticmethod
    def crawl(groups, result_path, silent):
        """
        Run the web-crawling process.

        Parameters
        ----------
            groups      : list. List of groups (website) and its Manga targets information.
            result_path : str. Relative pathname for output and log directory.
            silent      : boolean (default=False). Flag to silence progress messages.
        """
        for group in groups:
            website = group['website']
            targets = group['targets']
            for (title, url) in targets:
                data, response = MangaTracker._scrape(url)
                MangaTracker._load(result_path, title, response, data, silent)

    @staticmethod
    def end_job(result_path, silent):
        """
        Logging job's end time and show report.

        Parameters
        ----------
            result_path : str. Relative pathname for output and log directory.
            silent      : boolean (default=False). Flag to silence progress messages.
        """
        LogHandler.log_end(result_path, silent)

# Handler Utilization
MangaTracker.show_bounty = staticmethod(BountyHandler.show_bounty)
MangaTracker.add_target = staticmethod(BountyHandler.add_target)
MangaTracker.remove_target = staticmethod(BountyHandler.remove_target)
MangaTracker.update_target = staticmethod(BountyHandler.update_target)
MangaTracker.show_log = staticmethod(LogHandler.show_log)
MangaTracker.show_output = staticmethod(OutputHandler.show_output)
MangaTracker.result = staticmethod(OutputHandler.result)
