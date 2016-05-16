from datetime import datetime
import requests
import json

usr = 'tgv7x1m3'
passw = 'ro-29475fef0ab42ef8444a7a404109968163b5b9c8'
headers = {'Accept': 'application/json'}
url_list = 'https://api.intercom.io/conversations'
url_item = 'https://api.intercom.io/conversations/[ID]?display_as=plaintext'
output_fields = ['conversation_id', 'id', 'author_id', 'author_type', 'body',
                 'created_at', 'updated_at']
d_start = datetime(2016, 4, 12)
d_end = datetime(2016, 10, 10)


def get_conversations():
    r = requests.get(url_list, headers=headers, auth=(usr, passw))
    j = json.loads(r.text)
    return j['conversations']


def date_in_range(item):
    dt = datetime.fromtimestamp(int(item['updated_at']))
    return dt > d_start and dt < d_end


def get_conversation_parts(conversation_id):
    url = url_item.replace('[ID]', conversation_id)
    r = requests.get(url, headers=headers, auth=(usr, passw))
    j = json.loads(r.text)
    conv_parts = j['conversation_parts']['conversation_parts']
    for c in conv_parts: c['conversation_id'] = conversation_id
    return conv_parts


def output_conv_part(conv_parts):
    conv_parts_local = conv_parts[:]
    # prepare data for output

    def date_from_stamp(st):
        return datetime.fromtimestamp(int(st)).strftime('%Y-%m-%d %H:%M:%S')

    for cp in conv_parts_local:
        cp['updated_at'] = date_from_stamp(cp['updated_at'])
        cp['created_at'] = date_from_stamp(cp['created_at'])
        cp['notified_at'] = date_from_stamp(cp['notified_at'])
        cp['author_id'] = cp['author']['id']
        cp['author_type'] = cp['author']['type']
        del cp['author']
        cp['body'] = cp['body'] if cp['body'] else ''
        cp['body'] = cp['body'].replace('"','""')
        cp['body'] = cp['body'].replace('\n','<new line>')
        cp['body'] = '"' + cp['body'] + '"'

    # output data
    print(','.join(output_fields), end='')  # print header line
    for cp in conv_parts_local:
        print('')
        for f in output_fields:
            print(cp[f], end=',')

#  Execution
conv_all = filter(date_in_range, get_conversations())
conv_parts_all = []
for c in conv_all:
    conv_parts = filter(date_in_range, get_conversation_parts(c['id']))
    conv_parts_all = conv_parts_all + list(conv_parts)
output_conv_part(conv_parts_all)


