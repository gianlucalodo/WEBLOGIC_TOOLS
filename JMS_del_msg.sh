#!/usr/bin/ksh


WORKDIR="<insert here workdir"
BANNER="WARNING! weblogic connection problem"

clear

echo "\n\nDETETE JMS QUEUE"
echo "----------------------\033[0m"


if [ $# != 1 ]
then
        echo " EERROR!!!!"
        echo " Pass as parameter final part of server name"
        exit
fi

. ${WORKDIR}/setWLSTEnv.sh
GS_LIB="<in my case this path is use for application library"
export CLASSPATH=${CLASSPATH}:${GS_LIB}/log4j-1.2.15.jar:${GS_LIB}/flowapp-lib-foundation-2.0.jar:${GS_LIB}/gson-2.1.jar
${JAVA_OPT} -cp ${CLASSPATH} weblogic.WLST ${WORKDIR}/JMS_del_msg.py -p $1 
