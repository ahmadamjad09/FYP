Note: Use Ubuntu 16.04
Python: 3.5

*****Step 1******
Install Pycharm and MSSql server use the following links
(Pycharm) https://www.jetbrains.com/pycharm/
(MSSql Server) https://www.microsoft.com/en-us/sql-server/sql-server-2017

******Step 2*******
Run Pycharm and create a project. it will automatically create virtual enviroment.

******Step 3******
install libraries that are written in Requirements.txt file using pip3.
pip3 install package name (e.g: pip3 install flask)

******Step 4*******
In app folder copy follwoing files and directories
templates and static director
Application.py, User.py, DB.py, ReadProperty.py, Controller.py and routes.py

******Step 5******
Place project.py and config.py in main directory

******Step 6******
Import EDH.sql in MSSql server

******Step 7******
Export Flask app
export FLASK_APP=project.py

******Step 8******
Finally run flask app
flask run
you will see following output
 * Serving Flask app "project"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Run Browswer or click on link (application will start on port 5000)  

