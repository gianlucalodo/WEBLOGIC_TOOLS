import sets
import getopt  
import sys  

#=====================================  
try:  
 opts, args = getopt.getopt( sys.argv[1:], "p:", ["Path"])  
except getopt.GetoptError, err:  
 print str(err)  
 usage()  
 sys.exit(2)  
#=====================================  
for opt, arg in opts:  
 #print opt+" "+ arg
 if opt == "-p":  
  Path = arg
#print Path
#=====================================  

# Array containing Weblogic server name
wlsList = ['server_1','server_2']

# Connection to server admin
userConfigFile = Path+"/.profile/.myuserconfigfile.secure"
userKeyFile = Path+"/.profile/.myuserkeyfile.secure"
url = "t3s://adminserver:50002"
connect(userConfigFile=userConfigFile, userKeyFile=userKeyFile, url=url ,timeout='20000')
domainRuntime()



### Weblogic server status check
# Entering in server path...
cd('ServerRuntimes')
servers=domainRuntimeService.getServerRuntimes()

# Dictionary containing error
errDict = {} 
count_errDict = 0

# Array of weblogic server extracted from console ( need to test if any server is down ) 
wlsListExtract = [] 

title = "WLS STATE CHECK"
separator = "+------------------------------------------------------------------------+"
print separator
print '|\033[1m' , title.center(70) , '\033[0m|'
for server in servers:
        serverName=server.getName();
        serverState=server.getState();

        # Add weblogic server found every step
        wlsListExtract.append(serverName)
        # Check if server is running
        if ( serverState == "RUNNING" ) :
                serverOK = "OK";

        # otherwise print NOK and populate errDict
        else:
                serverOK = "NOT OK";
                errDict.update({count_errDict : 'WARNING: wls' + serverName + ' is in state ' + serverState + ' that is different from RUNNING'})
                count_errDict = count_errDict + 1

        # print state
        print separator 
        print '| %-12s %-15s | %6s \033[1m%-16s\033[0m | %-6s \033[1m%6s\033[0m |' % ('Server:',serverName,'State:',serverState,'Check:',serverOK)
        #print '| %-12s %-28s %-6s %-5d | %13s |' % ('Address:',server.getListenAddress(),'Port:',server.getListenPort(),' ')

# Extract difference between wlsList (contains static server name set from user) and 
# array wlsListExtract (contains weblogic server name extracted from CLI), the differences 
# are collected inside array resultWlsArray to be printed as a error
setWlsList = sets.Set(wlsList)
setWlsListExtract = sets.Set(wlsListExtract)
arrayWlsDifference = setWlsList.symmetric_difference(setWlsListExtract)
resultWlsArray= [a for a in arrayWlsDifference]
#add errors to errDict
if (len(resultWlsArray) != 0) :
        for i in resultWlsArray :
                print separator
                print '| %-12s %-15s | %6s \033[1m%-16s\033[0m | %-6s \033[1m%6s\033[0m |' % ('Server:', i ,'State:', 'NOT ACTIVE' ,'Check:','NOT OK')
                print '| \033[1m%-53s\033[0m  | %13s |' % ('SERVER NOT ACTIVE-VERIFY NODEMANAGER PRESENCE' , ' ' )
                errDict.update({count_errDict : 'WARNING: wls ' + i + ' not active - Verifify nodemanager presence'}) 
                count_errDict= count_errDict + 1


### APPLICATIONS CHECK
# Entering in application path
cd('../AppRuntimeStateRuntime/AppRuntimeStateRuntime')
# return all applications
applications = cmo.getApplicationIds()


title = "APPLICAZIONS STATE CHECK"
print separator
print '|\033[1m' , title.center(70) , '\033[0m|' 
for apps in applications:
        appsState = cmo.getIntendedState('' + apps + '')
        # If application is active...OK 
        if ( appsState == "STATE_ACTIVE" ) :
                appsOK = "OK";
        else:
                appsOK = "NOT OK";
                errDict.update({count_errDict : 'WARNING: application ' + apps + ' is in state ' + appsState + ' that is different from ACTIVE'})
                count_errDict = count_errDict + 1

        # print states
        print separator 
        print '| %-12s %-20s | %6s \033[1m%-11s\033[0m | %-6s \033[1m%6s\033[0m |' % ('Application:',apps,'State:',"".join(appsState.split('STATE_')),'Check:',appsOK)

print separator 
print '\n'

# print errors
print 'ERRORS:';
for key in errDict.keys():
        print errDict[key] 

#exit()
