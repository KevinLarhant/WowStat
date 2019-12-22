import json
import requests

APIPath = 'https://eu.api.blizzard.com'
tokenURL = 'https://us.battle.net/oauth/token?grant_type=client_credentials'
myOAuth = '2e7605b670ff412fb379e5ea706bca2f'
mySecret = '37oFLU6xjDwZ8DY6HDVSavGfhIUVJM0F'
credentials = '&client_id={0}&client_secret={1}'.format(myOAuth, mySecret)
paramz = '?locale=en_US&access_token='
#realm
dal = 'dalaran'
ys = 'Ysondre'


def get_token(url):
    return requests.get(url).json()['access_token']


def request_to_api(req):
    print('requesting : ', APIPath + req)
    return requests.get(APIPath + req).json()


def get_basic_info_char_by_server_name(realm, char):
    return request_to_api('/wow/character/' + realm + '/' + char)


def get_all_stat_by_server_name(realm, char, token):
    return request_to_api(
        '/wow/character/{0}/{1}?fields=statistics&locale=en_US&access_token={2}'.format(realm, char, token))


def get_bg_done(statJson):
    res = statJson['statistics']['subCategories'][9]['subCategories'][1]['statistics'][0]
    return res['quantity']


def get_bg_won(statJson):
    res = statJson['statistics']['subCategories'][9]['subCategories'][1]['statistics'][2]
    return res['quantity']


def get_gold_CM_done(statJson):
    return statJson['statistics']['subCategories'][14]['statistics'][12]
    return res['quantity']


def write_stat(realm, char, token):
    name_file = 'jsonStats/' + realm + '_' + char + '_' + 'stat.json'
    print('file : ', name_file)
    with open(name_file, "w") as fileStat:
        fileStat.write(json.dumps(get_all_stat_by_server_name(realm, char, token), indent=4))


def add_my_char():
    c = {'aktø': dal, 'waktorr': dal, 'kishaa': dal, 'klehia': dal, 'aktto': dal, 'kamss': dal, 'kaezia': dal,
         'kboom': dal, 'wakito': dal, 'keanna': dal, 'kylx': dal, 'kyootie': dal, 'aktok': dal, 'akkto': dal,
         'Aktø': ys, 'kziin': ys, 'akto': ys}
    return c


token = get_token(tokenURL + credentials)

# call_1_char = get_char_by_server_name('Dalaran', 'Waktorr')
# print('i call :' +APIPath + call_1_char + paramz + token)
# info = requests.get(APIPath + call_1_char + paramz + token)
# print(info.json())

# charge  fichier json stat war
# file = "jsonWaktorrStat.json"
# with open(file, "r") as f:
#     statWar = json.load(f)


#recup / creation fichier stat all persos
my_char = add_my_char()
for char in my_char:
    write_stat(my_char[char], char, token)


# test et print qq stat
# print(get_bg_done(statWar))
# print(get_bg_won(statWar))
# print(get_gold_CM_done(statWar))

# stat url :
# https://eu.api.blizzard.com/wow/character/dalaran/waktorr?fields=statistics&locale=en_US&access_token=USRYSRgBCOpB1XHItm8dI8qFAX6NDcs8BI
