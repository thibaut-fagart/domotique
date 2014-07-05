#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

import sharemem, time

#========== Programme principal =============
def thermostart():

  shm = sharemem.Globshm()

  shm.forceChaudiere = 1
  time.sleep(3)
  shm.forceChaudiere = 0

if __name__ == '__main__':
  thermostart()
