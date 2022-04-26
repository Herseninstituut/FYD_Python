# FYD_Python
[![DOI](https://zenodo.org/badge/342858223.svg)](https://zenodo.org/badge/latestdoi/342858223)  
Python scripts to access Follow Your Data (FYD) database


**USAGE:**  
To run either use getFYD.py with:  
> python getFYD.py

Or use jupyter notebook and open the file: 
> saveJSON.ipynb

You need to install mysql-connector-python; e.g conda install mysql-connector-python

Change conn.py to appropriate values for host, username, password and database. 

Both import getdbfields.py to open the dialog for selecting a value for each database field in the database (MYSQL) of your lab. 

When done; click "save" to save a json file at a selected location, "done" updates a cash file in your working directory and you can use the output in your script. "cancel" to exit with no effect.



### The GUI is designed with qtdesigner: 

**USAGE:**  
start qtdesigner in a command window (anaconda), simply with:  designer

open a ui file; opens a graphical window, allows you to drag window controls into your app, to position and edit its attributes.

save this file and convert to python code with pyuic5.bat to a file with py extention.
cmd > pyuic5.bat -x design.ui -o design.py 

Now add callbacks and functionality to the window controls. I've done this in getdbfields.py where the Qt generated files are imported: design.py and NWdlg.py

In getdbfields three classes are defined; 1. a mysql connection class, 2. a New dialog class, and 3. the main dlgfields class. 
