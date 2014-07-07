#!/usr/bin/env python

import memcache,time

shared = memcache.Client(['127.0.0.1:11211'], debug=0)
shared.set('Way', shared.get('neutralESC')+6)
time.sleep(0.6)
shared.set('Way', shared.get('neutralESC'))
