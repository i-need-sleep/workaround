import os
import json
import random
import threading
import webbrowser
import urllib.request
import requests
import io
from io import StringIO

import numpy as np

from flask import Flask, render_template, request, session, url_for, redirect, flash, make_response, send_file
from flask_cors import CORS, cross_origin
import jinja2

import soundfile as sf
from scipy.io.wavfile import write

# Server Setup ###################################################################################################################
app = Flask(__name__)
app.jinja_options['variable_start_string'] = '[['
app.jinja_options['variable_end_string'] = ']]'
CORS(app)
app.secret_key = str(random.random())\

# The Main Thing ##################################################################################################################
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", demo = '')


# Route the audio requests to http://128.2.204.47:8001
# Such that the audio is played on the client side
# For example, /audio/test/test.mp3 will play the audio file test.mp3 in the folder test
count = 0
@app.route('/sdb_audio/<path:path>', methods=['GET'])
def sdb_audio(path):
    # Fetch the audio from 128.2.204.47:8001
    url = f'http://128.2.204.47:8001/{path}'
    print(f'Fetching audio from {url}')
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if download fails

    with io.BytesIO(response.content) as f:
        data, samplerate = sf.read(f)

    # Write the audio to a buffer
    global count
    idx = count % 50
    count += 1
    sf.write(f'./sdb_{idx}.wav', np.array(data, dtype=float), int(samplerate), format='WAV')
    
    # Return the audio file
    return send_file(f'./sdb_{idx}.wav', as_attachment=True)


count_data = 0
@app.route('/data_audio/<path:path>', methods=['GET'])
def data_audio(path):
    # Fetch the audio from 128.2.204.47:8002
    url = f'http://128.2.204.47:8002/{path}'
    print(f'Fetching audio from {url}')
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if download fails

    with io.BytesIO(response.content) as f:
        data, samplerate = sf.read(f)

    # Write the audio to a buffer
    global count_data
    idx = count_data % 50
    count_data += 1
    sf.write(f'./data_{idx}.wav', np.array(data, dtype=float), int(samplerate), format='WAV')
    
    # Return the audio file
    return send_file(f'./data_{idx}.wav', as_attachment=True)


if __name__ == '__main__':
    # threading.Timer(1.25, lambda: webbrowser.open("http://127.0.0.1:5000/", new=0, autoraise=True) ).start()
    print(os.getenv('PORT',5000))
    app.run(debug=False,port=os.getenv('PORT',5000))
