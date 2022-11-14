## rta-transient-receiver

# Description

rta-transient-receiver is a simplified way for handling VoEvents notices in xml format.
The program extract the data from the xml file, then writes the notices in a MySQL database and performs several processes for detecting a possible correlation among instruments. Then it sends an email alert to the team for further analysis.

# Installation
The dependencies are listed in the file requirement.txt. It is recommended to install them into a venv enviromnent.

For creating and install a new virtual enviroment: https://docs.python.org/3/library/venv.html

Step to install:

First of all is important fill the config.json template with the required information. 
You can find this file in voeventhandler/config/config.json

Then create a new virtual enviroment whith the following command: 

```
python3 -m venv /path/to/new/virtual/environment
```

Then install the dependency contained in the file requirements.txt in the new virtual enviroment. 

```
pip install -r requirements.txt
```

Then use the following command for install the code into the virtual enviroment.

```
pip install .
```

#Testing installation
After the installation you can test the voevent handler with the provided test that can be found in voeventhandler/test
