import json
from json import JSONDecodeError

import requests

APIPath = 'https://eu.api.blizzard.com'
tokenURL = 'https://us.battle.net/oauth/token?grant_type=client_credentials'
myOAuth = '2e7605b670ff412fb379e5ea706bca2f'
mySecret = '37oFLU6xjDwZ8DY6HDVSavGfhIUVJM0F'
credentials = f'&client_id={myOAuth}&client_secret={mySecret}'
paramz = '?locale=en_US&access_token='
# realm
dal = 'dalaran'
ys = 'ysondre'


def get_token(url):
    return requests.get(url).json()['access_token']


def request_to_api(req):
    print('requesting : ', APIPath + req)
    try:
        res_request = requests.get(APIPath + req)
        if res_request.ok:
            return res_request.json()
        else:
            print('Error request : ', res_request.status_code, res_request.reason, ' in ', res_request.elapsed, 'ms')
            raise ConnectionError()
    except JSONDecodeError:
        print('Error decode JSON')


def get_basic_info_char_by_server_name(realm, char):
    return request_to_api('/wow/character/' + realm + '/' + char)


def get_all_stat_by_server_name(realm, char, token):
    return request_to_api(
        f'/profile/wow/character/{realm}/{char}?fields=statistics&locale=en_US&access_token={token}&namespace=profile-eu')


def get_bg_done(statJson):
    res = statJson['statistics']['subCategories'][9]['subCategories'][1]['statistics'][0]
    return res['quantity']


def get_bg_won(statJson):
    res = statJson['statistics']['subCategories'][9]['subCategories'][1]['statistics'][2]
    return res['quantity']


def get_gold_CM_done(statJson):
    res = statJson['statistics']['subCategories'][14]['statistics'][12]
    return res['quantity']


def write_stat(realm, char, token):
    name_file = 'jsonStats/' + realm + '_' + char + '_' + 'stat.json'
    print('file : ', name_file)
    with open(name_file, "w") as fileStat:
        fileStat.write(json.dumps(get_all_stat_by_server_name(realm, char, token), indent=4))


def listing_my_char():  # todo : refaire depuis fichier ou "Account Profile API"
    dalaran_char = ['aktø', 'waktorr', 'kishaa', 'klehia', 'aktto', 'kamss', 'kaezia', 'kboom', 'wakito', 'keanna',
                    'kylx', 'kyootie', 'aktok', 'akkto']
    ysondre_char = ['aktø', 'kziin', 'akto']
    c = {dal: dalaran_char, ys: ysondre_char}
    return c


def create_json_file():  # todo:refaire structure ou code idk c'est dégueu
    my_char = listing_my_char()
    for all_char_on_one_server in my_char.items():  # good var name !
        for char in all_char_on_one_server[1]:
            write_stat(all_char_on_one_server[0], char, token)


def main():
    # call_1_char = get_char_by_server_name('Dalaran', 'Waktorr')
    # print('i call :' +APIPath + call_1_char + paramz + token)
    # info = requests.get(APIPath + call_1_char + paramz + token)
    # print(info.json())

    # charge fichier json stat war
    # file = "/jsonStats/dalaran_waktorr_stat.json"
    # with open(file, "r") as f:
    #     statWar = json.load(f)

    # recup / creation fichier stat all persos - UTILE 1 FOIS
    create_json_file()

    # test et print qq stat
    # print(get_bg_done(statWar))
    # print(get_bg_won(statWar))
    # print(get_gold_CM_done(statWar))

    # stat url :
    # https://eu.api.blizzard.com/wow/character/dalaran/waktorr?fields=statistics&locale=en_US&access_token=USRYSRgBCOpB1XHItm8dI8qFAX6NDcs8BI


token = get_token(tokenURL + credentials)
print('token is : ', token)
main()
