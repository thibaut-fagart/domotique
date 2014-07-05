#!/usr/bin/env python

import memcache

shared = memcache.Client(['127.0.0.1:11211'], debug=0)
shared.set('Random', 0) 
shared.set('Turn', 0.5)
shared.set('Way', 1)
