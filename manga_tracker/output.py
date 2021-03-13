import pandas as pd

class OutputHandler:
    """
    Bridge from Web Crawler to Database
    """
    @staticmethod
    def init_output(path, job_id, delimiter='|', columns=['alias', 'title', 'authors', 'ongoing', 'genres', 'updated_at', 'latest_chapter', 'latest_chapter_link']):
        """
        Initiate output file.
        """
        with open('{}\{}.txt'.format(path, job_id), 'w') as f:
            f.write(delimiter.join(columns) + '\n')

    @staticmethod
    def load_data(out_path, alias, job_id, data, columns=['alias', 'title', 'authors', 'ongoing', 'genres', 'updated_at', 'latest_chapter', 'latest_chapter_link']):
        """
        Convert data to row format and load to database
        """
        # Transform data to row format
        trans_data = ''
        for col in columns[1:]:
            trans_data += '|{}'.format(data[col])
        row = alias + trans_data

        # Load to database
        with open('{}\{}.txt'.format(out_path, job_id), 'a', encoding="utf-8") as f:
            f.write(row + '\n')

    def show_result(self, job_id, columns=['alias', 'latest_chapter', 'updated_at']):
        """
        Get result from corresponding job.
        """
        result = pd.read_csv('{}\{}.txt'.format(self.path, job_id), delimiter='|')[columns]
        print(result)
