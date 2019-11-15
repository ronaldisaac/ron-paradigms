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

customer_server_names=CUST_SERVER_NAMES;
customer_server_ports=CUST_SERVER_PORTS;

edit()
startEdit()

cd('/Servers/inspy_server1/WebServer/inspy_server1') # go to MBean object
#Server start up memory arguments
cd('/Servers/inspy_server1/ServerStart/inspy_server1')
cmo.setArguments('-Xms6G -Xmx6G -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:SurvivorRatio=8 -XX:TargetSurvivorRatio=90 -XX:CMSInitiatingOccupancyFraction=80 -verbose:gc  -XX:+PrintGCApplicationStoppedTime -XX:+PrintGCApplicationConcurrentTime -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -Xloggc:gc.log -XX:+PrintClassHistogram')
cd('/Servers/inspy_server1/SSL/' + 'inspy_server1')
cmo.setHostnameVerificationIgnored(true)
cmo.setHostnameVerifier(None)
cmo.setTwoWaySSLEnabled(false)
cmo.setClientCertificateEnforced(false)
cmo.setJSSEEnabled(true)
cd('/');

invdb_targets = []

for j in range(len(customer_server_names)):
	cd('/');
	print 'SETTING ARGUMENTS FOR CUSTOMER SERVER: ' + customer_server_names[j];
	cd('/Servers/' + customer_server_names[j] + '/ServerStart/' + customer_server_names[j])
	cmo.setArguments('-Xms2G -Xmx2G -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:SurvivorRatio=8 -XX:TargetSurvivorRatio=90 -XX:CMSInitiatingOccupancyFraction=80 -verbose:gc  -XX:+PrintGCApplicationStoppedTime -XX:+PrintGCApplicationConcurrentTime -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -Xloggc:gc.log -XX:+PrintClassHistogram')
	cd('/Servers/' + customer_server_names[j] +'/SSL/' + customer_server_names[j])
	cmo.setHostnameVerificationIgnored(true)
	cmo.setHostnameVerifier(None)
	cmo.setTwoWaySSLEnabled(false)
	cmo.setClientCertificateEnforced(false)
	cmo.setJSSEEnabled(true)
	invdb_targets.append(ObjectName('com.bea:Name=' + customer_server_names[j] + ',Type=Server'))

cd('/');

cd('/Servers/UCM_server1/WebServer/UCM_server1') # go to MBean object
#Server start up memory arguments
cd('/Servers/UCM_server1/ServerStart/UCM_server1')
cmo.setArguments('-Xms512m -Xmx512m')
cd('/');

cd('/Servers/iui_server1/WebServer/iui_server1') # go to MBean object
#Server start up memory arguments
cd('/Servers/iui_server1/ServerStart/iui_server1')
cmo.setArguments('-Xms4G -Xmx4G -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:SurvivorRatio=8 -XX:TargetSurvivorRatio=90 -XX:CMSInitiatingOccupancyFraction=80 -verbose:gc  -XX:+PrintGCApplicationStoppedTime -XX:+PrintGCApplicationConcurrentTime -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -Xloggc:gc.log -XX:+PrintClassHistogram')
cd('/Servers/iui_server1/SSL/iui_server1')
cmo.setHostnameVerificationIgnored(true)
cmo.setHostnameVerifier(None)
cmo.setTwoWaySSLEnabled(false)
cmo.setClientCertificateEnforced(false)
cmo.setJSSEEnabled(true)
cd('/');

save()
activate()

#Datasource EBSDS configuration
dsName=EBS_DATASOURCE_NAME
dsFileName=EBS_DATASOURCE_FILENAME
dsDatabaseName=EBS_DATASOURCE_DATABASE_NAME
datasourceTarget1=EBS_DATASOURCE_TARGET1
dsJNDIName=EBS_DATASOURCE_JNDINAME
dsDriverName=EBS_DATASOURCE_DRIVER_CLASS
dsURL=EBS_DATASOURCE_URL
dsUserName=EBS_DATASOURCE_USERNAME
dsPassword=EBS_DATASOURCE_PASSWORD
dsTestQuery=EBS_DATASOURCE_TEST_QUERY

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

cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName )
cmo.createProperty('user')

cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/user')
cmo.setValue(dsUserName)

cd('/SystemResources/' + dsName )
set('Targets',jarray.array(invdb_targets, ObjectName))
save()
activate()
	
	
#Datasource INVDB configuration
dsName=INVDB_DATASOURCE_NAME
dsFileName=INVDB_DATASOURCE_FILENAME
dsDatabaseName=INVDB_DATASOURCE_DATABASE_NAME
datasourceTarget=INVDB_DATASOURCE_TARGET
dsJNDIName=INVDB_DATASOURCE_JNDINAME
dsDriverName=INVDB_DATASOURCE_DRIVER_CLASS
dsURL=INVDB_DATASOURCE_URL
dsUserName=INVDB_DATASOURCE_USERNAME
dsPassword=INVDB_DATASOURCE_PASSWORD
dsTestQuery=INVDB_DATASOURCE_TEST_QUERY

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
invdb_targets.append(ObjectName('com.bea:Name=inspy_server1,Type=Server'))
set('Targets',jarray.array([ObjectName('com.bea:Name=inspy_server1,Type=Server')], ObjectName))
set('Targets',jarray.array(invdb_targets, ObjectName))

save()
activate()

#Datasource INVDBUI configuration
dsName=INVDBUI_DATASOURCE_NAME
dsFileName=INVDBUI_DATASOURCE_FILENAME
dsDatabaseName=INVDB_DATASOURCE_DATABASE_NAME
datasourceTarget=INVDBUI_DATASOURCE_TARGET
dsJNDIName=INVDBUI_DATASOURCE_JNDINAME
dsDriverName=INVDB_DATASOURCE_DRIVER_CLASS
dsURL=INVDB_DATASOURCE_URL
dsUserName=INVDB_DATASOURCE_USERNAME
dsPassword=INVDB_DATASOURCE_PASSWORD
dsTestQuery=INVDB_DATASOURCE_TEST_QUERY

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
set('Targets',jarray.array([ObjectName('com.bea:Name=iui_server1,Type=Server')], ObjectName))

save()
activate()	

#Datasource INVDB_MOBILE configuration
dsName=INVDB_MOBILE_DATASOURCE_NAME
dsFileName=INVDB_MOBILE_DATASOURCE_FILENAME
dsDatabaseName=INVDB_DATASOURCE_DATABASE_NAME
datasourceTarget=INVDB_MOBILE_DATASOURCE_TARGET
dsJNDIName=INVDB_MOBILE_DATASOURCE_JNDINAME
dsDriverName=INVDB_DATASOURCE_DRIVER_CLASS
dsURL=INVDB_DATASOURCE_URL
dsUserName=INVDB_DATASOURCE_USERNAME
dsPassword=INVDB_DATASOURCE_PASSWORD
dsTestQuery=INVDB_DATASOURCE_TEST_QUERY

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
set('Targets',jarray.array([ObjectName('com.bea:Name=iui_server1,Type=Server')], ObjectName))

save()
activate()	

#Datasource INSPY_CONFIG configuration
dsName=INSPY_CONFIG_DATASOURCE_NAME
dsFileName=INSPY_CONFIG_DATASOURCE_FILENAME
dsDatabaseName=INVDB_DATASOURCE_DATABASE_NAME
datasourceTarget=INSPY_CONFIG_DATASOURCE_TARGET
dsJNDIName=INSPY_CONFIG_DATASOURCE_JNDINAME
dsDriverName=INVDB_DATASOURCE_DRIVER_CLASS
dsURL=INVDB_DATASOURCE_URL
dsUserName=INSPY_CONFIG_DATASOURCE_USERNAME
dsPassword=INSPY_CONFIG_DATASOURCE_PASSWORD
dsTestQuery=INVDB_DATASOURCE_TEST_QUERY

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
set('Targets',jarray.array([ObjectName('com.bea:Name=iui_server1,Type=Server')], ObjectName))

save()
activate()

edit()
startEdit()

print 'Creating Email JMS JDBC Store'
cd('/')
cmo.createJDBCStore('EmailJmsJDBCStore')
cd('/JDBCStores/EmailJmsJDBCStore')
cmo.setDataSource(getMBean('/SystemResources/INVDB'))
cmo.setPrefixName('INSPY')
set('Targets',jarray.array([ObjectName('com.bea:Name=inspy_server1,Type=Server')], ObjectName))

print 'Creating JMS Server'
cd('/')
cmo.createJMSServer('EmailJmsServer')
cd('/JMSServers/EmailJmsServer')
cmo.setTemporaryTemplateResource(None)
cmo.setTemporaryTemplateName(None)
cmo.setPersistentStore(getMBean('/JDBCStores/EmailJmsJDBCStore'))
cmo.addTarget(getMBean('/Servers/inspy_server1'))

print 'Creating JMS Module'
cd('/')
cmo.createJMSSystemResource('EmailJmsModule')
cd('/JMSSystemResources/EmailJmsModule')
cmo.addTarget(getMBean('/Servers/inspy_server1'))
cmo.createSubDeployment('EmailSubDeployment')

print 'Creating Connection Factory'
cd('/')
cd('/JMSSystemResources/EmailJmsModule/JMSResource/EmailJmsModule')
cmo.createConnectionFactory('EmailConnectionFactory')
cd('/JMSSystemResources/EmailJmsModule/JMSResource/EmailJmsModule/ConnectionFactories/EmailConnectionFactory')
cmo.setJNDIName('jms/EmailConnectionFactory')
set('SubDeploymentName','EmailSubDeployment')
cd('/JMSSystemResources/EmailJmsModule/JMSResource/EmailJmsModule/ConnectionFactories/EmailConnectionFactory/SecurityParams/EmailConnectionFactory')
cmo.setAttachJMSXUserId(false)
cd('/JMSSystemResources/EmailJmsModule/JMSResource/EmailJmsModule/ConnectionFactories/EmailConnectionFactory/ClientParams/EmailConnectionFactory')
cmo.setClientIdPolicy('Restricted')
cmo.setSubscriptionSharingPolicy('Exclusive')
cmo.setMessagesMaximum(10)
cd('/JMSSystemResources/EmailJmsModule/JMSResource/EmailJmsModule/ConnectionFactories/EmailConnectionFactory/TransactionParams/EmailConnectionFactory')
cmo.setXAConnectionFactoryEnabled(true)
cd('/JMSSystemResources/EmailJmsModule/JMSResource/EmailJmsModule/ConnectionFactories/EmailConnectionFactory')
cmo.setDefaultTargetingEnabled(false)

print 'Creating Queue'
cd('/')
cd('/JMSSystemResources/EmailJmsModule/JMSResource/EmailJmsModule')
cmo.createQueue('EmailJmsQueue')
cd('/JMSSystemResources/EmailJmsModule/JMSResource/EmailJmsModule/Queues/EmailJmsQueue')
set('JNDIName','jms/EmailJmsQueue')
set('SubDeploymentName','EmailSubDeployment')
cd('/JMSSystemResources/EmailJmsModule/SubDeployments/EmailSubDeployment')
cmo.addTarget(getMBean('/JMSServers/EmailJmsServer'))

print 'JMS Resources are Successfully Created'
activate()

edit()
startEdit()
undo(defaultAnswer='y', unactivatedChanges='true')
stopEdit('y')

shutdown(block='true')