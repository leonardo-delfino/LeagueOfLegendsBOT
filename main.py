import os
import time
import requests
from base64 import b64encode
from constants import *

# check if the client is running
lockfile_path = LEAGUE_PATH + "\lockfile"
lockfile = None
lockfile_exists = False
while not lockfile_exists:
    if os.path.isfile(lockfile_path):
        lockfile = open(lockfile_path, "r")
        lockfile_exists = True
    time.sleep(5)

# read the lockfile data
lockfile_data = lockfile.read()
lockfile_list = lockfile_data.split(":")

print(lockfile_list)

process_name = lockfile_list[0]
process_pid = lockfile_list[1]
league_port = lockfile_list[2]

host = "127.0.0.1"
username = "riot"
password = lockfile_list[3]

lockfile.close()

# prepare the request
password_b64 = b64encode(bytes("{}:{}".format(username, password), "utf-8")).decode("ascii")
headers = {'Authorization': 'Basic {}'.format(password_b64)}
print(headers['Authorization'])

# make the request
session = requests.session()
