from datetime import datetime

class Logger:
    """
    Module to Read, Load, and Represent Job Logs
    """
    def __init__(self, path):
        self.path = path
        self.column = ['alias', 'title', 'authors', 'ongoing', 'genres', 'updated_at', 'latest_chapter', 'latest_chapter_link']

    def _generate_report(self):
        """
        Generate log to report format.
        """
        report = ''
        report += 'Job ID: {}\n'.format(self.job_id)
        report += 'Start Time: {}\n'.format(self.start_time)
        report += 'End Time: {}\n'.format(self.end_time)

        report += 'Link Crawled:\n'
        for link in self.link_crawled:
            report += "\t - {} | {} | {}\n".format(*link)

        return report

    def log_start(self):
        """
        Initiate log record.
        """
        dt_start_time = datetime.now()
        self.job_id = dt_start_time.strftime("%Y%m%d%H%M")
        self.start_time = dt_start_time.strftime('%d/%m/%Y %H:%M:%S')
        self.link_crawled = []

        return self.job_id

    def log_scrape(self, title, response):
        """
        Insert scraping record.
        """
        time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.link_crawled.append((title, response, time))

    def log_end(self):
        """
        Closing log record
        """
        # Set End Time
        dt_end_time = datetime.now()
        self.end_time = dt_end_time.strftime('%d/%m/%Y %H:%M:%S')

        # Load log report
        report = self._generate_report()
        with open('{}\{}.txt'.format(self.path, self.job_id), 'w') as f:
            f.write(report)

    def show_log(self, job_id=None):
        """
        Get log from corresponding job.
        """
        job_id = job_id if (job_id) else self.job_id

        # Get Log
        with open('{}\{}.txt'.format(self.path, job_id), 'r') as f:
            log = f.read()
        print(log)
