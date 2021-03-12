import requests
from bs4 import BeautifulSoup
from datetime import datetime

from .bounty import BountyHandler
from .log import LogHandler
from .database import DatabaseEngine

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
    def _load(title, response, data, log_path, job_id, db):
        """
        Load data to database and log.
        """
        LogHandler.log_scrape(log_path, title, response)
        db.load_data(title, job_id, data)

    @staticmethod
    def init_job(log_path='logs', bounty_path='bounty.json', db_path='outputs'):
        """
        Initiate job by reading bounty and define job metadata.
        """
        job_id = LogHandler.log_start(log_path)
        groups = BountyHandler._read_bounty(bounty_path)
        LogHandler.logging(log_path, 'Target aquired from bounty file. X target(s).')

        db = DatabaseEngine(db_path)
        db.init_db(job_id)
        LogHandler.logging(log_path, 'Database connection successfully created.')

        handler = {
            'db': db,
            'groups': groups,
            'job_id': job_id,
            'log_path': log_path
        }
        return handler

    @staticmethod
    def crawl(db, groups, job_id, log_path):
        """
        Run the web-crawling process.
        """
        for group in groups:
            website = group['website']
            targets = group['targets']
            for (title, url) in targets:
                data, response = MangaTracker._scrape(url)
                MangaTracker._load(title, response, data, log_path, job_id, db)

    @staticmethod
    def end_job(log_path='logs'):
        """
        End job.
        """
        LogHandler.log_end(log_path)

# Bounty Handler
MangaTracker.show_bounty = staticmethod(lambda: BountyHandler.show_bounty())
MangaTracker.add_target = staticmethod(lambda kw: BountyHandler.add_target(**kw))
MangaTracker.remove_target = staticmethod(lambda kw: BountyHandler.remove_target(**kw))
MangaTracker.update_target = staticmethod(lambda kw: BountyHandler.update_target(**kw))
