#!/bin/sh
 
# source the properties:
SCRIPT=$(readlink -f $0)
SCRIPT_PATH=$(dirname $SCRIPT)

. ${SCRIPT_PATH}/silent-install.properties

rm silent-weblogic-infrastructure.txt

echo "[ENGINE]
	Response File Version=1.0.0.0.0
	[GENERIC]
	DECLINE_AUTO_UPDATES=true
	ORACLE_HOME=${MIDDLEWARE_HOME}
	INSTALL_TYPE=Fusion Middleware Infrastructure" >> silent-weblogic-infrastructure.txt

$JAVA_HOME/bin/java -jar $WEBLOGIC_INFRASTRUCTURE_INSTALL_FILE_PATH -silent -ignoreSysPrereqs -responsefile $PWD/silent-weblogic-infrastructure.txt -invPtrLoc $TEMPORARY_DIRECTORY/oraInst.loc

rm silent-weblogic-infrastructure.txt
