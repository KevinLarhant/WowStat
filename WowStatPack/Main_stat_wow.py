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
    print('requesting request_to_api : ', req)
    try:
        res_request = requests.get(req)
        if res_request.ok:
            return res_request.json()
        else:
            print('Error request : ', res_request.status_code, res_request.reason, ' in ', res_request.elapsed, 'ms')
            raise ConnectionError()
    except ConnectionError:
        pass


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


def create_json_file():  # todo:refaire structure ou code idk c'est dégueu
    my_char = listing_my_char()
    for all_char_on_one_server in my_char.items():  # good var name !
        for char in all_char_on_one_server[1]:
            write_stat(all_char_on_one_server[0], char, token)


def create_url(char, type_stat):
    things = f'{APIPath}{path_profile}/{char[0]}/{char[1]}{type_stat}?'
    # ajout des paramètre après
    things += f'{paramz}{token}'
    print('things :', things)
    return things


def get_Ragna_done(char):
    type_stat = path_raids
    res = request_to_api(create_url(char, type_stat))

    # sssssssssssssssssssssssssaaale
    # et non ça marche pas
    # res['expansions'][3]['instances'][3]['modes'][0]['progress']['encounters'][6]['completed_count']
    w = res['expansions'][3]['instances']
    # todo get isntances ou autre par id (ragna = 198)
    print(type(res))
    print(type(w), ':', w)
    a = find('encounters', res)
    for i in a:
        print('->', i)

    return 1


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
    # recup / creation fichier stat all persos - UTILE 1 FOIS - à jour 23/08/2020
    # et non maintenat c'est nul
    # create_json_file()

    # test new fonctionnnemlnt
    print(get_Ragna_done(All_char['Waktorr']))
    # print(get_for_all_char(get_Ragna_done))


token = get_token(tokenURL + credentials)
main()
