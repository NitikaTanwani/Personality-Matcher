import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights
def analyze(handle):

twitter_consumer_key = 'Wm98zOnGshD29DgMQ2CO2GoCR'
twitter_consumer_secret = 'Bb20JDAVUvtjVWj3Ug4cMlLufnA7KStnPgUyUPvYZi7AfbpVK6'
twitter_access_token = '1715108394-WLWBsYtwBCJw10RUSG4T1jpoeLvWhI4OJoey0vj'
twitter_access_secret = '5y2kHNvjjIp9N4YW0yqIyiGbCiuRpFQnUhkk8dJ91ahGj'

twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret, access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)

#We user handle to get username and the twitter api and getUserTimeline is self explaintory

handle=""
#we get data in the form of list of tweets
statuses = twitter_api.GetUserTimeline(screen_name=handle, count=200, include_rts=False)

# using for loop to traverse the list of tweets as it does not only contains
#  tweets but also lot of meta data,to separate the textual part we use status.text
for status in statuses:
    print status.text

#concatenate the tweet text into a singe string,called complete_text,and we
#  only want tweets in english,so we filter by language also

complete_text = ""

for status in statuses:
    if (status.lang =='en'): #English tweets
        complete_text += status.text.encode('utf-8')

 #Using username and platform from cloud platform
pi_username = 'e899767a-c852-4d64-84a7-5d395263780a'
pi_password = 'pbao2oZxBiew'
#"username": "e899767a-c852-4d64-84a7-5d395263780a",
  #"password": "pbao2oZxBiew"

# It contains the details sent by PeronalityInsights api after analysis
personality_insights = PersonalityInsights(username=pi_username, password=pi_password)

#This is the main ANALYZE function,it return the personality insights in json format,it creates a tree structure for various categories,These categories are broken into personality,values,needs
#Analyze the body of text recieved via twitter
#pi_result = personality_insights.profile(complete_text)
      pi_result = personality_insights.profile(text)
      return pi_result
#The flatten() function below will flatten the JSON structure that the analyze() function returns from PI.
def flatten(orig):
    data = {}
    for c in orig['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                            for c4 in c3['children']:
                                if (c4['category'] == 'personality'):
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if (c3['category'] == 'personality'):
                                                data[c3['id']] = c3['percentage']
    return data
#The flatten() function flattens the results from a user and store the results in a dictionary.
# The next step is to write a function that can compare two dictionaries (the user's and the user2's).

user_handle = "@maggi_lover"
user2_handle = "@stanfordnlp"

def compare(dict1, dict2):
    compared_data = {}
    for keys in dict1:
        if dict1[keys] != dict2[keys]:
                compared_data[keys]=abs(dict1[keys] - dict2[keys])
    return compared_data

#So now we ue anaylze function to analyse data retrieved from twitter

user_result = analyze(user_handle)
user2_result = analyze(user2_handle)

#Flatten() flattens the JSON structure as returned by the analyze() function

user = flatten(user_result)
user2 = flatten(user2_result)

#Then, compare the results of the Watson PI API by calculating the distance between the prominent traits
compared_results = compare(user,user2)

#To display the top 10 results we willhave to sort them
sorted_result = sorted(compared_results.items(), key=operator.itemgetter(1))

#We need top 10 personality traits and the probability of displaying such traits
for keys, value in sorted_result[:10]:
    print keys,
    print(user[keys]),
    print ('->'),
    print (user2[keys]),
    print ('->'),
    print (compared_results[keys])

 """Test Cases
    user_handle = "@maggi_lover"
    user2_handle = "@standfordnlp"
Self-consciousness 0.756978752982 -> 0.801731081463 -> 0.0447523284805
Anger 0.681402439042 -> 0.741205817495 -> 0.0598033784526
Assertiveness 0.714228414883 -> 0.80565623803 -> 0.091427823147
Self-efficacy 0.716440272172 -> 0.860140556439 -> 0.143700284267
Artistic interests 0.571766190921 -> 0.421436826791 -> 0.15032936413
Depression 0.869943727317 -> 0.712507948778 -> 0.157435778539
Activity level 0.798959506887 -> 0.964009522253 -> 0.165050015366
Orderliness 0.0687571300015 -> 0.235141475335 -> 0.166384345334
Cooperation 0.346336878607 -> 0.538686607358 -> 0.192349728751
Immoderation 0.25934223229 -> 0.0430053689645 -> 0.216336863325"""

'''Test Case 2
user_handle="@maggi_lover"
user2_handle="@DrBrianWeiss"
Imagination 0.857298612993 -> 0.818000135107 -> 0.0392984778861
Sympathy 0.949104425296 -> 0.999118821646 -> 0.0500143963504
Altruism 0.931442777426 -> 0.999091159666 -> 0.0676483822396
Self-efficacy 0.716440272172 -> 0.793108934044 -> 0.0766686618724
Gregariousness 0.512068718281 -> 0.402703005314 -> 0.109365712967
Emotionality 0.882069075772 -> 0.997017324299 -> 0.114948248527
Assertiveness 0.714228414883 -> 0.906679939984 -> 0.192451525101
Activity level 0.798959506887 -> 0.992991164234 -> 0.194031657348
Modesty 0.553775824519 -> 0.753069803509 -> 0.199293978989
Immoderation 0.25934223229 -> 0.0485085555308 -> 0.210833676759'''

