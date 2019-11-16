admin_server_port=ADMIN_SERVER_PORT;
admin_server_url = 't3://' + ADMIN_HOST + ':' + ADMIN_SERVER_PORT;
connect('adminUser', 'adminPassword', url=admin_server_url)
prps = makePropertiesObject("weblogic.ListenPort=" + ADMIN_SERVER_PORT)
storeUserConfig(CONFIGURATION_HOME + '/domains/' + DOMAIN_NAME + '/wlst_scripts/userconfigfile.secure', CONFIGURATION_HOME + '/domains/' + DOMAIN_NAME + '/wlst_scripts/userkeyfile.secure')

domain_name = DOMAIN_NAME;

edit()
startEdit()
cd('/SecurityConfiguration/'+ DOMAIN_NAME) # go to MBean object
cmo.setNodeManagerUsername('adminUser') # change username
cmo.setNodeManagerPassword('adminPassword') # change password
save()
activate()

application_server_names=APP_SERVER_NAMES;
application_server_ports=APP_SERVER_PORTS;

edit()
startEdit()


database_targets = []

for j in range(len(application_server_names)):
	cd('/');
	print 'SETTING ARGUMENTS FOR CUSTOMER SERVER: ' + application_server_names[j];
	cd('/Servers/' + application_server_names[j] + '/ServerStart/' + application_server_names[j])
	cmo.setArguments('-Xms2G -Xmx2G -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:SurvivorRatio=8 -XX:TargetSurvivorRatio=90 -XX:CMSInitiatingOccupancyFraction=80 -verbose:gc  -XX:+PrintGCApplicationStoppedTime -XX:+PrintGCApplicationConcurrentTime -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -Xloggc:gc.log -XX:+PrintClassHistogram')
	cd('/Servers/' + application_server_names[j] +'/SSL/' + application_server_names[j])
	cmo.setHostnameVerificationIgnored(true)
	cmo.setHostnameVerifier(None)
	cmo.setTwoWaySSLEnabled(false)
	cmo.setClientCertificateEnforced(false)
	cmo.setJSSEEnabled(true)
	database_targets.append(ObjectName('com.bea:Name=' + application_server_names[j] + ',Type=Server'))

cd('/');

save()
activate()

#Datasource INVDB configuration
dsName=DATASOURCE_NAME
dsFileName=DATASOURCE_FILENAME
dsDatabaseName=DATASOURCE_DATABASE_NAME
datasourceTarget=DATASOURCE_TARGET
dsJNDIName=DATASOURCE_JNDINAME
dsDriverName=DATASOURCE_DRIVER_CLASS
dsURL=DATASOURCE_URL
dsUserName=DATASOURCE_USERNAME
dsPassword=DATASOURCE_PASSWORD
dsTestQuery=DATASOURCE_TEST_QUERY

edit()
startEdit()
cd('/')
cmo.createJDBCSystemResource(dsName)
cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName)
cmo.setName(dsName)

cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName )
set('JNDINames',jarray.array([String(dsJNDIName)], String))

cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName )
cmo.setUrl(dsURL)
cmo.setDriverName( dsDriverName )
cmo.setPassword(dsPassword)

cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCConnectionPoolParams/' + dsName )
cmo.setTestTableName(dsTestQuery)
cmo.setMaxCapacity(100)
cmo.setWrapTypes(false)

cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName )
cmo.createProperty('user')

cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/user')
cmo.setValue(dsUserName)

cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName )
cmo.setGlobalTransactionsProtocol('None')

cd('/SystemResources/' + dsName )
set('Targets',jarray.array(database_targets, ObjectName))

save()
activate()

edit()
startEdit()
undo(defaultAnswer='y', unactivatedChanges='true')
stopEdit('y')

shutdown(block='true')