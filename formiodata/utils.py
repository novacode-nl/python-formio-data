# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import base64
import requests
import tempfile

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
