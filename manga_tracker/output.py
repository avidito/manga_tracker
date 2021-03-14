from datetime import datetime, timedelta

class OutputHandler:
    """
    Handler to create and show job outputs.
    """
    @staticmethod
    def init_output(path, delimiter='|', columns=['alias', 'title', 'ongoing', 'updated_at', 'latest_chapter', 'latest_chapter_link']):
        """
        Initiate output file.
        """
        with open('{}.txt'.format(path), 'w') as f:
            f.write(delimiter.join(columns) + '\n')

    @staticmethod
    def load_data(out_path, alias, data, columns=['alias', 'title', 'ongoing', 'updated_at', 'latest_chapter', 'latest_chapter_link']):
        """
        Convert data to row format and load to database
        """
        # Transform data to row format
        trans_data = ''
        for col in columns[1:]:
            trans_data += '|{}'.format(data[col])
        row = alias + trans_data

        # Load to database
        with open('{}.txt'.format(out_path), 'a', encoding="utf-8") as f:
            f.write(row + '\n')

    @staticmethod
    def show_output(out_path='outputs', delimiter='|'):
        """
        Show full crawling result in table format.
        """
        with open('{}.txt'.format(out_path), 'r', encoding="utf-8") as f:
            raw = f.read()
        result = [row.split(delimiter) for row in raw.split('\n')]

        # Showing result
        print(*result[0], sep=' | ')
        print("-" * 50)
        for row in result[1:]:
            print(*row, sep=' | ')

    @staticmethod
    def result(out_path='outputs', delimiter='|'):
        """
        Show crawling result summary.
        """
        with open('{}.txt'.format(out_path), 'r', encoding="utf-8") as f:
            raw = f.read()
        result = [row.split(delimiter) for row in raw.strip().split('\n')]

        # Grouping by Update Time
        updated_today = []
        updated_last_7 = []
        updated_last_30 = []
        updated_older = []
        today_date = datetime.now().date()
        for row in result[1:]:
            date = datetime.strptime(row[3], '%d-%m-%Y %H:%M').date()
            if (date == today_date):
                updated_today.append(row)
            elif (date >= (today_date - timedelta(days=7))):
                updated_last_7.append(row)
            elif (date >= (today_date - timedelta(days=30))):
                updated_last_30.append(row)
            else:
                updated_older.append(row)

        # Show Report
        print("--- Manga Tracker Web-Crawling Result ---")
        print("Updated Today:")
        for row in updated_today:
            print(row)
        print("\nUpdated in the Last 7 Days:")
        for row in updated_last_7:
            print(row)
        print("\nUpdated in the Last 30 Days:")
        for row in updated_last_30:
            print(row)
        print("\nUpdated More Than 30 Days ago:")
        for row in updated_older:
            print(row)
