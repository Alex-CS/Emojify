#!/usr/bin/env python
# coding: utf-8
#
# Flask server
#
# Author: Alex Simonides

from flask import Flask, render_template
from flask.ext.restful import Api

from emojify import EmojiTranslation

app = Flask(__name__)

api = Api(app)

api.add_resource(EmojiTranslation, "/emojify")

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")


