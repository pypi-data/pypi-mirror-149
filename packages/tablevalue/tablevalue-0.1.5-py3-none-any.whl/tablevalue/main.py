import sqlite3


class TableValue(object):

    class Types:
        INTEGER = 'INTEGER'
        REAL = 'REAL'
        TEXT = 'TEXT'
        BLOC = 'BLOB'

    @staticmethod
    def _get_where_string_value(filter_query: dict):
        if len(filter_query) > 0:
            where_section = list()
            where_string = 'where '
            values_query = list()
            for key, value in filter_query.items():
                string_filter = f'{key}=?'
                values_query.append(value)
                where_section.append(string_filter)

            where_string += ' and '.join(where_section)
        else:
            values_query = None
            where_string = ''
        return where_string, values_query

    def __init__(self, path=None):
        if path is None:
            self.conn = sqlite3.connect(':memory:')
        else:
            self.conn = sqlite3.connect(path)
        self._transaction_active = False
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Table1(
                           id INT PRIMARY KEY);""")
        self.conn.commit()
        self.columns = Columns(self)

    def begin_transaction(self):
        self._transaction_active = True

    def transaction_is_active(self) -> bool:
        return self._transaction_active

    def finish_transaction(self):
        if self.transaction_is_active():
            self.conn.commit()

    def cancel_transaction(self):
        if self.transaction_is_active():
            self.conn.rollback()

    def new_row(self):
        return Row(self)

    def new_bulk_insert(self, *values_to_bulk):
        self.cur.executemany(f'INSERT INTO table1({self.columns.get_all_at_string()}) VALUES({self.columns.get_question_for_query()});', tuple(values_to_bulk[0]))
        if not self.transaction_is_active():
            self.conn.commit()

    def get_data(self, filter_query=None, sort='', limit=100000000):
        """
        Fast get method from table
        :param limit: limit for select
        :param filter_query: dict
        :param sort: str
        :return:
        """

        if filter_query is None:
            filter_query = {}

        sort_string = ''
        if bool(sort):
            sort_string = f'order by {sort}'

        where_string, values_query = self._get_where_string_value(filter_query)

        if values_query is None:
            self.cur.execute(f'SELECT {self.columns.get_all_at_string()} FROM table1 {where_string} {sort_string} Limit {limit};')
        else:
            self.cur.execute(f'SELECT {self.columns.get_all_at_string()} FROM table1 {where_string} {sort_string} Limit {limit};', values_query)

        all_data = self.cur.fetchall()
        return all_data

    def get_rows(self, filter_query=None, sort='', limit=100000000):

        """
        Slow formatted get method from table
        :param limit: limit for select
        :param filter_query: dict
        :param sort: str
        :return: list of Row classes
        """

        if filter_query is None:
            filter_query = {}

        all_pre_data = self.get_data(filter_query, sort, limit)
        all_data = list()
        for data in all_pre_data:
            all_data.append(Row(self, data))

        return all_data

    def get_grouped_data(self, columns_to_group, columns_to_sum='', filter_query=None, sort='', number_of_rows=100000000, row_mode=True):

        if filter_query is None:
            filter_query = {}

        if type(columns_to_group) == str:
            columns_to_group = [i.strip() for i in columns_to_group.split(',')]

        if type(columns_to_sum) == str:
            columns_to_sum = [i.strip() for i in columns_to_sum.split(',')]

        sort_string = ''
        if bool(sort):
            sort_string = f'order by {sort}'

        where_string, values_query = self._get_where_string_value(filter_query)

        text_grouped = ','.join(columns_to_group)
        text_sum = []
        for to_group in columns_to_sum:
            text_sum.append(f'sum({to_group})')

        if len(text_sum):
            text_sum = ',' + ','.join(text_sum)
        else:
            text_sum = ''

        executed_text = f'select {text_grouped}{text_sum} from table1 {where_string} group by {text_grouped} {sort_string} Limit {number_of_rows}'

        if values_query is None:
            self.cur.execute(executed_text)
        else:
            self.cur.execute(executed_text, values_query)

        result = self.cur.fetchall()

        if row_mode:
            all_data = list()
            for data in result:
                all_data.append(Row(self, data, columns_to_group + columns_to_sum))
            return all_data
        else:
            return result

    def count(self):
        self.cur.execute('select count(*) from table1')
        return self.cur.fetchone()[0]

    def update(self, filter_query, values_query):
        update_string = []
        arguments = []
        for key, value in values_query.items():
            update_string.append(f'{key} = ?')
            arguments.append(value)

        where_string, values_for_query = self._get_where_string_value(filter_query)
        for value_query in values_for_query:
            arguments.append(value_query)

        update_string = ','.join(update_string)
        executed_text = f'''Update Table1 set {update_string} {where_string}'''
        self.cur.execute(executed_text, arguments)
        if not self.transaction_is_active():
            self.conn.commit()

    def special_query(self, query, need_commit=False):
        self.cur.execute(query)
        if need_commit:
            self.conn.commit()
        else:
            return self.cur.fetchall()

    def clear(self):
        sql = 'delete from table1'
        self.cur.execute(sql)
        if not self.transaction_is_active():
            self.conn.commit()

    def delete(self, filter_query):
        where_string, values_query = self._get_where_string_value(filter_query)
        sql = f'delete from table1 {where_string}'
        self.cur.execute(sql, values_query)
        if not self.transaction_is_active():
            self.conn.commit()


class Columns(list):

    def __init__(self, parent):
        self._parent = parent

    def add(self, name_column, type_column='TEXT') -> None:
        """
        Add column in the table
        :param name_column:
        :param type_column: INTEGER, REAL, TEXT, BLOB
        :return:
        """
        column = {'name': name_column,
                  'type': type_column}
        self.append(column)
        self._parent.cur.execute(f'ALTER TABLE table1 ADD COLUMN {name_column} {type_column}')
        self._parent.conn.commit()

    def get_all(self) -> list:
        result = list()
        for column in self:
            result.append(column['name'])

        return result

    def get_all_at_string(self):
        all_columns = self.get_all()
        return ','.join(all_columns)

    def get_question_for_query(self) -> str:
        pre_result = list()
        for column in self.get_all():
            pre_result.append('?')
        return ','.join(pre_result)


class Row(object):

    def __init__(self, parent: TableValue, filled_values=None, name_fields=None):
        self._parent = parent
        self._all_columns_string = parent.columns.get_all_at_string()
        self._all_columns = parent.columns.get_all()
        if filled_values is None:
            self._new_string = True
        else:
            self._new_string = False

        index = 0


        if name_fields is None:
            columns = self._parent.columns.get_all()
        else:
            columns = name_fields

        for column in columns:
            if filled_values is None:
                value = None
            else:
                value = filled_values[index]
            self.__dict__[column] = value
            index += 1

    def apply_add(self):
        if not self._new_string:
            return

        values_for_query = list()
        for column in self._all_columns:
            values_for_query.append(self.__dict__[column])

        self._parent.cur.execute(f'INSERT INTO table1({self._all_columns_string}) VALUES({self._parent.columns.get_question_for_query()});', list(values_for_query))
        if not self._parent.transaction_is_active():
            self._parent.finish_transaction()