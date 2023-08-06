
## Description

# install
```
  pip install tablevalue
```

#### import

```python
from tablevalue import TableValue
```

#### Methods

| Method    | Arguments | Description                |
| :-------- | :-------- |:------------------------- |
| begin_transaction |  |Setting the transaction start sign |
| finish_transaction |  |conn.commit() |
| cancel_transaction |  |conn.rollback() |
| transaction_is_active |  |Indication of transaction activity |
| new_row |  |return Row object |
| new_bulk_insert | values_to_bulk |fast insert to database |
| get_data |  filter_query:dict, sort: str, limit = 100000000| self.cur.fetchall() |
| get_rows |  filter_query:dict, sort: str, limit = 100000000| return list of Row objects, Easier to interact with |
| get_grouped_data |  columns_to_group: str, columns_to_sum: str, filter_query:dict, sort: str, number_of_rows = 100000000, row_mode=True| return grouped data
| count |  | the same as "select count(*) from table" |
| update | filter_query:dict, values_query:dict | update data |
| clear |  | delete all data from table |
| delete | filter_query: dict | deleting selection data |




#### Usage
# 1. Get grouped data
```python
  parsed_csv = (('oleg', 'Asbest', 2, 1),
                  ('ivan', 'Asbest', 1, 2),
                  ('nastya', 'Krasnodar', 0, 2),
                  ('Max', 'Asbest', 1, 2),
                  ('Even', 'Krasnodar', 1, 2),
                  ('Rob', 'Krasnodar', 1, 2),
                  ('Mob', 'Ekaterinburg', 1, 2),
                  ('Dick', 'Ekaterinburg', 1, 2),
                  ('Cheize', 'Krasnodar', 1, 2),
                  ('Longard', 'Ekaterinburg', 1, 2),
                  )

    table = TableValue()
    table.columns.add('Name')
    table.columns.add('country')
    table.columns.add('count_of_pets', table.Types.INTEGER)
    table.columns.add('count_of_children', table.Types.INTEGER)

    for data in parsed_csv:
        new_row = table.new_row()
        new_row.Name = data[0]
        new_row.country = data[1]
        new_row.count_of_pets = data[2]
        new_row.count_of_children = data[3]
        new_row.apply_add()

    grouped_county_data = table.get_grouped_data('country', 'count_of_pets, count_of_children')

    for country_data in grouped_county_data:
        message_county = f'{country_data.country}    :   pets: {country_data.count_of_pets}, childrens: {country_data.count_of_children}'
        print(message_county)
```

#### Output

```http
Asbest    :   pets: 4, childrens: 5
Ekaterinburg    :   pets: 3, childrens: 6
Krasnodar    :   pets: 3, childrens: 8
```

# 2. Get count
```python
print(table.count())
```

#### Output

```http
10
```

# 3. Get filtered data
```python
asbest = table.get_rows(filter_query={'country': 'Asbest'})
for data in asbest:
    print(f'{data.name}: childrens: {data.count_of_children}. Pets: {data.count_of_pets}')
```
#### Output
```http
oleg: childrens: 1. Pets: 2
ivan: childrens: 2. Pets: 1
Max: childrens: 2. Pets: 1
```

# 4. Update
```python
table.update(filter_query={'name': 'oleg'}, values_query={'name' : 'OLEG'})
data_oleg = table.get_rows(filter_query={'name': 'OLEG'})
data = data_oleg[0]
print(f'{data.name}: childrens: {data.count_of_children}. Pets: {data.count_of_pets}')
```
#### Output
```
OLEG: childrens: 1. Pets: 2
```
# 5. Delete record
```python
table.delete(filter_query={'name':'OLEG'})
data_oleg = table.get_rows(filter_query={'name': 'OLEG'})
data = data_oleg[0]
```
#### Output
```
  data = data_oleg[0]
IndexError: list index out of range
```

# 6. Transactions
When there is an active transaction, commit is not performed automatically.
The following construction interferes

```
if not self.transaction_is_active():
    self.conn.commit()
```

GitHub
https://github.com/nixonsis/TableValue