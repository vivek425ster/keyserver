from flask import Flask, redirect
import random
import datetime
import string
from collections import deque

app = Flask(__name__)

def generate_random_key(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

is_present = {}
is_block = {}
is_free = deque([])
blocked_keys = {}

@app.route('/generate_key')
def generate_key():
	while 1:
		key1 = generate_random_key(30)
		if key1 not in is_present.keys() or is_block[key1] == 0:
			is_present[key1] = datetime.datetime.now()
			is_block[key1] = 1
			is_free.append(key1)
			break
		else:
			continue
	return "key %s " % key1

@app.route('/get_key')
def get_key():
	size = len(is_free)
	if size != 0:
		while 1:
			free_key = is_free.pop()
			if is_block[free_key] == 1:
				is_block[free_key] = 2
				is_present[free_key] = datetime.datetime.now()
				return "Key %s" %free_key
			elif is_block[free_key] == 2:
				diff_time = datetime.datetime.now() - is_present[free_key]
				if diff_time.seconds > 60:
					is_block[free_key] = 2
					return "Key %s" %free_key
			else:
				return redirect("/where-ever"), 404, {"Refresh": "1; url=/where-ever"}			
	else:
	    return redirect("/where-ever"), 404, {"Refresh": "1; url=/where-ever"}			

@app.route('/unblock_key/<key>')
def unblock_key(key):
	if is_block[key] == 2:
		is_present[key] = datetime.datetime.now()
		is_free.append(key)
		is_block[key] = 1
		return "Key %s unblocked " %key
	elif is_block[key] == 1:
		return "Following key is already free"
	elif is_block[key] == 0:
		return "Following key has been purged"
	return "Following key has not been generated"

@app.route('/delete_key/<key>')
def delete_key(key):
	if key in is_present:
		is_block[key] = 0
		return "Key %s has been deleted" %key

@app.route('/keep_alive/<key>')
def keep_alive(key):
	if is_block[key] != 0:
		diff_time = datetime.datetime.now() - is_present[key]
		if diff_time.seconds > 300:
			is_block[key] = 0
			return "Key %s has been deleted" %key
		is_present[key] = datetime.datetime.now()
		return "Key %s is alive" %key
	return "Key %s has been deleted" %key
	
@app.route('/')
def hello_world():
    print generate_random_key(30)
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug = True)
