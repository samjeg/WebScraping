import json

myRecord = {
	'name': 'Samuel',
	'age': 28,
	'occupation': 'unemployed'
}

j = json.dumps(myRecord)
with open('my_record.json', 'w') as f:
	f.write(j)
	f.close()