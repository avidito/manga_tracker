import requests
from bs4 import BeautifulSoup
from datetime import datetime

from .bounty import BountyHandler
from .database import DatabaseEngine
from .log import Logger

class MangaTracker:
    """
    Web-Scraping Main Engine.
    """

    @staticmethod
    def _preproccess(data):
        """
        Preprocessing scraped data.
        """
        data['ongoing'] = 1 if (data['ongoing'].lower() == 'ongoing') else  0
        data['updated_at'] = datetime.strptime(data['updated_at'], '%b %d,%Y - %H:%M %p').strftime('%d-%m-%Y %H:%M')
        return data

    @staticmethod
    def _scrape(url):
        """
        Scraping proccess.
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
            'authors': [author.text for author in info_table[1].find_all('td')[1].find_all('a')],
            'ongoing': info_table[2].find_all('td')[1].text,
            'genres': [genre.text for genre in info_table[3].find_all('td')[1].find_all('a')],
            'updated_at': info_extent[0].find_all('span')[1].text,
            'latest_chapter': info_extent[3].find_all('span')[1].a.text,
            'latest_chapter_link': info_extent[3].find_all('span')[1].a['href'],
        }

        # Preprocess data
        data = MangaTracker._preproccess(extracted)
        return data, req.status_code

    @staticmethod
    def _load(title, data, response, log, db):
        """
        Load data to database and log.
        """
        log.log_scrape(title, response)
        db.load_data(title, log.job_id, data)

    @staticmethod
    def _end_job(log):
        """
        Logging data
        """
        log.log_end()

    @staticmethod
    def init_job(log_path='logs', bounty_path='bounty.json', db_path='outputs'):
        """
        Initiate job by reading bounty and define job metadata.
        """
        log = Logger(log_path)
        db = DatabaseEngine(db_path)

        # Initiate metadata
        job_id = log.log_start()
        groups = BountyHandler._read_bounty(bounty_path)
        db.init_db(job_id)
        handler = {
            'log': log,
            'db': db,
            'groups': groups
        }
        return handler

    @staticmethod
    def crawl(groups, log, db):
        """
        Run the web-crawling process.
        """
        # Start crawling
        for group in groups:
            website = group['website']
            targets = group['targets']
            for (title, url) in targets:
                data, response = MangaTracker._scrape(url)
                MangaTracker._load(title, data, response, log, db)

        # End job
        log.log_end()
        log.show_log()

# Bounty Handler
MangaTracker.show_bounty = staticmethod(lambda: BountyHandler.show_bounty())
MangaTracker.add_target = staticmethod(lambda kw: BountyHandler.add_target(**kw))
