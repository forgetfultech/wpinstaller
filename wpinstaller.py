#!/usr/bin/env python
# Automate Wordpress Setup

import random
import optparse
import os
import string
import crypt
import getpass
import MySQLdb as mdb

def main():
    p = optparse.OptionParser()
    p.add_option('--domain', '-d')
    p.add_option('--user', '-u')
    options, arguments = p.parse_args()

    # Create new *nix user

    userPasswd = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8)) # Random Password Generation
    os.system("useradd -p %s %s " % (userPasswd,options.user)) # User generation

    print "User Created"

    # Create site's directory

    os.system("mkdir -p /home/%s/%s" % (options.user, options.domain)) # Create domain's home directory

    # Seutp Wordpress DB

    dbName = 'wp_'+options.domain.split('.')[0]
    dbName = dbName.replace(" ", "_").replace("-","_")
    dbPasswd = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16)) # Random Password Generation
    con = mdb.connect('localhost', '<Your User Here>', '<Your Password Here>');
    cur = con.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS %s" % (dbName))
    cur.execute("CREATE USER '%s'@'localhost' IDENTIFIED BY  '%s';" % (options.user,dbPasswd))
    cur.execute("GRANT SELECT , INSERT , UPDATE , DELETE , CREATE , DROP , INDEX , ALTER , CREATE TEMPORARY TABLES ON  `%s` . * TO  '%s'@'localhost';" % (dbName,options.user))
    con.close()

    print "Database Created"

    # Create site's directory

    os.system("mkdir -p /home/%s/%s/" % (options.user,options.domain)) # Create domain's home directory

    # Setup Wordpress

    os.system("wget http://wordpress.org/latest.zip") # Download the latest Wordpress
    os.system("unzip -qq latest.zip -d /home/%s/%s/" % (options.user,options.domain)) # Unzip Wordpress into current (site's home) directory
    os.system("mv /home/%s/%s/wordpress/ /home/%s/%s/public_html/" % (options.user,options.domain,options.user,options.domain))
    os.system("rm -rf /home/%s/%s/wordpress/" % (options.user,options.domain))
    os.system("rm latest.zip")
    

    fin = open("/home/%s/%s/public_html/wp-config-sample.php" % (options.user,options.domain))
    fout = open("/home/%s/%s/public_html/wp-config.php" % (options.user,options.domain), "wt")
    for line in fin:
        result = line.replace('database_name_here', '%s'  % (dbName)).replace('username_here', '%s'  % (options.user)).replace('password_here', '%s' % (dbPasswd))
        fout.write(result)
    fout.write("define(\'FS_METHOD\', \'direct\');")
    fin.close()
    fout.close()

    os.system("wget https://github.com/eddiemachado/bones/archive/master.zip -O /home/%s/%s/public_html/wp-content/themes/master.zip" % (options.user,options.domain))
    os.system("unzip -qq /home/%s/%s/public_html/wp-content/themes/master.zip -d /home/%s/%s/public_html/wp-content/themes/" % (options.user,options.domain,options.user,options.domain))
    os.system("mv /home/%s/%s/public_html/wp-content/themes/bones-master /home/%s/%s/public_html/wp-content/themes/bones" % (options.user,options.domain,options.user,options.domain))
    os.system("rm /home/%s/%s/public_html/wp-content/themes/master.zip" % (options.user,options.domain))

    os.system("rm /home/%s/%s/public_html/wp-config-sample.php" % (options.user,options.domain)) # Move sample config$

    print "Wordpress Installed"

    # Setup proper Permissions

    os.system("chown -R %s:%s /home/%s/" % (options.user,options.user,options.user))
    os.system("chown -R %s:www-data /home/%s/%s/public_html/wp-content" % (options.user,options.user,options.domain))
    os.system("chmod -R g+w /home/%s/%s/public_html/wp-content" % (options.user,options.domain))
    os.system("chmod g+s /home/%s/%s/public_html/wp-content" % (options.user,options.domain))

    # Nginx Virtualhost Setup

    fin = open("/etc/nginx/sites-available/wordpress.vhost")
    fout = open("/etc/nginx/sites-available/%s.vhost" % (options.domain), "wt")
    for line in fin:
        result = line.replace('<site>', '%s' % (options.domain)).replace('<user>', '%s' % (options.user))
        fout.write(result)
    fin.close()
    fout.close()

    os.system("ln -s /etc/nginx/sites-available/%s.vhost /etc/nginx/sites-enabled/%s.vhost" % (options.domain, options.domain))
    
    groupUsers = ["www-data"]
    for groupUser in groupUsers:
        os.system("gpasswd -a %s %s" %(groupUser,options.user))
    
    # End of script. Print credentials
    print "\033[0;44;37mHere are your credentials:\033[0m"
    print "FTP User: %s" % (options.user)
    print "FTP Pass: %s" % (userPasswd)
    print "DB User: %s" % (options.user)
    print "DB Pass: %s" % (dbPasswd)
    print "\033[5;41;37mRESTART NGINX IN ORDER FOR SITE TO BE LIVE\033[0m"

if __name__ == '__main__':
    main()

