
# simple WLST script to delete JMS messages

from weblogic.jms.extensions import JMSMessageInfo
from javax.jms import TextMessage
from javax.jms import ObjectMessage
import sets
import getopt  
import sys  

#=====================================  
try:  
        opts, args = getopt.getopt( sys.argv[1:], "p:", ["Path"])  
except getopt.GetoptError, err:  
        print str(err)  
        sys.exit(2)  
#=====================================  
for opt, arg in opts:  
        #print opt+" "+ arg
        if opt == "-p":
                Serv = arg
#=====================================  


jmsservername='<insert here jms server name>' + Serv
jmsmodulename='<insert here JMSModule name>'
jmsdestname='<insert here destination name>' + Serv
queuename='<insert here queue name>'

### insert here string to search inside message
strtosearch='<insert here string to search>'

Path="<insert here path where find auyhentication files, or import from argv>"
#connect to weblogic...
userConfigFile = Path+"/.profile/.myuserconfigfile.secure"
userKeyFile = Path+"/.profile/.myuserkeyfile.secure"
url = "t3s://<adminserver>:<adminport>"
connect(userConfigFile=userConfigFile, userKeyFile=userKeyFile, url=url ,timeout='20000')


#Switch to the server runtime tree
domainRuntime()
cd('ServerRuntimes/'+jmsdestname+'/JMSRuntime/'+jmsdestname+'.jms/JMSServers/'+jmsservername+'/Destinations/'+jmsmodulename+'/'+jmsservername+'/'+queuename)

#Get the cursor (JMSMessageCursorRuntimeMBean) to browse the messages - No selector & No time out
cursor = cmo.getMessages('',0)

#Determine the number of messages in the destination
cursorsize = cmo.getCursorSize(cursor)
print '------------------------------------------'
print 'Total Number of Messages -> ', cursorsize
print '------------------------------------------'
print ' Deleted=1 -> record deleted'
print ' Deleted=0 -> record not deleted'

#Get all the messages as an array of javax.management.openmbean.CompositeData
#messages = cmo.getNext(cursor, cursorsize) 
piece=1
i=0
while (i < cursorsize):
        messages = cmo.getItems(cursor,i,piece)
        
        #Loop through the array of messages
        for message in messages:
                
                #Create WebLogic JMSMessageInfo to get Message ID
                jmsmsginfo = JMSMessageInfo(message)
                wlmsg = jmsmsginfo.getMessage()
                wlmsgid = wlmsg.getJMSMessageID()
                
                #Get Message with body
                fullcursormsg = cmo.getMessage(cursor,wlmsgid)
                fulljmsmsginfo = JMSMessageInfo(fullcursormsg)
                handle = fulljmsmsginfo.getHandle()
                compdata = cmo.getMessage(cursor, handle)
                msgwithbody = JMSMessageInfo(compdata)
                
 
                
                #Print Message Body
                fullwlmsg = fulljmsmsginfo.getMessage()

                        
                if isinstance(fullwlmsg, TextMessage):
                        msgtxt = fullwlmsg.getText()
                        if msgtxt.find(strtosearch) != -1 :
                                print 'TextMessage - Message ID           - ' + msgwithbody.getMessage().getJMSMessageID()
                                
                else:
                    if isinstance(fullwlmsg, ObjectMessage):
                        msgobj = fullwlmsg.getObject()  
                        tmpvar = str(msgobj)
                        if tmpvar.find(strtosearch) != -1: 
                                selector = str(msgwithbody.getMessage().getJMSMessageID())
                                #### uncomment this to delete
                                ###cmo.getMessages("JMSMessageID = ' + selector + '");
                                numdel = cmo.deleteMessages("JMSMessageID = ' + selector + '"); 
                                ##while numdel != 1:
                                ###     numdel = cmo.deleteMessages("JMSMessageID = ' + selector + '"); 
                                print 'Msg.ID - ' + selector + ' Deleted = ' + str(numdel) 
                                #print 'JMSMessageID = \'' + selector + '\''    
                                ###print fullwlmsg.getObject()
                    else:
                        print '***Not a Text or Object Message***'
                        print fullwlmsg.toString()
                #print ' '
                i=i+ piece;

#Close cursor as No Time Out specified - Best practice
cmo.closeCursor(cursor)

#Disconnect & Exit
disconnect()
exit()
