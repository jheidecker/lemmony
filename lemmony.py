import requests

# enter your local instance, username and password here (probably use a bot account?)
local_instance = 'lemmy.management'
username = 'fed_sub_bot'
password = 'bVtwxF92QDeeZK'

# get global communities from feddit.de and store in list
print('fetching global communities from feddit.de...')
community_list = requests.get('https://browse.feddit.de/communities.json')
#print(community_list.status_code)
community_actors = []
for community in community_list.json():
    #some instances are not federated but are in the feddit list, so we skip because they always fail
    if community['counts']['posts'] > 0 and not community['community']['actor_id'].startswith('https://www.hexbear.net') and not community['community']['actor_id'].startswith('https://bbs.9tail.net') and not community['community']['actor_id'].startswith('https://thevapor.space') and not community['community']['actor_id'].startswith('https://baomi.tv'):
        community_actors.append(community['community']['actor_id'])

# store total number of communities from feddit.de
community_count = str(len(community_actors))
print('got ' + community_count + ' non-empty communities.')

# create new session object for local instance
curSession = requests.Session()
 
# login and get jwt token
payload='{"username_or_email": "'+username+'","password": "'+password+'"}'
print('logging in to ' + local_instance + ' as ' + username + '...')
login_resp = curSession.post('https://'+local_instance+'/api/v3/user/login', data=payload, headers={"Content-Type": "application/json"})
#print(login_resp.status_code)
auth_token = login_resp.json()['jwt']

# get local communities and store in list
print('enumerating all local communities (this might take a while)...')
local_community_id_list = []
local_community_actor_id_list = []
new_results = True
page = 1
while new_results:
    actor_resp = curSession.get('https://'+local_instance+'/api/v3/community/list?type_=All&limit=50&page=' + str(page), headers={"Cookie": "jwt=" + auth_token})
    if actor_resp.json()['communities'] != []:
        for community in actor_resp.json()['communities']:
            local_community_id_list.append(community['community']['id'])
            local_community_actor_id_list.append(community['community']['actor_id'])
        page += 1
    else:
        new_results = False

# add remote communities to local communities via. search
print('adding new global communities > local instance (this will take a while)...')
for idx, actor_id in enumerate(community_actors, 1):
    if actor_id not in local_community_actor_id_list:
        actor_resp = curSession.get('https://'+local_instance+'/search?q=' + actor_id + '&type=All&listingType=All&page=1&sort=TopAll', headers={"Cookie": "jwt=" + auth_token})
        print(str(idx) + "/" + community_count + " " + actor_id + ": " + str(actor_resp.status_code))
    else:
        print(str(idx) + "/" + community_count + " " + actor_id + ": already exists")

# re-fetch communities ready for subscription
print('re-fetching communities ready for subscription (this might take a while)...')
local_community_id_list = []
new_results = True
page = 1
while new_results:
    actor_resp = curSession.get('https://'+local_instance+'/api/v3/community/list?type_=All&limit=50&page=' + str(page) + '&auth=' + auth_token, headers={"Content-Type": "application/json"})
    if actor_resp.json()['communities'] != []:
        for community in actor_resp.json()['communities']:
            if community['subscribed'] == 'Subscribed':
                pass
            else:
                local_community_id_list.append(community['community']['id'])
        page += 1
    else:
        new_results = False

# store and display total number of local communities
local_community_count = str(len(local_community_id_list))
print('found ' + local_community_count + ' communities to subscribe to.')

# subscribe user to all local communities
print('subscribing ' + username + ' to communities (this will take a while)...')
for idx, community_id in enumerate(local_community_id_list, 1):
    sub_resp = curSession.post('https://'+local_instance+'/api/v3/community/follow', data='{"community_id": ' + str(community_id) + ', "follow": true, "auth": "' + auth_token + '"}', headers={"Cookie": "jwt=" + auth_token, "Content-Type": "application/json"})
    print(str(idx) + "/" + local_community_count + " " + str(community_id) + ": " + str(sub_resp.json()['community_view']['subscribed']))

print('done.')