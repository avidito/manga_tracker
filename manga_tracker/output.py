from datetime import datetime, timedelta
import operator
import re

class OutputHandler:
    """
    [Static Method] Handler to create and show job outputs.
    """
    @staticmethod
    def _date_grouper(today_dt, date_str, pattern='%d-%m-%Y %H:%M'):
        """
        Function to convert date into time category.

        Params
        ------
            today_dt: date. System current date.
            date_str: str. Date in string format.
            pattern : str (default='%d-%m-%Y %H:%M'). String literal to extract date data.

        Returns
        -------
            group   : int. Time group (1 for 'today', 2 for 'last 7 days', 3 for 'last 30 days', 4 for 'older')
        """
        query_dt = datetime.strptime(date_str, pattern).date()
        if (query_dt == today_dt):
            return 1
        elif (query_dt >= today_dt - timedelta(days=7)):
            return 2
        elif (query_dt >= today_dt - timedelta(days=30)):
            return 3
        else:
            return 4

    @staticmethod
    def _output_viz(data):
        """
        Format data for output visualisation.

        Params
        ------
            data        : list. Output data in 2D list format.

        Returns
        -------
            header  : list. Header in list of string format.
            content : list. Transformed data in list of list format.
        """
        _tr = (
            lambda x: (x),                                              # website
            lambda x: x,                                              # alias
            lambda x: ''.join((x[:17], '...')) if len(x) > 20 else x, # title
            lambda x: 'Ongoing' if (x) else 'Completed',              # ongoing
            lambda x: x,                                              # updated_at
            lambda x: ''.join((x[:17], '...')) if len(x) > 20 else x, # latest_chapter
            lambda x: ''.join((x[:17], '...')) if len(x) > 20 else x, # latest_chapter_link
        )
        header = data[0]
        content = [[_tr[i](val) for i, val in enumerate(row)] for row in data[1:]]
        content.sort(key=operator.itemgetter(0, 1))
        return header, content

    @staticmethod
    def _result_viz(data):
        """
        Rearrange and transform output data for result visualization.

        Params
        ------
            data        : list. Output data in 2D list format.

        Returns
        -------
            header  : list. Header in list of string format.
            content : list. Transformed data in list of list format.
        """
        # Extract and Rearrange Column
        _er = (4, 4, 1, 0, 5, 6)
        er_data = [[ row[col_id] for col_id in _er] for row in data]

        # Transform
        today = datetime.now().date()
        _tr = (
            lambda x: OutputHandler._date_grouper(today, x),          # update_tag
            lambda x: x,                                              # update_at
            lambda x: x,                                              # title
            lambda x: x,                                              # website
            lambda x: ''.join((x[:17], '...')) if len(x) > 20 else x, # chapter
            lambda x: re.sub('http[s]*://', '', x),                                              # chapter_link
        )
        header = er_data[0]
        content = [[_tr[i](val) for i, val in enumerate(row)] for row in er_data[1:]]
        content.sort(key=operator.itemgetter(0, 1))

        return header, content

    @staticmethod
    def init_output(path, columns, delimiter):
        """
        Initiate output file by pathname.

        Paramaters
        ----------
            path        : str. Relative pathname for output file directory (result directory).
            columns     : list. List of columns name for output table.
            delimiter   : str. Delimiter used for separating data.
        """
        out_path = path + '/outputs.txt'
        with open(out_path, 'w') as f:
            f.write(delimiter.join(columns) + '\n')

    @staticmethod
    def load_data(path, website, alias, data, columns, delimiter):
        """
        Convert data to row format and load to database.

        Parameters
        ----------
            path        : str. Relative pathname for output file directory (result directory).
            website     : str. Website's name for output data.
            alias       : str. Defined manga alias for output and log result.
            data        : dict. Extracted data that want to be loaded to outputs file.
            columns     : list. List of columns name for output table.
            delimiter   : str. Delimiter used for separating data.
        """
        # Transform data to row format
        trans_data = ''
        for col in columns[2:]:
            trans_data += '{}{}'.format(delimiter, data[col])
        row = ''.join([website, '|', alias, trans_data])

        # Load to database
        out_path = path + '/outputs.txt'
        with open(out_path, 'a', encoding="utf-8") as f:
            f.write(row + '\n')

    @staticmethod
    def show_output(path, delimiter):
        """
        Show full crawling result in table format.

        Parameters
        ----------
            path        : str. Relative pathname for output file directory (result directory).
            delimiter   : str. Delimiter used for separating data.

        Returns
        -------
            output      : list. Output data in 2D list format.
        """
        out_path = path + '/outputs.txt'
        with open(out_path, 'r', encoding="utf-8") as f:
            raw = f.read()[:-1]
        output = [row.split(delimiter) for row in raw.split('\n')]

        # Format Visualization
        header, content = OutputHandler._output_viz(output)
        formatted = [header] + content
        return formatted

    @staticmethod
    def result(path, delimiter):
        """
        Show crawling result summary.

        Parameters
        ----------
            path        : str. Relative pathname for output file directory (result directory).
            delimiter   : str. Delimiter used for separating data.
        """
        out_path = path + '/outputs.txt'
        with open(out_path, 'r', encoding="utf-8") as f:
            raw = f.read()
        result = [row.split(delimiter) for row in raw.strip().split('\n')]
        header, content = OutputHandler._result_viz(result)
        formatted = [header] + content
        return formatted
