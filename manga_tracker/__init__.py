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
    def __init__(self, bounty='bounty.json', output='outputs', log='logs'):
        self.bh = BountyHandler(bounty)
        self.db = DatabaseEngine(output)
        self.log = Logger(log)

    def _init_job(self):
        """
        Initiate job metadata and output file.
        """
        # Init log and database
        job_id = self.log.log_start()
        self.db.init_db(job_id)

        return job_id

    def _preproccess(self, data):
        """
        Preprocessing scraped data.
        """
        data['ongoing'] = 1 if (data['ongoing'].lower() == 'ongoing') else  0
        data['updated_at'] = datetime.strptime(data['updated_at'], '%b %d,%Y - %H:%M %p').strftime('%d-%m-%Y %H:%M')
        return data

    def _scrape(self, url):
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
        data = self._preproccess(extracted)
        return data, req.status_code

    def _load(self, title, data, response):
        """
        Load data to database and log.
        """
        self.db.load_data(title, self.log.job_id, data)
        self.log.log_scrape(title, response)

    def _end_job(self):
        """
        Logging data
        """
        self.log.log_end()

    def crawl(self):
        """
        Run the web-scraping process.
        """
        # Job initiation
        self._init_job()

        # Start scraping each target
        for bounty in self.bh.bounty['bounty']:
            website = bounty['website']
            targets = bounty['targets']

            # Scrape each link
            for (alias, url) in targets:
                data, response = self._scrape(url)
                self._load(alias, data, response)

        # Logging job
        self._end_job()
