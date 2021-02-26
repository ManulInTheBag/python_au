import requests
import json

TOKEN = 'I am clown' #insert your token here
PREFIXES = ['GENERATOR', 'LEETCODE']
GROUPS = ['1021', '1022', '1013', '2021', '2022']
PR_ACTION = ['Added', 'Deleted', 'Refactored', 'Moved', 'Fixed']

def prepare_headers():
	return {
			'Authorization': 'token {}'.format(TOKEN),
			'Content-Type': "application/json",
			'Accept': "application/vnd.github.v3+json"
	}

all_prs = requests.get('https://api.github.com/repos/OcTatiana/python_au/pulls', headers=prepare_headers())

def prepare_check_message(pull):
	check_result = []
	title_parts = pull['title'].split()
	prefix_parts = title_parts[0].split('-')

	if len(prefix_parts) == 1:
		prefix_parts.append('')
	elif len(prefix_parts) != 2:
		prefix_parts = ['', '']

	task_prefix, group = prefix_parts

	if task_prefix not in PREFIXES:
		check_result.append('* Pull Request title must start with prefix in {}'.format(PREFIXES))

	if group not in GROUPS:
		check_result.append('* Pull Request title must contain group number in {}')

	if len(title_parts) < 2 or title_parts[1] not in PR_ACTION:
		check_result.append('* Pull Request title action must start with {}'.format(PR_ACTION))

	return '\n'.join(check_result)

def prepare_body(pull, comment):
	return {
		'body': 'Your Pull Request title: {}\n\nCheck result:\n\n{}'.format(pull['title'], comment),
		'path': requests.get(pull['url'] + '/files', headers=prepare_headers()).json()[0]['filename'],
		'position': 1,
		'commit_id': pull['head']['sha']
	}

def send_check_result(pull, comment):
	if len(comment) > 0:
		r = requests.post(pull['url'] + '/comments', headers=prepare_headers(), data=json.dumps(prepare_body(pull, comment)).encode("utf8"))
		print(r.json())

def main():
	r = requests.get('https://api.github.com/repos/OcTatiana/python_au/pulls?state=open', headers=prepare_headers())
	print(r)
	for pull in r.json():
		send_check_result(pull, prepare_check_message(pull))

main()
