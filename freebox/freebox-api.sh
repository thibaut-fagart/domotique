#!/bin/bash

# by GLR <blog.glrnet.fr>
# version 2.0.2.1


MY_APP_ID="fr.glr.cacti"
MY_APP_TOKEN="ePjskFNclq4n96yutEABJ1e+8w68oN3BZsoajSju+CWtmuJ2lJyAIoSVke4A+rxv"
CACTI_PATH=/usr/share/cacti

source $CACTI_PATH/scripts/freeboxos_bash_api.sh

login_freebox "$MY_APP_ID" "$MY_APP_TOKEN"

cnx=$(call_freebox_api '/connection/')
xdsl=$(call_freebox_api '/connection/xdsl')

#clear
#echo
#echo cnx=$cnx
#echo
#echo xdsl=$xdsl
#echo

bytes_up=`echo $cnx | cut -d':' -f6 | cut -d',' -f1`
bytes_down=`echo $cnx | cut -d':' -f18 | cut -d',' -f1`
bw_up=`echo $cnx | cut -d':' -f8 | cut -d',' -f1`
bw_down=`echo $cnx | cut -d':' -f15 | cut -d',' -f1`

uptime=`echo $xdsl | cut -d':' -f7 | cut -d',' -f1`

down_es=`echo $xdsl | cut -d':' -f10 | cut -d',' -f1`
down_attn=`echo $xdsl | cut -d':' -f12 | cut -d',' -f1`
down_snr=`echo $xdsl | cut -d':' -f13 | cut -d',' -f1`
down_rate=`echo $xdsl | cut -d':' -f15 | cut -d',' -f1`
down_hec=`echo $xdsl | cut -d':' -f16 | cut -d',' -f1`
down_crc=`echo $xdsl | cut -d':' -f17 | cut -d',' -f1`
down_rxmt_uncorr=`echo $xdsl | cut -d':' -f18 | cut -d',' -f1`
down_rxmt_corr=`echo $xdsl | cut -d':' -f19 | cut -d',' -f1`
down_ses=`echo $xdsl | cut -d':' -f20 | cut -d',' -f1`
down_fec=`echo $xdsl | cut -d':' -f21 | cut -d',' -f1`
down_maxrate=`echo $xdsl | cut -d':' -f22 | cut -d',' -f1`
down_rxmt=`echo $xdsl | cut -d':' -f23 | cut -d',' -f1 | cut -d'}' -f1`

up_es=`echo $xdsl | cut -d':' -f25 | cut -d',' -f1`
up_attn=`echo $xdsl | cut -d':' -f27 | cut -d',' -f1`
up_snr=`echo $xdsl | cut -d':' -f28 | cut -d',' -f1`
up_rate=`echo $xdsl | cut -d':' -f30 | cut -d',' -f1`
up_hec=`echo $xdsl | cut -d':' -f31 | cut -d',' -f1`
up_crc=`echo $xdsl | cut -d':' -f32 | cut -d',' -f1`
up_rxmt_uncorr=`echo $xdsl | cut -d':' -f33 | cut -d',' -f1`
up_rxmt_corr=`echo $xdsl | cut -d':' -f34 | cut -d',' -f1`
up_ses=`echo $xdsl | cut -d':' -f35 | cut -d',' -f1`
up_fec=`echo $xdsl | cut -d':' -f36 | cut -d',' -f1`
up_maxrate=`echo $xdsl | cut -d':' -f37 | cut -d',' -f1`
up_rxmt=`echo $xdsl | cut -d':' -f38 | cut -d',' -f1 | cut -d'}' -f1`

printf "bytes_up:%s bytes_down:%s bw_up:%s bw_down:%s down_es:%s down_attn:%s down_snr:%s down_rate:%s down_hec:%s down_crc:%s down_rxmt_uncorr:%s down_rxmt_corr:%s down_ses:%s down_fec:%s down_maxrate:%s down_rxmt:%s up_es:%s up_attn:%s up_snr:%s up_rate:%s up_hec:%s up_crc:%s up_rxmt_uncorr:%s up_rxmt_corr:%s up_ses:%s up_fec:%s up_maxrate:%s up_rxmt:%s uptime:%s\n" $bytes_up $bytes_down $bw_up $bw_down $down_es $down_attn $down_snr $down_rate $down_hec $down_crc $down_rxmt_uncorr $down_rxmt_corr $down_ses $down_fec $down_maxrate $down_rxmt $up_es $up_attn $up_snr $up_rate $up_hec $up_crc $up_rxmt_uncorr $up_rxmt_corr $up_ses $up_fec $up_maxrate $up_rxmt $uptime
