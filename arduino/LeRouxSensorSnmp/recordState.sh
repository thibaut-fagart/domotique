# ! /bin/sh
echo "burningTime_s"
snmpget -v 1 -r 1 -c public 109.190.53.51:10161  1.3.6.1.4.1.36582.10
echo "usedFuel_ml"
snmpget -v 1 -r 1 -c public 109.190.53.51:10161  1.3.6.1.4.1.36582.11
echo "remainingFuel_l"
snmpget -v 1 -r 1 -c public 109.190.53.51:10161  1.3.6.1.4.1.36582.12

