#!/usr/bin/env python

import memcache

shared = memcache.Client(['127.0.0.1:11211'], debug=0)
shared.set('Way', 70)
time.sleep(0.05)
shared.set('Way', 50)
