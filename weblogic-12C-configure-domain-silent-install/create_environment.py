# -*- coding: utf-8 -*-
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;

import socket;

def createFile(directory_name, file_name, content):
	dedirectory = java.io.File(directory_name);
	defile = java.io.File(directory_name + '/' + file_name);

	writer = None;
	try:
		dedirectory.mkdirs();
		defile.createNewFile();
		writer = java.io.FileWriter(defile);
		writer.write(content);
	finally:
		try:
			print 'WRITING FILE ' + file_name;
			if writer != None:
				writer.flush();
				writer.close();
		except java.io.IOException, e:
			e.printStackTrace();


			
print 'SETTING PARAMETERS';
machine_listen_addresses=MACHINE_ADDRESS;
customer_server_names=CUST_SERVER_NAMES;
customer_server_ports=CUST_SERVER_PORTS;
data_source_url=DATA_SOURCE_URL;
data_source_driver=DATA_SOURCE_DRIVER;
data_source_user_prefix=SERVERS_SCHEMA_PREFIX;
data_source_password=SCHEMA_PASSWORD;
data_source_test='SQL SELECT 1 FROM DUAL';

print 'CREATE PATHS';
domain_name=DOMAIN_NAME;
java_home=JAVA_HOME;
middleware_home=MIDDLEWARE_HOME;
weblogic_home=WEBLOGIC_HOME;
configuration_home=CONFIGURATION_HOME;
Oracle_UCM1_home=Oracle_UCM1_HOME;

domain_home=configuration_home + '/domains/' + domain_name;
domain_application_home=configuration_home + '/applications/' + domain_name;

weblogic_template=weblogic_home + '/common/templates/wls/wls.jar';

Oracle_UCM_ContentServer=Oracle_UCM1_home +'/common/templates/wls/oracle.ucm.cs_template.jar';

print 'CREATE DOMAIN';
readTemplate(weblogic_template);
setOption('DomainName', domain_name);
setOption('OverwriteDomain', 'true');
setOption('JavaHome', java_home);
setOption('ServerStartMode', 'prod');
cd('/Security/base_domain/User/weblogic');
cmo.setName('adminUser');
cmo.setUserPassword('adminPassword');
cd('/');

print "SAVE DOMAIN";
writeDomain(domain_home);
closeTemplate();

print 'READ DOMAIN';
readDomain(domain_home);

print 'ADD TEMPLATES';
addTemplate(Oracle_UCM_ContentServer);

setOption('AppDir', domain_application_home);

print 'CREATING MACHINES AND (ADJUSTING) SERVERS : ' + machine_listen_addresses[0];
machine = create('machine_' + machine_listen_addresses[0],MACHINE_TYPE);

cd('/Machine/' + machine.getName());
nodemanager = create(machine.getName(),'NodeManager');
nodemanager.setListenAddress(machine_listen_addresses[0]);
nodemanager.setNMType(NODE_MANAGER_MODE);
cd('/');

print 'CREATING INSPY_SERVER1';
create('inspy_server1','Server');
cd('/Servers/inspy_server1');
cmo.setName('inspy_server1');
cmo.setListenPort(int(INSPY_SERVER_PORT));
cmo.setMachine(machine);

cd('/');

print 'CREATING UCM_SERVER1';
cd('/Servers/UCM_server1');
cmo.setName('UCM_server1');
cmo.setListenPort(int(UCM_SERVER_PORT));
cmo.setMachine(machine);

cd('/');

print 'CREATING IUI_SERVER1';
create('iui_server1','Server');
cd('/Servers/iui_server1');
cmo.setName('iui_server1');
cmo.setListenPort(int(IUI_SERVER_PORT));
cmo.setMachine(machine);

cd('/');

for j in range(len(customer_server_names)):
	cd('/');
	print 'CREATING CUSTOMER SERVER: ' + customer_server_names[j];
	create(customer_server_names[j],'Server');
	cd('/Servers/' + customer_server_names[j]);
	cmo.setName(customer_server_names[j]);
	cmo.setMachine(machine);
	cmo.setListenPort(int(customer_server_ports[j]));
	
cd('/');
	

print 'ADJUST DATA SOURCE SETTINGS';
jdbcsystemresources = cmo.getJDBCSystemResources();
for jdbcsystemresource in jdbcsystemresources:
	cd ('/JDBCSystemResource/' + jdbcsystemresource.getName() + '/JdbcResource/' + jdbcsystemresource.getName() + '/JDBCDriverParams/NO_NAME_0');
	cmo.setUrl(data_source_url);
	if(jdbcsystemresource.getName() == "wlsbjmsrpDataSource"):
		cmo.setDriverName(data_source_driver);
	cmo.setPasswordEncrypted(data_source_password);
	cd ('/JDBCSystemResource/' + jdbcsystemresource.getName() + '/JdbcResource/' + jdbcsystemresource.getName() + '/JDBCDriverParams/NO_NAME_0/Properties/NO_NAME_0/Property/user');
	cmo.setValue(cmo.getValue().replace('DEV',data_source_user_prefix));
	cd('/');

cd('/Server/AdminServer');
cmo.setListenPort(int(ADMIN_SERVER_PORT));
create('AdminServer','SSL');

print 'SAVE CHANGES';
updateDomain();
closeDomain();

print 'CREATE FILES';
directory_name = domain_home + '/servers/AdminServer/security';
file_name = 'boot.properties';
content = 'username=' + 'adminUser' + '\npassword=' + 'adminPassword';
createFile(directory_name, file_name, content);

directory_name = domain_application_home;
file_name = 'readme.txt';
content = 'This directory contains deployment files and deployment plans.\nTo set-up a deployment, create a directory with the name of the application.\nSubsequently, create two sub-directories called app and plan.\nThe app directory contains the deployment artifact.\nThe plan directory contains the deployment plan.';
createFile(directory_name, file_name, content);