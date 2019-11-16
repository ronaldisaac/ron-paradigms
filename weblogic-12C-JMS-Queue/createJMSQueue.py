admin_server_port=ADMIN_SERVER_PORT;
admin_server_url = 't3://' + ADMIN_HOST + ':' + ADMIN_SERVER_PORT;
connect('adminUser', 'adminPassword', url=admin_server_url)

edit()
startEdit()

print 'Creating App JMS JDBC Store'
cd('/')
cmo.createJDBCStore('AppJmsJDBCStore')
cd('/JDBCStores/AppJmsJDBCStore')
cmo.setDataSource(getMBean('/SystemResources/' + DATASOURCE_NAME))
cmo.setPrefixName('APP')
set('Targets',jarray.array([ObjectName('com.bea:Name=app_server1,Type=Server')], ObjectName))

print 'Creating JMS Server'
cd('/')
cmo.createJMSServer('AppJmsServer')
cd('/JMSServers/AppJmsServer')
cmo.setTemporaryTemplateResource(None)
cmo.setTemporaryTemplateName(None)
cmo.setPersistentStore(getMBean('/JDBCStores/AppJmsJDBCStore'))
cmo.addTarget(getMBean('/Servers/app_server1'))

print 'Creating JMS Module'
cd('/')
cmo.createJMSSystemResource('AppJmsModule')
cd('/JMSSystemResources/AppJmsModule')
cmo.addTarget(getMBean('/Servers/app_server1'))
cmo.createSubDeployment('AppSubDeployment')

print 'Creating Connection Factory'
cd('/')
cd('/JMSSystemResources/AppJmsModule/JMSResource/AppJmsModule')
cmo.createConnectionFactory('AppConnectionFactory')
cd('/JMSSystemResources/AppJmsModule/JMSResource/AppJmsModule/ConnectionFactories/AppConnectionFactory')
cmo.setJNDIName('jms/AppConnectionFactory')
set('SubDeploymentName','AppSubDeployment')
cd('/JMSSystemResources/AppJmsModule/JMSResource/AppJmsModule/ConnectionFactories/AppConnectionFactory/SecurityParams/AppConnectionFactory')
cmo.setAttachJMSXUserId(false)
cd('/JMSSystemResources/AppJmsModule/JMSResource/AppJmsModule/ConnectionFactories/AppConnectionFactory/ClientParams/AppConnectionFactory')
cmo.setClientIdPolicy('Restricted')
cmo.setSubscriptionSharingPolicy('Exclusive')
cmo.setMessagesMaximum(10)
cd('/JMSSystemResources/AppJmsModule/JMSResource/AppJmsModule/ConnectionFactories/AppConnectionFactory/TransactionParams/AppConnectionFactory')
cmo.setXAConnectionFactoryEnabled(true)
cd('/JMSSystemResources/AppJmsModule/JMSResource/AppJmsModule/ConnectionFactories/AppConnectionFactory')
cmo.setDefaultTargetingEnabled(false)

print 'Creating Queue'
cd('/')
cd('/JMSSystemResources/AppJmsModule/JMSResource/AppJmsModule')
cmo.createQueue('AppJmsQueue')
cd('/JMSSystemResources/AppJmsModule/JMSResource/AppJmsModule/Queues/AppJmsQueue')
set('JNDIName','jms/AppJmsQueue')
set('SubDeploymentName','AppSubDeployment')
cd('/JMSSystemResources/AppJmsModule/SubDeployments/AppSubDeployment')
cmo.addTarget(getMBean('/JMSServers/AppJmsServer'))

print 'JMS Resources are Successfully Created'
activate()