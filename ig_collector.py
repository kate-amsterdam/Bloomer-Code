"""
How to run this python script!
- Open terminal
- cd /Users/katehudson/code/bloomer_work/data_collection
- python3 ig_collector.py <start_time> <end_time> <metric_name>
Example python3 ig_collector.py '2024-01-01' '2024-06-01' list_media_all_metrics


1. Scope: Write code to collect all posts on our instagram account by 
calling the API (<ig-user-id>/media endpoint) and then print it out (in the future, we can replace "print out" with "write to a DB")

2. Input / Output
Input:
       1) start_time (the start timestamp of the collection)
       2) end_time (the end timestamp of the collection)
       3) metric_name (list_media)
Output:
        - For starting, let's just print the data out!

Example: python3 ig_collector.py '2024-01-01' '2024-06-01' list_media_all_metrics

completed functions so far: 
-follower_location
-engaged_audience_gender
-follows_unfollows
-profile_list_metrics
-follower_age_gender
-follower_location
-list_media_all_metrics
-

"""
import sys
from datetime import datetime, timezone
import requests
import json

#constants
MAX_LIMIT = 10000
BLOOMER_USER_ID = '17841403267966216'
USER_TOKEN = 'EAAFYE3XftlQBO8DkIDPG8lqSbyb0yqGXgvuOR0SpO8VnGzhTXKVEzh7sjVcoTWosZC1dKyZCuscM6SQRT02ZBobPEXRtDSZCL0cyjeXDZBdInIiRDsjzko3Mt9I3P8bNC89hfLVrDHNoOio5lkKb2j6fhD4XrtdtylxLsT7ffMtZAQFgbim1k0vYjL5UCAJLApTo8qrME2V46huUup'

#

#reached location
def reached_location():
    url = f"https://graph.facebook.com/v20.0/{BLOOMER_USER_ID}/insights"
    headers = {"Authorization": f"Bearer {USER_TOKEN}"}
    params = {
        'metric' : 'reached_audience_demographics',
        'breakdown' : 'city',
        'metric_type' : 'total_value',
        'period' : 'lifetime', 
        'timeframe' : 'this_month'
    }
    data = requests.get(url, headers=headers, params=params).json()
    return data

#reached_age_gender: The demographic characteristics of the reached audience
def reached_age_gender():
    url = f"https://graph.facebook.com/v20.0/{BLOOMER_USER_ID}/insights"
    headers = {"Authorization": f"Bearer {USER_TOKEN}"}
    breakdown = ['age', 'gender']
    params = {
        'metric' : 'reached_audience_demographics',
        'breakdown' : ','.join(breakdown),
        'metric_type' : 'total_value',
        'period' : 'lifetime', 
        'timeframe' : 'this_month'
    }
    data = requests.get(url, headers=headers, params=params).json()
    return data 


#follower_age_gender
def follower_age_gender():
    url = f"https://graph.facebook.com/v20.0/{BLOOMER_USER_ID}/insights"
    headers = {"Authorization": f"Bearer {USER_TOKEN}"}
    breakdown = ['age', 'gender']
    params = {'metric' : 'follower_demographics',
              'breakdown' : ','.join(breakdown),
              'metric_type' : 'total_value',
              'period' : 'lifetime',
              'timeframe' : 'this_month'
              }
    data = requests.get(url, headers=headers, params=params).json()
    return data

#location of followers 
def follower_location():
    url = f"https://graph.facebook.com/v20.0/{BLOOMER_USER_ID}/insights"
    headers = {"Authorization": f"Bearer {USER_TOKEN}"}
    params = {'metric' : 'follower_demographics',
              'breakdown' : 'city',
              'metric_type' : 'total_value',
              'period' : 'lifetime',
              'timeframe' : 'this_month'
              }
    data = requests.get(url, headers=headers, params=params).json()
    return data

#location of engaged audience
def engaged_audience_location():
    url = f"https://graph.facebook.com/v20.0/{BLOOMER_USER_ID}/insights"
    headers = {"Authorization": f"Bearer {USER_TOKEN}"}
    params = {'metric' : 'engaged_audience_demographics',
              'breakdown' : 'city',
              'metric_type' : 'total_value',
              'period' : 'lifetime',
              'timeframe' : 'this_month'
              }
    data = requests.get(url, headers=headers, params=params).json()
    return data

#engaged_audience_gender The demographic characteristics of the engaged audience
    #TIMEFRAME == 'THIS_MONTH'  used to take other arguments but they are all expiring with v.20
def engaged_audience_gender_age():
    url = f"https://graph.facebook.com/v20.0/{BLOOMER_USER_ID}/insights"
    headers = {"Authorization": f"Bearer {USER_TOKEN}"}
    breakdown= ['age','gender']
    params = {'metric' : 'engaged_audience_demographics',
              'breakdown' : ','.join(breakdown),
              'metric_type' : 'total_value',
              'period' : 'lifetime',
              'timeframe' : 'this_month'
              }
    data = requests.get(url, headers=headers, params=params).json()
    return data

#follows_unfollows number of follows and unfollows on a given day, only accepts day, though it seems it should support month, 28 day and week but those paramters cause an error
"""
fixed error
"""
def follows_unfollows(start_time, end_time):
    url = f"https://graph.facebook.com/v20.0/{BLOOMER_USER_ID}/insights"
    headers = {"Authorization": f"Bearer {USER_TOKEN}"}
    params={'metric': 'follows_and_unfollows',
            'metric_type' : 'total_value',
            'period' : 'day',
            'since' : start_time,
            'until' : end_time,
            'breakdown' : 'follow_type'
            }
    data = requests.get(url, headers=headers, params= params).json()
    return data

#profile_list_metrics, gets email_contacts, follower_count, get_directions_clicks, impressions, phone_call_clicks, profile_views, reach, text_message_clicks, website_clicks per day
#most of these params are only available with the period being 'day'
def profile_insights(start_time, end_time):
    url = f"https://graph.facebook.com/v20.0/{BLOOMER_USER_ID}/insights"
    headers = {"Authorization": f"Bearer {USER_TOKEN}"} 
    metric_list = ['email_contacts', 'follower_count', 'get_directions_clicks', 'impressions', 'phone_call_clicks', 'profile_views', 'reach', 'text_message_clicks', 'website_clicks']
    params = {'metric' : ','.join(metric_list),
              'period' :'day',
              'since' : start_time,
              'until' : end_time
              }
    data = requests.get(url, headers=headers, params=params).json()
    return data
    

# get follower age, gender
def follower_age_gender():
   url = f"https://graph.facebook.com/v20.0/{BLOOMER_USER_ID}/insights"
   headers = {"Authorization": f"Bearer {USER_TOKEN}"} 
   breakdown = ['age','gender']
   params = {
       'metric' : 'follower_demographics',
       'metric_type' : 'total_value',
       'period' : 'lifetime',
       'breakdown' : ','.join(breakdown)
   }
   data = requests.get(url, headers=headers, params=params).json()
   return data

# gets lifetime follower location demographics 
def follower_location():
    url = f"https://graph.facebook.com/v20.0/{BLOOMER_USER_ID}/insights"
    headers = {"Authorization": f"Bearer {USER_TOKEN}"}
    params = {
        'metric' : 'follower_demographics',
        'metric_type' : 'total_value',
        'period' : 'lifetime',
        'breakdown' : 'city'
        
    }
    data = requests.get(url,headers=headers, params=params).json()
    return data

#returns metrics per post
def list_media(start_time, end_time):
    """
    Calls /<ig-user-id>/media endpoint, gets all metrics
    with since=start_time,until=end_time.
    Returns JSON result
    """
    url = f"https://graph.facebook.com/v20.0/{BLOOMER_USER_ID}/media"
    headers = {"Authorization": f"Bearer {USER_TOKEN}"}

    params = {
        "since": start_time,
        "until": end_time,
        "limit": MAX_LIMIT,
        "fields": "timestamp,media_type,media_product_type,media_url,caption,is_comment_enabled"
    }

    data = requests.get(url, headers=headers, params=params).json()
    return data

def parse_timestamp(timestamp_str):
    # parse provided time into datetime object, return unix
    # expects timestamp in '2024-01-01' format
    try:
        time_dt = datetime.strptime(timestamp_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    except:
        print("You inputted an invalid date. Please use 'YYYY-MM-DD' (ex. 2024-01-01)")
        raise Exception("Invalid date")

    return int(time_dt.timestamp())

def main():
    """
    1) gets and parses the input
    2) calls the API
    3) print out the results
    """
    # We expect 3 inputs, start_time, end_time, metric_name
    start_time, end_time, metric_name = sys.argv[1], sys.argv[2], sys.argv[3]

    start_time_unix = parse_timestamp(start_time) 
    end_time_unix = parse_timestamp(end_time) 

    data = ''
    if metric_name == 'list_media':
        data = list_media(start_time_unix, end_time_unix)
    elif metric_name == 'follower_location':
        data =  follower_location()
    elif metric_name == 'follower_age_gender':
        data = follower_age_gender()
    elif metric_name == 'profile_insights':
        data = profile_insights(start_time_unix, end_time_unix)
    elif metric_name == 'follows_unfollows':
        data = follows_unfollows(start_time_unix, end_time_unix)
    elif metric_name == 'engaged_audience_gender_age':
        data = engaged_audience_gender_age()
    elif metric_name == 'engaged_audience_location':
        data = engaged_audience_location()
    elif metric_name == 'reached_age_gender':
        data = reached_age_gender()
    elif metric_name == 'reached_location':
        data = reached_location()
    elif metric_name == 'media_insights':
        data = media_insights(start_time_unix, end_time_unix)
    else:
        print("Unsupported metric name")
        return
    # OUTPUT
    print(json.dumps(data, indent=2))


def media_insights(start_time_unix, end_time_unix):
    #get all media_ids between start and end time, 
    all_media = list_media(start_time_unix, end_time_unix)
    media_list = all_media['data']

    insights = {}
    for current_media in media_list:
        # called 50 times if there are 50 medias
        curr_media_id = current_media['id']
        current_insights = get_media_insights(curr_media_id)
        print(f"Calling insights on media {curr_media_id}")
        insights[curr_media_id] = current_insights

    return insights


def get_media_insights(media_id):
    url = f"https://graph.facebook.com/v20.0/{media_id}/insights"
    headers = {"Authorization": f"Bearer {USER_TOKEN}"}
    metric_values = ['comments', 'follows', 'likes','profile_visits', 'shares', 'total_interactions']
    params = {'metric': ','.join(metric_values)}
    print(f"Get request on <media-id>/insights endpoint: url: {url}, params: {params}")
    resp = requests.get(url, headers=headers, params = params).json()
    if 'error' in resp:
        print("Error getting media insights: {}".format(resp['error']))
        return None
    else:
        return resp['data']


if __name__ == "__main__":
    main()


''' 
next we need to build a function to get metrics on all posts that are  only available for one post at a time using the api
could we create a variable for all instagram post_ids?

'''