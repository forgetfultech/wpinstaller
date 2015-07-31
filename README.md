WPInstaller
==========================================================

Simple command line utility to automate the Wordpress Installation

WPInstaller:

Creates new System User
Creates new DB User
Creates new DB
Downloads latest version of Wordpress
Installs wordpress into a users direcetory under the sites domain
Changes wp-contents permsissions to install plugins and edit styles



Change the DB connectors login information on line 34 ('<Your User Here>', '<Your Password Here>') to your user and password

Run command with python ./wpinstaller.py -d <domain> -u <user>

Example : python ./wpinstaller.py -d myblog.com -u blogger