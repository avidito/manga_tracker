import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json

class MangaTracker:
    def __init__(self, bounty='bounty.json', output='outputs', log='logs'):
        self.bou_path = bounty
        self.out_path = output
        self.log_path = log
        self.meta = {}

    def _get_bounty(self):
        """
        Read and parse target list from bounties.json.
        """
        with open(self.bou_path, 'r') as f:
            bounty = json.loads(f.read())
        return bounty['targets']

    def _init_job(self):
        """
        Initiate job metadata and output file.
        """
        # Init metadata
        dt_start_time = datetime.now()
        self.meta['start_time'] = dt_start_time.strftime('%d/%m/%Y %H:%M:%S')
        self.meta['job_id'] = dt_start_time.strftime("%Y%m%d%H%M")
        self.meta['website_crawled'] = 0
        self.meta['link_crawled'] = 0

        # Init output file
        self.meta['columns'] = ['alias', 'title', 'authors', 'ongoing', 'genres', 'updated_at', 'latest_chapter', 'latest_chapter_link']
        with open('{}\{}.txt'.format(self.out_path, self.meta['job_id']), 'w') as f:
            f.write('|'.join(self.meta['columns']) + '\n')

        return self.meta['job_id']

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
        self.meta['response_status'] = req.status_code
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
        return data

    def _load(self, title, data):
        """
        Load data to output file.
        """
        # Format data to row form
        trans_data = ""
        for col in self.meta['columns'][1:]:
            trans_data += '|{}'.format(data[col])
        row = title + trans_data

        # Load data
        with open('{}\{}.txt'.format(self.out_path, self.meta['job_id']), 'a', encoding="utf-8") as f:
            f.write(row + '\n')

        # Increase link crawled counter
        self.meta['link_crawled'] += 1

    def _logging(self):
        """
        Logging data
        """
        # Set End Time
        dt_end_time = datetime.now()
        self.meta['end_time'] = dt_end_time.strftime('%d/%m/%Y %H:%M:%S')

        # Create log report
        report = ''
        report += 'Job ID: {}\n'.format(self.meta['job_id'])
        report += 'Start Time: {}\n'.format(self.meta['start_time'])
        report += 'End Time: {}\n'.format(self.meta['end_time'])
        report += 'Response: {}\n'.format(self.meta['response_status'])
        report += 'Link Crawled: {}\n'.format(self.meta['link_crawled'])
        print(report)

        with open('{}\{}.txt'.format(self.log_path, self.meta['job_id']), 'w') as f:
            f.write(report)

    def start(self):
        """
        Run the web-scraping process.
        """
        # Job preparation
        self._init_job()
        targets = self._get_bounty()

        # Start scraping each target
        for target in targets:
            website = target['website']
            titles = target['titles']
            urls = target['urls']

        # Scrape each link
        for (title, url) in zip(titles, urls):
            data = self._scrape(url)
            self._load(title, data)

        # Loggin job
        self._logging()
