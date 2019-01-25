#!/usr/bin/env python

import time
import hashlib
import random
from flask import Flask, jsonify
from scipy.stats import lognorm

# Settings: mean/stddev delivery time (days)
mean_delivery_time = 7
stddev = 3

app = Flask(__name__)

@app.route('/predict/<string:zip_code>/<string:sku_id>')
def predict(zip_code, sku_id):

    # Real AI takes at least 3 seconds.
    time.sleep(random.randint(3, 5))

    # Find a consistent number based on the params.
    hash = hashlib.sha1()
    hash.update(('%s %s' % (zip_code, sku_id)).encode('utf-8'))
    offset = int(hash.hexdigest(), 16) % 100

    # Deep learning
    dist = lognorm([stddev],loc=mean_delivery_time)

    # Base est delivery (secs)
    base_secs = dist.cdf(offset) * 86400

    # Add some jitter like it's going out of style
    jitter_secs = random.randint(-9, 13) * 3600

    predicted = int(time.time()) + mean_delivery_time * 86400 + base_secs + jitter_secs

    return jsonify({
        'predicted_delivery_date': time.strftime('%Y%m%d', time.localtime(predicted)),
        })
