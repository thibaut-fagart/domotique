#!/bin/sh

curl -X POST -i -H "Content-type: application/json" -X POST http://mafreebox.freebox.fr/api/v1/login/authorize/ -d '
{
   "app_id": "fr.glr.cacti",
   "app_name": "Cacti script",
   "app_version": "2.0.2.1",
   "device_name": "Cacti"
}'
