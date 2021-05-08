import datetime

def open_csv(input_csv): #открыть файл, считать список
	data = open(input_csv, r)
	return list(map(lambda x: x.strip().split(','), data.readlines()))

def list_to_dict(table):
	return list(map(lambda x: dict(zip(headers, x)), table[1:]))

def filter_data(data, key, value):
	f = filter(lambda x: x[key] == value, data)
	return f

def sorted_data(data, sort_key):
	if sort_key in ['resource', 'count']:
        return sorted(data, key=lambda x: int(x[sort_key] if x[sort_key] != '' else 0))
    if sort_key == 'date':
        return sorted(data, key=lambda x: datetime.strptime(x[sort_key], "%Y-%m") if x[sort_key] != '' else datetime.datetime(1, 1, 1))
    if sort_key == 'staff_id':
        return sorted(data, key=lambda x: x[sort_key].strip())

		#графики
