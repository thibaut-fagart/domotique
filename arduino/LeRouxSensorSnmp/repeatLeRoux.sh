for i in {1..10}
do
snmpget -v 1 -r 1 -c public 192.168.1.99 1.3.6.1.4.1.36582.0
sleep 1
done
