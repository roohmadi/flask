# -*- coding: utf-8 -*-
"""
Created on Mon May 13 13:58:29 2024

@author: MAT-Admin
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"

if __name__ == '__main__':
    app.run(debug=True)