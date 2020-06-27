#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
os.environ['DND_DEBUG'] = "1"
from dnd.app import app


@app.route('/dnd')
def index():
    return 'DND'


if __name__ == '__main__':
    app.run(port=5002)


