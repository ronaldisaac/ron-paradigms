#!/bin/sh
 
# source the properties:
SCRIPT=$(readlink -f $0)
SCRIPT_PATH=$(dirname $SCRIPT)

. ${SCRIPT_PATH}/silent-install.properties

rm silent-weblogic-server.txt
rm setEnvironmentVars.sh

echo "inventory_loc=$ORACLE_INVENTORY_HOME
  inst_group=$ORACLE_INSTALL_GROUP" >> $TEMPORARY_DIRECTORY/oraInst.loc
  
echo "[ENGINE]
	Response File Version=1.0.0.0.0
	[GENERIC]
	DECLINE_AUTO_UPDATES=true
	ORACLE_HOME=${MIDDLEWARE_HOME}
	INSTALL_TYPE=WebLogic Server" >> silent-weblogic-server.txt
	
echo "export PATH=$PATH:$MIDDLEWARE_HOME/oracle_common/modules/thirdparty/org.apache.ant/1.9.8.0.0/apache-ant-1.9.8/bin
	  export JAVA_HOME=$JAVA_HOME" >> setEnvironmentVars.sh

$JAVA_HOME/bin/java -jar $WEBLOGIC_SERVER_INSTALL_FILE_PATH -silent -ignoreSysPrereqs -responsefile $PWD/silent-weblogic-server.txt -invPtrLoc $TEMPORARY_DIRECTORY/oraInst.loc

rm silent-weblogic-server.txt
