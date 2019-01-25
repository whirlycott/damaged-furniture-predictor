#!/usr/bin/env python

import time
import hashlib
import random
from flask import Flask, jsonify
from scipy.stats import lognorm

# Settings: mean/stddev delivery time (days)
mean_delivery_time = 5
stddev = 3

app = Flask(__name__)

@app.route('/predict/<string:zip_code>/<string:sku_id>')
def predict(zip_code, sku_id):

    hash = hashlib.sha1()
    hash.update(('%s %s' % (zip_code, sku_id)).encode('utf-8'))
    offset = int(hash.hexdigest(), 16) % 100

    dist = lognorm([stddev],loc=mean_delivery_time)

    # Base est delivery (secs)
    base_secs = dist.cdf(range(0, 100))[offset] * 86400

    # Add some jitter like it's going out of style
    jitter_secs = random.randint(-9, 13) * 3600

    predicted = int(time.time()) + base_secs + jitter_secs

    predicted_readable = time.strftime('%Y%m%d', time.localtime(predicted))

    return jsonify({
        'predicted_delivery_date': predicted_readable,
        })
