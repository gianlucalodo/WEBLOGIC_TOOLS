#!/usr/bin/ksh

# simple script that monitor Weblogic server status and applications status
# this script launch WLST server-app_monitor.pj

WORKDIR="<set here workdir>"


BANNER="WARNING... Weblogic connection problem !"

clear

print "\nWLS server and app check\n"

. ${WORKDIR}/setWLSTEnv.sh
${JAVA_OPT} -cp ${CLASSPATH} weblogic.WLST ${WORKDIR}/server-app_monitor.py -p ${WORKDIR} 2>/dev/null

#return 0 -> OK
#return different from 0 -> NOK 
if [ $? -ne 0 ]
then
        banner "ATTENZIONEr!"
        print "\n\n\n${BANNER}\n\n"
        print "ERRORS:\n\n${BANNER}"

fi

print "\n\n"
