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

echo "Ampli Salon"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.30
echo "Ampli SdB"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.31
echo "Ampli Cuisine"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.32
echo "Ampli Chambre"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.33
echo "************************************************************"

echo "Porte"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.20
echo "Thermo"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.21
echo "************************************************************"

echo "Set TempEte"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.50
echo "Set VMC man"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.51
echo "Set Audio man"
snmpget -v 1 -r 1 -c public 192.168.0.70  1.3.6.1.4.1.36582.52
echo "************************************************************"
sleep 10
done
