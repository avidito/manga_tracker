from datetime import datetime

class LogHandler:
    """
    Handler to create and show job logs.
    """
    @staticmethod
    def _dtlog(message):
        """
        Embed Log Time to Message.

        Parameters
        ----------
            message : str. Message that need to be embedded.

        Returns
        -------
            message : str. Formatted message.
        """
        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        return "[{}] {}\n".format(now, message)

    @staticmethod
    def log_start(path):
        """
        Create start of job log.

        Parameters
        ----------
            path    : str. Pathname for log file (please insert fullpath to filename).

        Returns
        -------
            job_id  : int. Job Id for new initiated job.
        """
        # Init Job Id
        dt_start_time = datetime.now()
        job_id = dt_start_time.strftime("%Y%m%d%H%M")
        LogHandler.logging(path, '[Job] Starting Job. Job Id: {}'.format(job_id), mode='w')

        # Log Start Time
        start_time = dt_start_time.strftime('%d/%m/%Y %H:%M:%S')
        LogHandler.logging(path, '[Job] Start Time: {}'.format(start_time))

        return job_id

    @staticmethod
    def logging(path, message, mode='a'):
        """
        Create initiation activity or process log.

        Paramaters
        ----------
            path    : str. Pathname for log file (please insert fullpath to filename).
            message : str. Message for successfull activity or process attempt.
            mode    : str (default='a'). File opening mode.
        """
        with open('{}.txt'.format(path), mode) as f:
            f.write(LogHandler._dtlog(message))

    @staticmethod
    def log_scrape(path, alias, response):
        """
        Create scraping log.

        Parameters
        ----------
            path    : str. Pathname for log file (please insert fullpath to filename).
            alias   : str. New manga title (or alias) to be inputted.
            response: int. Request status code while trying to get web page.
        """
        LogHandler.logging(path, '[Scraping] {} - Response: {}'.format(title, response))

    @staticmethod
    def log_end(path):
        """
        Create end of job log.

        Parameters
        ----------
        path    : str. Pathname for log file (please insert fullpath to filename).
        """
        end_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        LogHandler.logging(path, '[Job] End Time: {}\n'.format(end_time))

    @staticmethod
    def show_log(path='logs'):
        """
        Get log from corresponding job.

        Parameters
        ----------
        path    : str (default='logs'). Pathname for log file (please insert fullpath to filename).
        """
        with open('{}.txt'.format(path), 'r') as f:
            log = f.read()
        print(log, end='')
