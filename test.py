import logging
from mininet.log import setLogLevel
from emuvim.dcemulator.net import DCNetwork
from emuvim.api.rest.rest_api_endpoint import RestApiEndpoint
from emuvim.api.tango import TangoLLCMEndpoint

logging.basicConfig(level=logging.DEBUG)
setLogLevel('info')  # set Mininet loglevel
logging.getLogger('werkzeug').setLevel(logging.DEBUG)
logging.getLogger('5gtango.llcm').setLevel(logging.DEBUG)


def create_topology():
    net = DCNetwork(monitor=True, enable_learning=True)
    # create two data centers
    dc1 = net.addDatacenter("dc1")
    dc2 = net.addDatacenter("dc2")
    # interconnect data centers
    net.addLink(dc1, dc2, delay="20ms")
    # add the command line interface endpoint to the emulated DC (REST API)
    rapi1 = RestApiEndpoint("0.0.0.0", 5001)
    rapi1.connectDCNetwork(net)
    rapi1.connectDatacenter(dc1)
    rapi1.connectDatacenter(dc2)
    rapi1.start()
    # add the 5GTANGO lightweight life cycle manager (LLCM) to the topology
    llcm1 = TangoLLCMEndpoint("0.0.0.0", 5000, deploy_sap=False)
    llcm1.connectDatacenter(dc1)
    llcm1.connectDatacenter(dc2)
    # run the dummy gatekeeper (in another thread, don't block)
    llcm1.start()
    # start the emulation and enter interactive CLI
    net.start()
    net.CLI()
    # when the user types exit in the CLI, we stop the emulator
    net.stop()


def main():
    create_topology()


if __name__ == '__main__':
    main()

