from datetime import datetime

class LogHandler:
    """
    Module to Read, Load, and Represent Job Logs
    """
    @staticmethod
    def _dtlog(msg):
        """
        Embed Log Time to Message
        """
        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        return "[{}] {}\n".format(now, msg)

    @staticmethod
    def log_start(path):
        """
        Create start of job log.
        """
        # Init Job Id
        dt_start_time = datetime.now()
        job_id = dt_start_time.strftime("%Y%m%d%H%M")
        LogHandler.logging(path, 'Job Id: {}'.format(job_id), mode='w')

        # Log Start Time
        start_time = dt_start_time.strftime('%d/%m/%Y %H:%M:%S')
        LogHandler.logging(path, 'Start Time: {}'.format(start_time))

        return job_id

    @staticmethod
    def logging(path, msg, mode='a'):
        """
        Create initiation activity log.
        """
        with open('{}.txt'.format(path), mode) as f:
            f.write(LogHandler._dtlog(msg))

    @staticmethod
    def log_scrape(path, title, response):
        """
        Create scraping log.
        """
        LogHandler.logging(path, '{} - Response: {}'.format(title, response))

    @staticmethod
    def log_end(path):
        """
        Create end of job log.
        """
        end_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        LogHandler.logging(path, 'End Time: {}\n'.format(end_time))

    def show_log(self, job_id=None):
        """
        Get log from corresponding job.
        """
        job_id = job_id if (job_id) else self.job_id

        # Get Log
        with open('{}\{}.txt'.format(self.path, job_id), 'r') as f:
            log = f.read()
        print(log)
