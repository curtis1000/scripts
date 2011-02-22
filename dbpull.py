#!/usr/bin/python
import os
import getpass

# Script to get a database from remote server and import it locally, built on Ubuntu.
# This script assumes you want to use the same db username and password on both systems.

temp_dir = '/tmp'
temp_filename = 'temp.sql'

remote_dbserver = raw_input("Remote DB Server: ")

# same for both
dbname_dbusername = raw_input("DB Name/DB Username: ")

# db password
dbpassword = raw_input("DB Password: ")

# local mysql root acct
local_mysql_root_name = raw_input("Local Mysql Root Username: ")
local_mysql_root_password = getpass.getpass("Local Mysql Root Password: ")

print 'fetching remote mysql dump from '+remote_dbserver+'...'

# dump sql to a temp file
os.system('mysqldump --opt --host '+remote_dbserver+' --user='+dbname_dbusername+' --password='+dbpassword+' '+dbname_dbusername+' > '+temp_dir+'/temp.sql')

# ensure user/db exists on local mysql server
# we're going to do them seperate because drop user can error out if the user doesn't exist (breaking following statements)
# by making the drop user statement the LAST statement in the command, it doesn't affect further calls

ensure_drop = "DROP DATABASE IF EXISTS "+dbname_dbusername+"; DROP USER "+dbname_dbusername+";" 
ensure_create = "CREATE DATABASE "+dbname_dbusername+"; CREATE USER '"+dbname_dbusername+"'@'%' IDENTIFIED BY '"+dbpassword+"'; GRANT ALL PRIVILEGES on  "+dbname_dbusername+".* to "+dbname_dbusername+"@'%' ;"

print 'ensuring user/db exists on local system...'

#run them
#send drop sql to /dev/null to silence the potential error for drop user
os.system('mysql --user='+local_mysql_root_name+' --password='+local_mysql_root_password+' -e "'+ensure_drop+'" > /dev/null')
os.system('mysql --user='+local_mysql_root_name+' --password='+local_mysql_root_password+' -e "'+ensure_create+'"')

# for a db that utilizes foreign keys, missing foreign keys will cause the import to fail, temporarily turning them off in import file

foreign_key_off = 'SET FOREIGN_KEY_CHECKS = 0;'
foreign_key_on = 'SET FOREIGN_KEY_CHECKS = 1;'


# prepend foreign key check flags
os.system('echo "'+foreign_key_off+'" | cat - '+temp_dir+'/'+temp_filename+' > '+temp_dir+'/'+dbname_dbusername+'.sql')

# append foreign key check flag
os.system('echo "'+foreign_key_on+'" >> '+temp_dir+'/'+dbname_dbusername+'.sql')

print 'importing database to local system...'

# '+temp_dir+'/'+dbname_dbusername+'.sql' is ready for import
os.system('mysql --user='+local_mysql_root_name+' --password='+local_mysql_root_password+' '+dbname_dbusername+' < '+temp_dir+'/'+dbname_dbusername+'.sql')

print 'deleting temp files...'

# clean up
os.system('rm '+temp_dir+'/temp.sql')
os.system('rm '+temp_dir+'/'+dbname_dbusername+'.sql')

