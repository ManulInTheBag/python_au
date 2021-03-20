#Importing libraries

import requests
import json

#Constants

TOKEN = 'imaclown' #insert your token instead of this string
PREFIXES = ['LEETCODE', 'GENERATOR', 'TRIANGLE', 'HEXNUMBER', 'REQUESTS', 'ITERATOR']
GROUPS = ['1021', '1022']
PR_ACTION = ['Added', 'Deleted', 'Refactored', 'Moved', 'Fixed']

#Methods

def prepare_headers():
	return {
			'Authorization': 'token {}'.format(TOKEN),
			'Content-Type': "application/json",
			'Accept': "application/vnd.github.v3+json"
	}

def get_all_pulls(login = 'ManulInTheBag', repos = 'python_au', state = 'open'):
	all_prs = requests.get('https://api.github.com/repos/{}/{}/pulls?state={}'.format(login, repos, state), headers=prepare_headers())
	return all_prs

def get_all_commits(pull):
	all_commits = requests.get(pull['commits_url'], headers=prepare_headers())
	return all_commits

def prepare_check_message(name, iscommit):
	check_result = []
	if not name:
		check_result.append('* The title must exist.')
		return '\n'.join(check_result)
	title_parts = name.split()
	prefix_parts = title_parts[0].split('-')

	if len(prefix_parts) == 1:
		prefix_parts.append('')
	elif len(prefix_parts) != 2:
		prefix_parts = ['', '']

	task_prefix, group = prefix_parts

	forformat = []

	if iscommit:
		forformat = 'Commit'
	else:
		forformat = 'Pull Request'

	if task_prefix not in PREFIXES:
		check_result.append('* {} title must start with prefix in {}'.format(forformat, PREFIXES))

	if group not in GROUPS:
		check_result.append('* {} title must contain group number in {}'.format(forformat, GROUPS))

	if len(title_parts) < 2 or title_parts[1] not in PR_ACTION:
		check_result.append('* {} title action must start with {}'.format(forformat, PR_ACTION))

	print(check_result)

	return '\n'.join(check_result)

#returns last comment of author for this pull
def last_comment_time(pull, author):
    all_comments = requests.get(pull['review_comments_url'], headers=prepare_headers()).json()
    last_comment = "0000-00-00T00:00:00Z"
    for comment in all_comments:
    	if comment['user']['login'] == author:
        	last_comment = comment['created_at']
    return last_comment

def get_commit_time(commit):
    return commit['commit']['author']['date']

def prepare_body_pull(pull, comment):
	return {
		'body': 'Your Pull Request title: {}\n\nCheck result:\n\n{}'.format(pull['title'], comment),
		'path': requests.get(pull['url'] + '/files', headers=prepare_headers()).json()[0]['filename'],
		'position': 1,
		'commit_id': pull['head']['sha']
	}

def send_check_result_pull(pull, comment):
	if len(comment) > 0:
		r = requests.post(pull['review_comments_url'], headers=prepare_headers(), data=json.dumps(prepare_body_pull(pull, comment)).encode("utf8"))
		print(r.json())

def check_pull(pull):
	message = prepare_check_message(pull['title'], False)
	for commit in get_all_commits(pull).json():
		if last_comment_time(pull, 'ManulInTheBag') < get_commit_time(commit):
			message = message + '\n' +  prepare_check_message(commit['commit']['message'], True)
	send_check_result_pull(pull, message)

def main():
	r = get_all_pulls('ManulInTheBag','python_au', 'open')#using OcTatiana because my git is empty
	message = ''
	print(r)
	for pull in r.json():
		check_pull(pull)

#Actual script

main()