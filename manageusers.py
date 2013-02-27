#!/usr/bin/python

'''
****************************
* QuasselCore User Manager *
****************************

The QuasselCore user manager modifies the quasselcore database to add
or remove users, and change an existing user's password. 

This allows the creation of users beyond the default single-user
scenario. In addition. In the default quassel package, while 
there is a built-in --add-user option, it is known to fail.

The version of Quassel in question here is version 0.8.0.
This may or may not work for versions beyond the above.

Finally, this works only for Quassel installations using SQLite
databases.

Usage:  manageusers.py (add|changepass|delete) <username> <password>
        manageusers.py list

'''

import os
import sha
import sys
from pprint import pprint


# Import sqlite3 library

try:
    import sqlite3

except ImportError:
    print >> sys.stderr, "ERROR: sqlite3 module not available!"
    print >> sys.stderr, "This script needs sqlite3 support which is part of Python 2.5"
    print >> sys.stderr, "You probably need to upgrade your Python installation first."
    sys.exit(3)


class UserManager(object):
    '''
    UserManager class that encapsulates the functionality of
    reading from the database, and adding, deleting and modifying
    passwords for users in the database

    '''

    def __init__(self):
        '''
        Get SQLite connection to the database.

        '''
        dbpaths = [os.environ['HOME'] + '/.quassel/quassel-storage.sqlite',
                   os.environ['HOME'] + '/.config/quassel-irc.org/quassel-storage.sqlite',
                   '/var/lib/quassel/quassel-storage.sqlite',
                   '/var/cache/quassel/quassel-storage.sqlite']

        self.db = None
        self.cursor = None

        for dbpath in dbpaths:
            if os.path.exists(dbpath):
                print('(info) Using database path %s' % dbpath)
                self.db = sqlite3.connect(dbpath)
                break

        if (self.db):
            self.cursor = self.db.cursor()
            if not (self.cursor):
                print '(error) Got database connection but could not read/write to database.'
                return None
        else:
            print '(error) Could not get database connection.'
            return None


    def __del__(self):
        '''
        Close the database connection.

        '''
        if (self.db):
          self.db.commit()
          self.db.close();

    def _shaCrypt(self, password):
        '''
        Handles SHA.

        '''
        return sha.new(password).hexdigest()

    def add(self, username, password):
        '''
        Adds a user to the database.

        '''
        if (self.db and self.cursor):
            self.cursor.execute('INSERT INTO quasseluser (username, password) VALUES (:username, :password)',
                                {'username':username, 'password':self._shaCrypt(password)}).fetchone()
            print('Adding user %s with password %s.\n' % (username, password))
        else:
            print '(error) Could not add user.'

    def delete(self, username):
        '''
        Removes a user from the database.

        '''
        if (self.db and self.cursor):
            self.cursor.execute('DELETE FROM quasseluser where username=:username', 
                                {'username':username}).fetchone()
            print('Deleting user %s.\n' % username)
        else:
            print '(error) Could not remove user.'

    def changepass(self, username, password):
        '''
        Change the password of a specified user.

        '''
        if (self.db and self.cursor):
            self.cursor.execute('UPDATE quasseluser SET password = :password WHERE username = :username',
                                {'username':username, 'password':self._shaCrypt(password)}).fetchone()
            print('Changing password of user %s to %s.\n' % (username, password))
        else:
            print '(error) Could not change user password.'

    def list(self):
        '''
        Lists all the users in the database.

        '''
        if (self.db and self.cursor):
            return self.cursor.execute("SELECT * FROM quasseluser").fetchall()
        else:
            print '(error) Could not retrieve user list.'
            return None
          
    def callByName(self, name, *args, **kws):
        '''
        Helper method to call class functions.

        '''
        return self.__getattribute__(name)(*args, **kws)

def main():
    try:
        # Grab hold of arguments
        action = sys.argv[1].lower()
    except:
        # No arguments supplied
        print(__doc__)
        return

    usermanager = UserManager()
    if not (usermanager.db or usermanager.cursor):
        return
    
    if action == 'list':
        userlist = usermanager.list()
        if (userlist):
            print 'Users registered with Quasselcore:\n'
            pprint(userlist)
    
    elif action in ['add', 'changepass'] and len(sys.argv) > 3:
        usermanager.callByName(action, sys.argv[2], sys.argv[3])
    
    elif action in ['delete'] and len(sys.argv) > 2:
        usermanager.callByName(action, sys.argv[2])
    
    else:
        print("(error) Invalid argument.")


if __name__ == "__main__":
    main()


