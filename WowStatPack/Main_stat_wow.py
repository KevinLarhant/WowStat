import requests
from WowStatPack.const import *


def get_token(url):
    return requests.get(url).json()['access_token']


def request_to_api(req):
    res_request = requests.get(req)
    if res_request.ok:
        return res_request.json()
    else:
        print('Error request : ', res_request.status_code, res_request.reason, ' in ', res_request.elapsed, 'ms')
        print('\t\tRequete : ', req)
        print('\t\t\tCause : Mal orthographié, Maj, ou non connecté depuis longtemps')


# todo
def get_gold_CM_done(stat_json):
    res = stat_json['statistics']['subCategories'][14]['statistics'][12]
    return res['quantity']


# Après changement de l'api, inutile :'(
# def write_stat(realm, char, token):
#     name_file = 'jsonStats/' + realm + '_' + char + '_' + 'stat.json'
#     print('file : ', name_file)
#     with open(name_file, "w") as fileStat:
#         fileStat.write(json.dumps(get_all_stat_by_server_name(realm, char, token), indent=4))


# recup / creation fichier stat all persos - UTILE 1 FOIS
# Après changement de l'api, inutile :'(
# def create_json_file():
#     my_char = All_char
#     for all_char_on_one_server in my_char.items():  # good var name !
#         for char in all_char_on_one_server[1]:
#             write_stat(all_char_on_one_server[0], char, token)


def create_url(char, type_stat):
    things = f'{APIPath}{path_profile}/{char[0]}/{char[1]}{type_stat}?'
    # ajout des paramètre après
    things += f'{paramz}{token}'
    return things


def get_Ragna_done(char):
    type_stat = path_stats_raids

    res = request_to_api(create_url(char, type_stat))
    try:
        count = get_nb_kill_from_json(res, 73, 198)
        return count
    except (KeyError, TypeError):
        print('Error get stat sur : ', char)
        print('\t\tCause : Rien fait sur ce perso')
    return 0


# todo : possiblement refaire parce que c'est peu compréhensible au final
def get_nb_kill_from_json(res, expansion_id, boss_id):
    """
    Classic = 68
    BC = 70
    WOTLK = 72
    Cata = 73
    MOP = 74
    WOD = 124
    Legion = 395
    BFA = 396
    """
    count = 0
    aze = zip(res['expansions'])
    for n in aze:  # tuple in list_tuple ?
        the_good_expansion = n[0]
        if the_good_expansion['expansion']['id'] == expansion_id:
            generator_all_encounters = find('encounters', the_good_expansion)
            for encounters in generator_all_encounters:
                for encounter_obj in encounters:
                    if encounter_obj['encounter']['id'] == boss_id:
                        count += encounter_obj['completed_count']
    return count


# <3
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
    # print(get_Ragna_done(All_char['Klehia']))
    print(get_for_all_char(get_Ragna_done))


token = get_token(tokenURL + credentials)
main()
