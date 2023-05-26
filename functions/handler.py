import os
import boto3
import psycopg2
import json

conn = psycopg2.connect(database="slack-grapher",
                        host="slack-grapher.cdgby7ohhzqb.eu-west-2.rds.amazonaws.com",
                        user="postgres",
                        password=os.environ['DB_PASSWORD'],
                        port="5432")

cursor = conn.cursor()

s3_client = boto3.client('s3')

def create_sql_string(item):
    columns = ['channel_id', 'name', 'is_channel', 'is_group', 'is_im', 'is_mpim',\
                'is_private', 'created', 'is_archived', 'is_general', 'unlinked',\
                'name_normalized', 'is_shared', 'is_org_shared', 'is_pending_ext_shared',\
                'context_team_id', 'updated', 'parent_conversation', 'creator', 'is_ext_shared',\
                'shared_team_ids', 'pending_connected_team_ids', 'is_member', 'topic', 'purpose', 'previous_names',\
                'num_members']
    values = []
    for column in columns:
        if column == 'channel_id':
            values.append(str(item['id']))
            continue
        if column in ('pending_shared', 'shared_team_ids', 'pending_connected_team_ids', 'previous_names'):
            values.append(f"ARRAY {item[column]}")
            continue
        if column in ('topic', 'purpose'):
            values.append("\'" + str(json.dumps(item[column])) + "\'")
            continue
        
        values.append(str(item[column]))

    sql_string = f"INSERT INTO channels ({', '.join(columns)}) VALUES ({', '.join(values)});"
    print(sql_string)
    return sql_string


def hello(event, context):
    for item in event['Items']:
        content_object = s3_client.get_object(Bucket='slack-data-store', Key=item['Key'])
        file_content = content_object['Body'].read().decode('utf-8')
        full_item = json.loads(file_content)

        if item['Key'].split('/')[0] == 'channels':
            sql_string = create_sql_string(full_item)
            cursor.execute(sql_string)


# TODO: extract info that is needed only - get rid of all data that is useless