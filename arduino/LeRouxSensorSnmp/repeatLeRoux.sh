for i in {1..100}
do
snmpget -v 1 -r 1 -c public 109.190.53.51:10161  1.3.6.1.4.1.36582.$1
sleep 1
done
