import os
import requests
import urllib3
import time
from base64 import b64encode
from json_parser import create_champions_hashmap


def parse_lockfile():
    # check if the client is running
    league_path = "E:\Riot Games\League of Legends"
    lockfile_path = league_path + "\lockfile"
    lockfile = None
    lockfile_exists = False

    print("Waiting for the client to start")
    while not lockfile_exists:
        if os.path.isfile(lockfile_path):
            lockfile = open(lockfile_path, "r")
            lockfile_exists = True
    # read the lockfile data
    lockfile_data = lockfile.read()
    lockfile_list = lockfile_data.split(":")

    lockfile.close()

    return lockfile_list


def make_request(session, method, path, parameters, data=None, query=None):
    if query is None:
        url = "{}://127.0.0.1:{}{}".format(parameters[4], parameters[2], path)
    else:
        url = "{}://127.0.0.1:{}{}?{}".format(parameters[4], parameters[2], path, query)

    if data is None:
        return getattr(session, method)(url, verify=False, headers=headers)
    else:
        return getattr(session, method)(url, verify=False, headers=headers, json=data)




def get_owned_champions():
    pass


if __name__ == '__main__':
    champions_key = create_champions_hashmap()
    pick_priority = [
        'Draven',
        'Darius',
        'Blitzcrank',
        'Shen',
    ]
    ban_priority = [
        'Morgana',
        'Samira',
        'Leona',
        'Nautilus',
        'MasterYi'
    ]

    username = "riot"
    # 0. process name
    # 1. process pid
    # 2. port
    # 3. password
    # 4. protocol
    request_parameters = parse_lockfile()

    # prepare the request
    password_b64 = b64encode(bytes("{}:{}".format(username, request_parameters[3]), "utf-8")).decode("ascii")
    headers = {'Authorization': 'Basic {}'.format(password_b64)}
    print(headers['Authorization'])

    # login session
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    session = requests.session()
    while True:
        req = make_request(session, 'get', '/lol-login/v1/session', request_parameters)

        if req.status_code != 200:
            continue

        if req.json()['state'] == "SUCCEEDED":
            break

    account_id = req.json()['accountId']
    summoner_id = req.json()['summonerId']
    champions_owned = []
    champions = []
    while True:
        req = make_request(session, 'get', '/lol-champions/v1/owned-champions-minimal', request_parameters)

        print(req.status_code)
        if req.status_code == 200:
            champions = req.json()
            break

    for champion in champions:
        if not champion['active']:
            continue
        champions_owned.append(champion['alias'])

    print(champions_owned)

    picks = []
    for champ_alias in pick_priority:
        if champ_alias not in champions_owned:
            pass
        else:
            picks.append(champions_key[champ_alias])

    lock = False
    if lock:
        print("locking")
    else:
        print("picking")

    champion_index = 0
    ban_index = 0
    champion_locked = False

    planning = False

    while True:
        time.sleep(3)
        req = make_request(session, 'get', '/lol-gameflow/v1/gameflow-phase', request_parameters)

        if req.status_code != 200:
            continue

        phase = req.json()
        print(phase)

        if phase == "Lobby":
            json = {'positionPref': ['BOTTOM', 'UTILITY']}
            make_request(session, 'put', '/lol-lobby/v1/parties/metadata', request_parameters, json)
            time.sleep(1)

            # start the queue
            make_request(session, 'post', '/lol-lobby/v2/lobby/matchmaking/search', request_parameters)

        elif phase == "ReadyCheck":
            time.sleep(1)
            make_request(session, 'post', '/lol-matchmaking/v1/ready-check/accept', request_parameters)

        elif phase == "ChampSelect":
            r = make_request(session, 'get', '/lol-champ-select/v1/session', request_parameters)

            if r.status_code != 200:
                continue

            data = r.json()

            actor_cell_id = -1
            for x in data['myTeam']:
                if x['summonerId'] == summoner_id:
                    actor_cell_id = x['cellId']

            if actor_cell_id == -1:
                continue

            for action in data['actions'][0]:
                if actor_cell_id != action['actorCellId']:
                    continue

                # if data['timer']['phase'] == "BAN_PICK":
                json_data = {'championId': champions_key['Pyke']}

                if action['championId'] == 0:
                    r1 = make_request(session, 'patch', '/lol-champ-select/v1/session/actions/{}'
                                      .format(action['id']), request_parameters, None, json_data)
                    time.sleep(3)
                    print("fiero proprio")

                    if not action['completed']:
                        r2 = make_request(session, 'post', '/lol-champ-select/v1/session/actions/{}/complete'
                                          .format(action['id']), request_parameters, None, json_data)

                """
                if data['timer']['phase'] == "PLANNING" and not planning:
                    r1 = make_request(session, 'patch', '/lol-champ-select/v1/session/actions/{}'.format(action['id']),
                                      request_parameters, {'championId': champions_key['Pyke']})
                    planning = True
                """

                if data['timer']['phase'] == "FINALIZATION":
                    exit(0)
