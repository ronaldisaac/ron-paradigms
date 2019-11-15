#!/bin/sh
 
# source the properties:
SCRIPT=$(readlink -f $0)
SCRIPT_PATH=$(dirname $SCRIPT)

. ${SCRIPT_PATH}/silent-install.properties

rm silent-ucm-server.txt

echo "[ENGINE]
	Response File Version=1.0.0.0.0
	[GENERIC]
	DECLINE_AUTO_UPDATES=true
	ORACLE_HOME=${MIDDLEWARE_HOME}
	INSTALL_TYPE=WebCenter Content" >> silent-ucm-server.txt

$JAVA_HOME/bin/java -jar $UCM_INSTALL_FILE_PATH -silent -ignoreSysPrereqs -responsefile $PWD/silent-ucm-server.txt -invPtrLoc $TEMPORARY_DIRECTORY/oraInst.loc

rm silent-ucm-server.txt
