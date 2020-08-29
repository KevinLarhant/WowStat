# Création token
tokenURL = 'https://us.battle.net/oauth/token?grant_type=client_credentials'
myOAuth = '2e7605b670ff412fb379e5ea706bca2f'
mySecret = '37oFLU6xjDwZ8DY6HDVSavGfhIUVJM0F'
credentials = f'&client_id={myOAuth}&client_secret={mySecret}'

# for requests
APIPath = 'https://eu.api.blizzard.com'
path_profile = '/profile/wow/character'
path_stats_raids = '/encounters/raids'
paramz = 'namespace=profile-eu&locale=en_US&access_token='
token = ''

# realm
dal = 'dalaran'
ys = 'ysondre'

# char
All_char = {
    'Akto': ('dalaran', 'aktø'),
    'Waktorr': ('dalaran', 'waktorr'),
    'Kishaa': ('dalaran', 'kishaa'),
    'Akkto': ('dalaran', 'akkto'),
    'Aktok': ('dalaran', 'aktok'),
    'Kyootie': ('dalaran', 'kyootie'),
    'Kylx': ('dalaran', 'kylx'),
    'Keanna': ('dalaran', 'keanna'),
    'Wakito': ('dalaran', 'wakito'),
    'Kboom': ('dalaran', 'kboom'),
    'Kaezia': ('dalaran', 'kaezia'),
    'Kamss': ('dalaran', 'kamss'),
    'Aktto': ('dalaran', 'aktto'),
    'Klehia': ('dalaran', 'klehia'),
    'Akto2_ys': ('ysondre', 'aktø'),
    'Kziin': ('ysondre', 'kziin'),
    'Akto_ys': ('ysondre', 'akto')
}
