for i in {1..10}
do
echo "Ventilo couloire 1"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.10
echo "Ventilo couloire 2"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.11
echo "Ventilo couloire speed"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.12

echo "Ventilo SdB 1"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.15
echo "Ventilo SdB 2"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.16
echo "Ventilo SdB speed"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.17

echo "VMC"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.40
echo "************************************************************"

echo "hum SdB"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.6
echo "hum Salon"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.2
echo "temp Ext"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.7
echo "temp Ete"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.50
echo "************************************************************"
sleep 10
done
