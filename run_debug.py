#!/usr/bin/env python3os.environ['DND_DEBUG'] = "0"
# -*- coding: utf-8 -*-
import os
os.environ['DND_ENV'] = "DEVELOPMENT"
from dnd.app import app


@app.route('/')
def index():
    return 'DND'


if __name__ == '__main__':
    app.run(port=5005)
