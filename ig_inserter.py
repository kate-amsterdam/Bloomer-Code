
import sys
from ig_collector import parse_timestamp,list_media,get_media_insights
import boto3
import uuid
import json
from datetime import datetime

REGION = "us-west-2"
DYNAMO_DB_ENDPOINT = f"https://dynamodb.{REGION}.amazonaws.com"
MEDIA_TABLE_NAME = 'ig_media'
MEDIA_INSIGHTS_TABLE_NAME = 'ig_media_insights'


def insert_items(table_name, items):
    """
    Given a list of JSON objects, insert them into a dynamodb table
    """
    # TODO use BatchWriteAPI instead of for loop
    dynamodb = boto3.resource('dynamodb', endpoint_url=DYNAMO_DB_ENDPOINT, region_name=REGION)

    table = dynamodb.Table(table_name)
    print(f"Got table {table_name} from dyanmodb")

    count = 0
    for item in items:
        print(f"Inserting item {count}")
        resp = table.put_item(
            Item=item
        )
        if resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
            print("Failed to insert item {}: {}".format(item, resp))
        else:
            count += 1

    print(f"Successfully inserted {count} items!")


def scan_all_items(table_name):
    dynamodb = boto3.resource('dynamodb', endpoint_url=DYNAMO_DB_ENDPOINT, region_name=REGION)
    table = dynamodb.Table(table_name)
    resp = table.scan()
    items = resp['Items']
    while 'LastEvaluatedKey' in resp:
        print("Paginating scan from {}".format(resp['LastEvaluatedKey']))
        resp = table.scan(ExclusiveStartKey=resp['LastEvaluatedKey'])
        items.extend(resp['Items'])

    return items


def update_media_insights():
    """
    Fetches new insights for all media currently in the ig_media table.
    Then, inserts those new insights into the ig_media_insights table
    """
    media_list = scan_all_items(MEDIA_TABLE_NAME)
    #media_list = list_media(parse_timestamp('2024-06-01'), parse_timestamp('2024-06-15'))['data']
    collection_timestamp = datetime.now()

    count = 0
    all_items = []
    for media in media_list:
        curr_insights = get_media_insights(media['id'])
        if (curr_insights):
            items = parse_insights_to_items(collection_timestamp, media['id'], curr_insights)
            all_items.extend(items)

    insert_items(MEDIA_INSIGHTS_TABLE_NAME, all_items)


def parse_insights_to_items(collection_timestamp, media_id, insights):
    """
    Parse insights into list of structures in the format:
    {
        "pk": <random UUID value>
        "media_id": <>
        "collection_timestamp": <>
        "insight_type": <>
        "description: <>
        "value": <>
    }
    """
    items = []
    for entry in insights:
        items.append({
            "pk": str(uuid.uuid4()),
            "media_id": media_id,
            "collection_timestamp": collection_timestamp.isoformat(),
            "insight_type": entry.get("name"),
            "description": entry.get("description"),
            "value": entry.get("values")[0].get("value")
        })
    return items



if __name__ == '__main__':
    operation = sys.argv[1]

    start_time,end_time = '',''
    if (len(sys.argv) == 4):
        start_time = parse_timestamp(sys.argv[2])
        end_time = parse_timestamp(sys.argv[3])

    if operation == 'insert_media':
        # ensure start_time and end_time were parsed
        assert(start_time and end_time)
        media_to_insert = list_media(start_time, end_time)['data']
        insert_items(MEDIA_TABLE_NAME, media_to_insert)
    elif operation == 'update_media_insights':
        update_media_insights()



