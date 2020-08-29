import json
from json import JSONDecodeError
import requests
from WowStatPack.const import *


def get_token(url):
    return requests.get(url).json()['access_token']


def request_to_api_for_json(req):
    print('requesting request_to_api_for_json: ', APIPath + req)
    try:
        res_request = requests.get(APIPath + req)
        if res_request.ok:
            return res_request.json()
        else:
            print('Error request : ', res_request.status_code, res_request.reason, ' in ', res_request.elapsed, 'ms')
            raise ConnectionError()
    except JSONDecodeError:
        print('Error decode JSON')


def request_to_api(req):
    # try:
    res_request = requests.get(req)
    if res_request.ok:
        return res_request.json()
    else:
        print('Error request : ', res_request.status_code, res_request.reason, ' in ', res_request.elapsed, 'ms')
        print('\t\tRequete : ', req)
        print('\t\t\tCause : Mal orthographié, Maj, ou non connecté depuis longtemps')
    #         raise ConnectionError()
    # except ConnectionError:
    #     pass


def get_all_stat_by_server_name(realm, char, token):
    return request_to_api_for_json(
        f'/profile/wow/character/{realm}/{char}?fields=statistics&locale=en_US&access_token={token}&namespace=profile-eu')


def get_gold_CM_done(statJson):
    res = statJson['statistics']['subCategories'][14]['statistics'][12]
    return res['quantity']


def write_stat(realm, char, token):
    name_file = 'jsonStats/' + realm + '_' + char + '_' + 'stat.json'
    print('file : ', name_file)
    with open(name_file, "w") as fileStat:
        fileStat.write(json.dumps(get_all_stat_by_server_name(realm, char, token), indent=4))


# recup / creation fichier stat all persos - UTILE 1 FOIS
# Après changement de l'api, inutile
def create_json_file():
    my_char = listing_my_char()
    for all_char_on_one_server in my_char.items():  # good var name !
        for char in all_char_on_one_server[1]:
            write_stat(all_char_on_one_server[0], char, token)


def create_url(char, type_stat):
    things = f'{APIPath}{path_profile}/{char[0]}/{char[1]}{type_stat}?'
    # ajout des paramètre après
    things += f'{paramz}{token}'
    return things


def get_Ragna_done(char):
    type_stat = path_stats_raids

    res = request_to_api(create_url(char, type_stat))
    # raids = res['expansions']
    try:
        count = get_nb_kill_from_jsonAPI(res, 73, 198)
        return count
    except (KeyError,TypeError) as e:
        print('Error get stat sur : ', char)
        print('\t\tCause : Rien fait sur ce perso')
    return 0


def get_nb_kill_from_jsonAPI(res, expansion_id, boss_id):
    count = 0
    aze = zip(res['expansions'])
    for n in aze:
        mlj = n[0]
        if mlj['expansion']['id'] == expansion_id:
            a = find('encounters', mlj)
            for z in a:
                for j in z:
                    if j['encounter']['id'] == boss_id:
                        count += j['completed_count']
    return count


def get_for_all_char(func):
    res = 0
    for char in All_char.items():
        res += func(char[1])
    return res


def find(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result


def main():
    # create_json_file()

    # test new fonctionnnemlnt
    # print(get_Ragna_done(All_char['Klehia']))
    print(get_for_all_char(get_Ragna_done))


token = get_token(tokenURL + credentials)
main()
