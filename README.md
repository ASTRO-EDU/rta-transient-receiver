# rta-transient-receiver

## Description

rta-transient-receiver is a simplified way for handling VoEvents notices provided in xml format.
The program extract the data from the xml file, then writes the notices in a MySQL database and performs several processes for detecting a possible correlation among instruments. Then it sends an email alert to the team for further analysis.

## Installation
The dependencies are listed in the file requirement.txt. It is recommended to install them into a venv enviromnent.

For creating and install a new virtual enviroment: https://docs.python.org/3/library/venv.html

### Steps for installation:

First of all is important fill the config.json template with the required information. 
You can find this file in voeventhandler/config/config.json

Then create a new virtual enviroment in a folder named venv whith the following command: 
```
python3 -m venv venv
```

Now activate the virtual enviroment whit the command: 
```
source venv/bin/activate
```

Then install the dependency contained in the file requirements.txt in the new virtual enviroment. 
```
pip install -r requirements.txt
```

If you just wanto to use the code use the following command for excecute the file setup.py
```
pip install .
```

If you want to modify the code and test without reinstalling everytime use:
```
pip install -e .
```


### Testing installation
After the installation you can test the voevent handler with the provided test that can be found in voeventhandler/test
Those test use dummy voevent provided by the class test_voevent

For example you can test the whole code using test_VoEventHandler.py:
```
python3 voeventhandler/test/test_VoeventHandler.py
```
This test will simulate multiple call of the main method handleVoevent conteined in the class voeventhandler whith different type of voevent.
For each of those will extract and insert into the database the usefull data from the given xml file and notify the team sending an email. 

## Important email 
The code provides a special function for establish if a voevent is important and sholud be marked in a special way during the email notification. 
You can find this function in the path voeventhandler/emailnotifier.py and it's name is is_important(). 
From deafault configuration this class return False, but you can build yuor own rule creating conditional operations usign the field of the voeventdata object. For a fast look to what this field are look at the class voeventdata contained at path voeventhandler/utilis/voeventdata.py. The tag can be modified in the config file.

## Databasem configuration
For developing was used mysql 5.7.40 with the option ONLY_FULL_GROUP_BY disabled. 

For checking what options are enabled use the command:
```
mysql > SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
```

For disabling ONLY_FULL_GROUP_BY use the mysql command: 
```
mysql > SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
```

Is important because this query conteined in the class databaseinterface.py can couse problems
```
SELECT ins.name, max(n.seqnum),n.noticetime, n.receivedsciencealertid, rsa.triggerid,rsa.ste,rsa.time as `trigger_time` from notice n join correlations c on (n.receivedsciencealertid = c.rsaId2) join receivedsciencealert rsa on ( rsa.receivedsciencealertid = n.receivedsciencealertid) join instrument ins on (ins.instrumentid = rsa.instrumentid) where c.rsaId1 = {voeventdata.receivedsciencealertid} group by n.receivedsciencealertid
```

