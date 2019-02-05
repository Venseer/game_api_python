# Python Database Example consuming the Giantbomb API. 
Works by seeding the database with platforms and games in a one-to-one relationship and then gives the user RESTful APIs for Game and Platform (including Games and Platforms listing too). Added two flask commands to help with database generation. Examples of GET, POST, PUT, DELETE.

Uses Flask, Flask-restful, Flask-migration and Alchemy

## How to run:

#### Install project dependencies.  
#### If the db.sqlite file is not present create it by running ```flask db upgrade```  
#### Create a Giantbomb Account and add your API Key to the application in settings.py  
#### Run ```flask populate-database```. This will cause the application to consume Giantbomb's API, seeding the database with platforms and games  
#### Once it's done, run ```flask run```  
#### Access api on http://localhost:5000/api/


## Added Flask Commands ###
#### flask populate-database - Cleans the local database and consumes the Giantbomb API in a series of requests, adding all platforms and 100 games of a fix list of 10 consoles.
#### flask clean-database - Wipes the database clean, resetting table indexes.
