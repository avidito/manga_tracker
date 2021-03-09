import pandas as pd

class DatabaseEngine:
    """
    Bridge from Web Crawler to Database
    """
    def __init__(self, path):
        self.path = path
        self.columns = ['alias', 'title', 'authors', 'ongoing', 'genres', 'updated_at', 'latest_chapter', 'latest_chapter_link']

    def init_db(self, job_id, delimiter='|'):
        """
        Initiate database (output file).
        """
        with open('{}\{}.txt'.format(self.path, job_id), 'w') as f:
            f.write(delimiter.join(self.columns) + '\n')

    def load_data(self, alias, job_id, data):
        """
        Convert data to row format and load to database
        """
        # Transform data to row format
        trans_data = ''
        for col in self.columns[1:]:
            trans_data += '|{}'.format(data[col])
        row = alias + trans_data

        # Load to database
        with open('{}\{}.txt'.format(self.path, job_id), 'a', encoding="utf-8") as f:
            f.write(row + '\n')

    def show_result(self, job_id, columns=['alias', 'latest_chapter', 'updated_at']):
        """
        Get result from corresponding job.
        """
        result = pd.read_csv('{}\{}.txt'.format(self.path, job_id), delimiter='|')[columns]
        print(result)
