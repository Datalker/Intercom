from datetime import datetime
import requests
import re
import json
import copy

import settings as lset

output_fields = ['conversation_id', 'id', 'author_id', 'author_type', 'body',
                 'created_at', 'updated_at']

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

def download_conversations(app_id, api_key):
    r = requests.get(lset.url_list, headers=lset.headers, auth=(app_id, api_key))
    j = json.loads(r.text)
    print('Conversations: ', j)
    return j['conversations']


def date_in_range(item):
    dt = datetime.fromtimestamp(int(item['updated_at']))
    return dt > d_start and dt < d_end


def download_conversation_parts(conversation_id, app_id, api_key):
    url = lset.url_item.replace('[ID]', conversation_id)
    r = requests.get(url, headers=lset.headers, auth=(app_id, api_key))
    j = json.loads(r.text)
    conv_parts = j['conversation_parts']['conversation_parts']
    for c in conv_parts: c['conversation_id'] = conversation_id
    return conv_parts


def prepare_conv_parts(conv_parts, output='dict'):
    conv_parts_local = copy.deepcopy(conv_parts)
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
        cp['body'] = remove_tags(cp['body'] )
    # output data
    if output == 'csv':
        result = ','.join(output_fields) # header line
        for cp in conv_parts_local:
            result = result + '\n'
            for f in output_fields:
                result = result + cp[f] + ','
            result = result[:-1]  #cutting out the last comma
    if output ==  'dict':
        result = conv_parts_local
    return result

#  Execution

def get_conversation_parts(from_date, to_date, app_id, api_key):
    conv_all = download_conversations(app_id, api_key)
    conv_all_filtered = []

    for c in conv_all:
        dt = datetime.fromtimestamp(int(c['updated_at']))
        if dt > from_date and dt < to_date:
            conv_all_filtered.append(c)

    conv_parts_all = []
    for c in conv_all:
        conv_parts = download_conversation_parts(c['id'], app_id, api_key)
        conv_parts_filtered = []
        for c in conv_parts:
            dt = datetime.fromtimestamp(int(c['updated_at']))
            if dt > from_date and dt < to_date:
                conv_parts_filtered.append(c)
        conv_parts_all = conv_parts_all + conv_parts_filtered

    return conv_parts_all

if __name__ == '__main__':
    conv_parts = get_conversation_parts(from_date=datetime(2016, 4, 12),
            to_date=datetime(2016, 8, 12), app_id=lset.app_id,
            api_key=lset.api_key)
    print(prepare_conv_parts(conv_parts, output='dict'))
