#!/usr/bin/env python
#
import sys, os, signal
import optparse

# Make sure we use the local copy, not a system-wide one
sys.path.insert(0, os.path.dirname(os.getcwd()))
import netsnmpagent

prgname = sys.argv[0]

# Process command line arguments
parser = optparse.OptionParser()
parser.add_option(
        "-p",
        "--persistencedir",
        dest="persistencedir",
        help="Sets the path to the persistence directory",
        default="/var/lib/net-snmp"
)

parser.add_option(
	"-m",
	"--mastersocket",
	dest="mastersocket",
	help="Sets the transport specification for the master agent's AgentX socket",
	default="/var/agentx/master"
)
(options, args) = parser.parse_args()

# First, create an instance of the netsnmpAgent class. We specify the
# fully-qualified path to SCHUGART-MIB.txt ourselves here, so that you
# don't have to copy the MIB to /usr/share/snmp/mibs.
try:
        agent = netsnmpagent.netsnmpAgent(
                AgentName      = "SimpleAgent",
                MasterSocket   = options.mastersocket,
                PersistenceDir = options.persistencedir,
                MIBFiles       = [ "/usr/share/snmp/mibs/SCHUGART-MIB.mib" ]
        )
except netsnmpagent.netsnmpAgentException as e:
        print "{0}: {1}".format(prgname, e)
        sys.exit(1)

# Then we create all SNMP scalar variables we're willing to serve.
ampliCuisine = agent.Integer32(
        oidstr = "SCHUGART-MIB::ampliCuisine"
)
ampliSdb = agent.Integer32(
        oidstr = "SCHUGART-MIB::ampliSdb"
)
ampliChambre = agent.Integer32(
        oidstr = "SCHUGART-MIB::ampliChambre"
)
ampliSalon = agent.Integer32(
        oidstr = "SCHUGART-MIB::ampliSalon"
)
dht22ExtTemp = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22ExtTemp",
)
dht22ExtHum = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22ExtHum",
)
dht22CuisineTemp = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22CuisineTemp",
)
dht22CuisineHum = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22CuisineHum",
)
dht22SdbTemp = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22SdbTemp",
)
dht22SdbHum = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22SdbHum",
)
dht22SalonTemp = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22SalonTemp",
)
dht22SalonHum = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22SalonHum",
)
dht22PcTemp = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22PcTemp",
)
dht22PcHum = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22PcHum",
)
dht22ChambreTemp = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22ChambreTemp",
)
dht22ChambreHum = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22ChambreHum",
)
dht22ChambreEnfantTemp = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22ChambreEnfantTemp",
)
dht22ChambreEnfantHum = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22ChambreEnfantHum",
)
dht22CaveTemp = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22CaveTemp",
)
dht22CaveHum = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22CaveHum",
)
dht22ThermoOldTemp = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22ThermoOldTemp",
)
dht22ThermoOldHum = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22ThermoOldHum",
)
dht22ThermoNewTemp = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22ThermoNewTemp",
)
dht22ThermoNewHum = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22ThermoNewHum",
)
dht22SdbOldTemp = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22SdbOldTemp",
)
dht22SdbOldHum = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22SdbOldHum",
)
dht22SdbNewTemp = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22SdbNewTemp",
)
dht22SdbNewHum = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22SdbNewHum",
)
dht22RaspTemp = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22RaspTemp",
)
dht22RaspHum = agent.Integer32(
        oidstr   = "SCHUGART-MIB::dht22RaspHum",
)
edfAdco = agent.Integer32(
        oidstr   = "SCHUGART-MIB::edfAdco",
)
edfOptarif = agent.Integer32(
        oidstr   = "SCHUGART-MIB::edfOptarif",
)
edfIsousc = agent.Integer32(
        oidstr   = "SCHUGART-MIB::edfIsousc",
)
edfBase = agent.Integer32(
        oidstr   = "SCHUGART-MIB::edfBase",
)
edfIndexNormal = agent.Integer32(
        oidstr   = "SCHUGART-MIB::edfIndexNormal",
)
edfIndexPointe = agent.Integer32(
        oidstr   = "SCHUGART-MIB::edfIndexPointe",
)
edfPtec = agent.Integer32(
        oidstr   = "SCHUGART-MIB::edfPtec",
)
edfIinst = agent.Integer32(
        oidstr   = "SCHUGART-MIB::edfIinst",
)
edfIinst1 = agent.Integer32(
        oidstr   = "SCHUGART-MIB::edfIinst1",
)
edfIinst2 = agent.Integer32(
        oidstr   = "SCHUGART-MIB::edfIinst2",
)
edfIinst3 = agent.Integer32(
        oidstr   = "SCHUGART-MIB::edfIinst3",
)
edfImax = agent.Integer32(
        oidstr   = "SCHUGART-MIB::edfImax",
)
edfPapp = agent.Integer32(
        oidstr   = "SCHUGART-MIB::edfPapp",
)
edfPreavisEJP = agent.Integer32(
        oidstr   = "SCHUGART-MIB::edfPreavisEJP",
)
fuelBurningTime = agent.Integer32(
        oidstr   = "SCHUGART-MIB::fuelBurningTime",
)
fuelBurnt = agent.Integer32(
        oidstr   = "SCHUGART-MIB::fuelBurnt",
)
fuelRemaining = agent.Integer32(
        oidstr   = "SCHUGART-MIB::fuelRemaining",
)
ftpUser1 = agent.Integer32(
        oidstr   = "SCHUGART-MIB::ftpUser1",
)
ftpUser2 = agent.Integer32(
        oidstr   = "SCHUGART-MIB::ftpUser2",
)
ftpUser3 = agent.Integer32(
        oidstr   = "SCHUGART-MIB::ftpUser3",
)
ftpUser4 = agent.Integer32(
        oidstr   = "SCHUGART-MIB::ftpUser4",
)
ftpUser5 = agent.Integer32(
        oidstr   = "SCHUGART-MIB::ftpUser5",
)
ftpUser6 = agent.Integer32(
        oidstr   = "SCHUGART-MIB::ftpUser6",
)
# Finally, we tell the agent to "start". This actually connects the
# agent to the master agent.
try:
        agent.start()
except netsnmpagent.netsnmpAgentException as e:
        print "{0}: {1}".format(prgname, e)
        sys.exit(1)

# Install a signal handler that terminates our simple agent when
# CTRL-C is pressed or a KILL signal is received
def TermHandler(signum, frame):
	global loop
	loop = False
signal.signal(signal.SIGTERM, TermHandler)

loop = True
while (loop):
	agent.check_and_process()

