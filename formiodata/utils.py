# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import base64
import requests
import tempfile
import re


def base64_encode_url(url):
    content = requests.get(url).content
    tf = tempfile.TemporaryFile()
    tf.write(content)
    tf.seek(0)
    b64encode = base64.b64encode(tf.read())
    tf.close()
    # prefix and decode bytes to str
    b64encode = '%s,%s' % ('data:image/png;base64', b64encode.decode())
    return b64encode


def decode_resource_template(tmp):
    res = re.sub(r"<.*?>", " ", tmp)
    strcleaned = re.sub(r'\{{ |\ }}', "", res)
    list_kyes = strcleaned.strip().split(".")
    return list_kyes[1:]


def fetch_dict_get_value(dict_src, list_keys):
    if len(list_keys) == 0:
        return
    node = list_keys[0]
    list_keys.remove(node)
    nextdict = dict_src.get(node)
    if len(list_keys) >= 1:
        return fetch_dict_get_value(nextdict, list_keys)
    else:
        return dict_src.get(node)
