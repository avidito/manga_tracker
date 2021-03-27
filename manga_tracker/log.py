from datetime import datetime

class LogHandler:
    """
    [Static Class] Handler to create and show job logs.
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
        message = f"[{now}] {message}"
        return message

    @staticmethod
    def logging(path, message, silent, mode='a'):
        """
        Create initiation activity or process log.

        Paramaters
        ----------
            path    : str. Pathname for log file directory (result directory).
            message : str. Message for successfull activity or process attempt.
            silent  : boolean (default=False). Flag to silence progress messages.
            mode    : str (default='a'). File opening mode.
        """
        log_path = f'{path}/logs.txt'
        with open(log_path, mode) as f:
            f.write(LogHandler._dtlog(message) + '\n')
        if (not silent):
            print(LogHandler._dtlog(message))

    @staticmethod
    def log_start(path, silent):
        """
        Create start of job log.

        Parameters
        ----------
            path    : str. Pathname for log file directory (result directory).
            silent  : boolean. Flag to silence progress messages.
        """
        # Init Job Id
        dt_start_time = datetime.now()
        job_id = dt_start_time.strftime("%Y%m%d%H%M")
        LogHandler.logging(path, f'[Job] Starting Job. Job Id: {job_id}', silent, mode='w')

        # Log Start Time
        start_time = dt_start_time.strftime('%d/%m/%Y %H:%M:%S')
        LogHandler.logging(path, f'[Job] Start Time: {start_time}', silent)

    @staticmethod
    def log_scrape(path, alias, response, silent):
        """
        Create scraping log.

        Parameters
        ----------
            path    : str. Pathname for log file directory (result directory).
            alias   : str. New manga title (or alias) to be inputted.
            response: int. Request status code while trying to get web page.
            silent  : boolean. Flag to silence progress messages.
        """
        LogHandler.logging(path, f'[Scraping] {alias} - Response: {response}', silent)

    @staticmethod
    def log_end(path, silent):
        """
        Create end of job log.

        Parameters
        ----------
            path    : str. Relative pathname for log file directory (result directory).
        """
        end_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        LogHandler.logging(path, f'[Job] End Time: {end_time}', silent)

    @staticmethod
    def show_log(path):
        """
        Get log from latest job.

        Parameters
        ----------
            path    : str. Pathname for log file directory (result directory).

        Returns
        -------
            logs    : str. Log file in string format.
        """
        log_path = f'{path}/logs.txt'
        with open(log_path, 'r') as f:
            logs = f.read()
        return logs

    @staticmethod
    def extract_meta(path):
        """
        Extracting meta information about latest job from log file.

        Parameters
        ----------
            path    : str. Relative pathname for log file directory (result directory).

        Returns
        -------
            meta    : dict. Meta information in dictionary format.
        """
        logs = LogHandler.show_log(path).split('\n')
        meta = {
            'job_id': logs[0][-12:],
            'start_time': logs[1][-19:],
            'end_time': logs[-2][-19:],
            'bounty_path': logs[2].split('"')[1],
            'result_path': logs[3].split('"')[1],
            'counter': logs[2].split('.')[-1].strip(),
            'success': sum([1 if (row[-3:] == '200') else 0 for row in logs])
        }
        return meta
