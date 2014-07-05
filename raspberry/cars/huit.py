#!/usr/bin/env python

import memcache,random

shared = memcache.Client(['127.0.0.1:11211'], debug=0)

shared.set('Random', 1)

while  shared.get('Random') = 1:
	shared.set('Turn', random.uniform(-1,1))
	shared.set('Way', random.uniform(0,100))
	sleep(2)
