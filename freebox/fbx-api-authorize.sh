#!/bin/bash
#ecriture des donnees postees dans la demande d'enregistrement de l application
echo '{"app_id":"fr.glr.cacti","app_name":"Cacti script","app_version":"2.0.2.1","device_name":"Cacti"}' > /tmp/post.xml

#post de la demande
app_register=`wget --post-file=/tmp/post.xml http://mafreebox.freebox.fr/api/v1/login/authorize/ -qO-`

#recuperation du track_id
track_id="$(echo $app_register|awk -F: '{print $5}'|rev | cut -c 3-|rev)"

#recuperation du token
app_token="$(echo $app_register|awk -F\" '{print $8}')"

#recuperation du challenge
challenge_req=`wget http://mafreebox.freebox.fr/api/v1/login/authorize/$track_id -qO-`
challenge="$(echo $challenge_req|awk -F\" '{print $12}')"

#calcul du password
PW=`echo -n "$challenge" | openssl sha1 -hmac "$app_token"| cut -c 10-`

#DEBUG
#echo "app_register = $app_register"
#echo ""
#echo "track_id  = $track_id"
echo "app_token = $app_token"
#echo ""
#echo "challenge_req = $challenge_req"
#echo ""
#echo "challenge = $challenge"
#echo "PW        = $PW"
#echo ""

#ecriture des donnees a poster dans l autorisation de l application
echo "{\"app_id\":\"fr.glr.cacti\",\"password\":\"$PW\"}" > /tmp/post.xml

#post de la demande
curl -X POST -d `cat /tmp/post.xml` -H "Content-Type:application/json" http://mafreebox.freebox.fr/api/v1/login/session/
echo ""

#monitoring en attente de validation sur la BOX
while(true)
do
sleep 2
wget http://mafreebox.freebox.fr/api/v1/login/authorize/$track_id -qO-
echo ""
done

