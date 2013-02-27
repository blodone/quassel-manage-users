quassel-manage-users
====================

# What is Quassel

"Quassel IRC is a modern, cross-platform, distributed IRC client, meaning that 
one (or multiple) client(s) can attach to and detach from a central core, much 
like the popular combination of screen and a text-based IRC client such as 
WeeChat, but graphical. In addition to this, Quassel aims to bring a 
pleasurable, comfortable chatting experience to all major platforms 
(including Linux, Windows, and MacOS X as well as Qtopia-based cell phones 
and PDAs), making communication with your peers not only convenient, but 
also ubiquitous available."


# Managing Users

Quassel's distribution package comes with a manageusers.py script which
tries to handle the management of users. However, the functionality of
the default manageusers.py is somewhat not very complete, and often
cannot locate the database that it needs to handle users. 

This version of manageusers.py does so correctly. It modifies the quasselcore 
database to add or remove users, and change an existing user's password.

This allows the creation of users beyond the default single-user scenario. 
In addition. In the default quassel package, while there is a built-in 
--add-user option, it is known to fail.

The version of Quassel in question here is version 0.8.0. This may or may 
not work for versions beyond the above.

Finally, this works only for Quassel installations using SQLite databases.

Usage:  
* manageusers.py (add|changepass|delete) \<username\>  
* manageusers.py (delete) \<username\>  
* manageusers.py list  


