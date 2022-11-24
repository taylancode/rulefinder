# RuleFinder - Palo Alto Utility
This is a utility built to work with the Palo Alto firewall management system (Panorama).
It provides the ability to search for any IP/FQDN and find all associated security rules.  

![Demo](https://user-images.githubusercontent.com/88141669/203670698-aa2621a7-1be6-4479-9688-bb131aa7e06e.gif)  

# Inspiration
For anyone unfamiliar with Palo Alto firewalls or managing security rules in general,
there are potentially thousands of rules in any one environment with probably 10x 
more actual objects to be used in said rules. Panorama in this case does give the
ability to search for rules associated with objects but there are a few steps involved. 
For an admin this is not necessarily needed but I've been asked many times to provide
a list of rules for a list of servers and this can be time consuming. With this app,
not only can they search for themselves, it also is much faster than doing it manually. 

# Technologies  
Python  
PostgreSQL  
Flask/Jinja  
HTML/CSS  

## Modules:  
```
External:  
Flask  
requests  
ipaddress  
psycopg2  

Built-In:  
configparser  
functools  
xml.etree.ElementTree  
socket  
re  
os  
```

# Usage  
WARNING: This is not a production ready app and should not be used as such.

Clone the repo into a new folder and have a terminal in the directory.
Update the files as mentioned below.

### constants.py:
```
FLASK_KEY = 'YOUR FLASK KEY'

FW = 'YOUR PANORAMA IP/FQDN'
PA_KEY = 'YOUR API KEY FOR PANORAMA'

DGROUPS = ['ALL DEVICE GROUPS YOU WANT TO QUERY']
```
### database.ini:
```
[postgresql]
host=localhost (Database host location)
database=YOUR DB NAME
user=YOUR DB USER
password=YOUR DB PASSWORD
```

### Getting the app up and running  
`rulefinder.dbupdate` - Update the SQL Database   
`rulefinder` - Start the Flask service
