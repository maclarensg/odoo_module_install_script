#!/usr/bin/env python
import sys
import ConfigParser

from pprint import pprint

import odoorpc


# main
def  main(list):

    # Read configurations and parse them to variables
    Config = ConfigParser.ConfigParser()
    Config.read("./config.ini")

    host = Config.get('host', 'host')
    port = int(Config.get('host', 'port'))

    db_name = Config.get('database', 'db_name')
    user = Config.get('database', 'user')
    passwd = Config.get('database', 'passwd')

    # Prepare the connection to the server
    odoo = odoorpc.ODOO(host, port)    

    # Check if db_name exist in db list
    if db_name not in odoo.db.list():
        sys.exit("DB %s not found in db list" % db_name)
    
    # Login
    odoo.login(db_name, user, passwd)
    
    # Module is 'ir.module.module'
    Module = odoo.env['ir.module.module']
    
    # Iterate the list of items to install
    for item in list:
        # Get the module ids by name
        module_ids = Module.search([['name', '=', item]])

        # there should be 1 module in module_ids, but iterate for each module object
        for module in Module.browse(module_ids):
            if module.state == 'installed':
                # If installed, just print that it has install
                print "%s has already been installed." % module.name
            else:
                # Otherwise, install it
                sys.stdout.write("Installing %s ... " % module.name)
                module.button_immediate_install()
                print "Done."
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage:\n./install_module.py <module 1> <module 2> .. <module n>")
    
    # Get module list from argv
    modules_list = sys.argv
    modules_list.pop(0)
    
    # call main 
    main(modules_list)      
