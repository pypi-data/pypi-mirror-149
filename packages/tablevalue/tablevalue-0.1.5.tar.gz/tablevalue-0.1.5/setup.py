# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tablevalue']

package_data = \
{'': ['*'],
 'tablevalue': ['.git/*',
                '.git/hooks/*',
                '.git/info/*',
                '.git/logs/*',
                '.git/logs/refs/heads/*',
                '.git/logs/refs/remotes/origin/*',
                '.git/objects/09/*',
                '.git/objects/16/*',
                '.git/objects/1a/*',
                '.git/objects/2d/*',
                '.git/objects/37/*',
                '.git/objects/5f/*',
                '.git/objects/89/*',
                '.git/objects/94/*',
                '.git/objects/96/*',
                '.git/objects/aa/*',
                '.git/objects/bf/*',
                '.git/objects/e1/*',
                '.git/objects/f6/*',
                '.git/refs/heads/*',
                '.git/refs/remotes/origin/*',
                '.idea/*',
                '.idea/inspectionProfiles/*']}

setup_kwargs = {
    'name': 'tablevalue',
    'version': '0.1.5',
    'description': 'Table value as 1C:Enterprise',
    'long_description': '\n## API Reference\n\n#### import\n\n```python\n  from tablevalue import TableValue\n```\n\n#### Methods\n\n| Method    | Arguments | Description                |\n| :-------- | :-------- |:------------------------- |\n| begin_transaction |  |Setting the transaction start sign |\n| finish_transaction |  |conn.commit() |\n| cancel_transaction |  |conn.rollback() |\n| transaction_is_active |  |Indication of transaction activity |\n| new_row |  |return Row object |\n| new_bulk_insert | values_to_bulk |fast insert to database |\n| get_data |  filter_query:dict, sort: str, limit = 100000000| self.cur.fetchall() |\n| get_rows |  filter_query:dict, sort: str, limit = 100000000| return list of Row objects, Easier to interact with |\n| get_grouped_data |  columns_to_group: str, columns_to_sum: str, filter_query:dict, sort: str, number_of_rows = 100000000, row_mode=True| return grouped data\n| count |  | the same as "select count(*) from table" |\n| update | filter_query:dict, values_query:dict | update data |\n| clear |  | delete all data from table |\n| delete | filter_query: dict | deleting selection data |\n\n\n\n\n#### Usage\n# 1. Get grouped data\n```python\n  parsed_csv = ((\'oleg\', \'Asbest\', 2, 1),\n                  (\'ivan\', \'Asbest\', 1, 2),\n                  (\'nastya\', \'Krasnodar\', 0, 2),\n                  (\'Max\', \'Asbest\', 1, 2),\n                  (\'Even\', \'Krasnodar\', 1, 2),\n                  (\'Rob\', \'Krasnodar\', 1, 2),\n                  (\'Mob\', \'Ekaterinburg\', 1, 2),\n                  (\'Dick\', \'Ekaterinburg\', 1, 2),\n                  (\'Cheize\', \'Krasnodar\', 1, 2),\n                  (\'Longard\', \'Ekaterinburg\', 1, 2),\n                  )\n\n    table = TableValue()\n    table.columns.add(\'Name\')\n    table.columns.add(\'country\')\n    table.columns.add(\'count_of_pets\', table.Types.INTEGER)\n    table.columns.add(\'count_of_children\', table.Types.INTEGER)\n\n    for data in parsed_csv:\n        new_row = table.new_row()\n        new_row.Name = data[0]\n        new_row.country = data[1]\n        new_row.count_of_pets = data[2]\n        new_row.count_of_children = data[3]\n        new_row.apply_add()\n\n    grouped_county_data = table.get_grouped_data(\'country\', \'count_of_pets, count_of_children\')\n\n    for country_data in grouped_county_data:\n        message_county = f\'{country_data.country}    :   pets: {country_data.count_of_pets}, childrens: {country_data.count_of_children}\'\n        print(message_county)\n```\n\n#### Output\n\n```http\nAsbest    :   pets: 4, childrens: 5\nEkaterinburg    :   pets: 3, childrens: 6\nKrasnodar    :   pets: 3, childrens: 8\n```\n\n# 2. Get count\n```python\nprint(table.count())\n```\n\n#### Output\n\n```http\n10\n```\n\n# 3. Get filtered data\n```python\nasbest = table.get_rows(filter_query={\'country\': \'Asbest\'})\nfor data in asbest:\n    print(f\'{data.name}: childrens: {data.count_of_children}. Pets: {data.count_of_pets}\')\n```\n#### Output\n```http\noleg: childrens: 1. Pets: 2\nivan: childrens: 2. Pets: 1\nMax: childrens: 2. Pets: 1\n```\n\n# 4. Update\n```python\ntable.update(filter_query={\'name\': \'oleg\'}, values_query={\'name\' : \'OLEG\'})\ndata_oleg = table.get_rows(filter_query={\'name\': \'OLEG\'})\ndata = data_oleg[0]\nprint(f\'{data.name}: childrens: {data.count_of_children}. Pets: {data.count_of_pets}\')\n```\n#### Output\n```\nOLEG: childrens: 1. Pets: 2\n```\n# 5. Delete record\n```python\ntable.delete(filter_query={\'name\':\'OLEG\'})\ndata_oleg = table.get_rows(filter_query={\'name\': \'OLEG\'})\ndata = data_oleg[0]\n```\n#### Output\n```\n  data = data_oleg[0]\nIndexError: list index out of range\n```\n\n# 6. Transactions\nWhen there is an active transaction, commit is not performed automatically.\nThe following construction interferes\n\n```\nif not self.transaction_is_active():\n    self.conn.commit()\n```\n\nGitHub\nhttps://github.com/nixonsis/TableValue',
    'author': 'to101',
    'author_email': 'to101kv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.1,<4.0',
}


setup(**setup_kwargs)
