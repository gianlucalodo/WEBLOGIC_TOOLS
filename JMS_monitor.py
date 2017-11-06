# authentication parameter
userConfigFile = Path+"/.profile/.myuserconfigfile.secure"
userKeyFile = Path+"/.profile/.myuserkeyfile.secure"
url = "t3s://<admin_server_url>:<admin_server_port>"
connect(userConfigFile=userConfigFile, userKeyFile=userKeyFile, url=url ,timeout='20000')

servers = domainRuntimeService.getServerRuntimes();
if (len(servers) > 0):
        print "+-----------------------------------------------------------------------------------------------------------------------------------------------------------+------------+"
        print "| QUEUE                                                                                                                                                     |  MESSAGES  |"
        print "+-----------------------------------------------------------------------------------------------------------------------------------------------------------+------------+"      
        for server in servers:
                        jmsRuntime = server.getJMSRuntime();
                        jmsServers = jmsRuntime.getJMSServers();
                        for jmsServer in jmsServers:
                                destinations = jmsServer.getDestinations();
                                for destination in destinations:
                                        print "|%-155s|%11s |" % (destination.getName(),destination.getMessagesCurrentCount()) 
        print "+-----------------------------------------------------------------------------------------------------------------------------------------------------------+------------+"
        print "\n\n"
