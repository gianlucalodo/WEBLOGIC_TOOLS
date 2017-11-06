#!/usr/bin/ksh

### Simple script to monitor weblogic JMS queue

WORKDIR="<set_here_work_dir>"
BANNER="Warning! problem to connect to weblogic server"

clear

echo "\n\nJMS QUEUE"
echo "-------------

. ${WORKDIR}/setWLSTEnv.sh
${JAVA_OPT} -cp ${CLASSPATH} weblogic.WLST ${WORKDIR}/monitorJMS.py -p ${WORKDIR} 1> /dev/null 2>&1

#return 0 -> OK
#return != 0 -> NOK 
if [ $? -ne 0 ]
then      
        print "\n\n\n${BANNER}\n\n"
fi
print "\n\n"
