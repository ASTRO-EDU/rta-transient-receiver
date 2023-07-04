# rta-transient-receiver

## Description

rta-transient-receiver is a simplified way for handling VoEvents notices provided in xml format.
The program extract the data from the xml file, then writes the notices in a MySQL database and performs several processes for detecting a possible correlation among instruments. Then it sends an email alert to the team for further analysis.

Coverage: 82%

## Installation
The dependencies are listed in the file `requirements.lock`. It is recommended to install them into a virtual enviromnent.

For creating and install a new virtual enviroment: https://docs.python.org/3/library/venv.html

### Dependencies
The following dependencies are required (by the ligo.skymap package) to install the software:
* GCC >= 5
* Python >= 3.9

### Steps for installation:
Create a new virtual enviroment in a folder named venv whith the following command: 
```
python3 -m venv venv
```

Now activate the virtual enviroment whit the command: 
```
source venv/bin/activate
```

Then install the dependency contained in the file requirements.lock in the new virtual enviroment:
```
pip install -r requirements.lock
```

Then install the software:
```
pip install .
```

### Tests
After the installation you can execute the unit tests that can be found in voeventhandler/test
Those tests use dummy voevents provided by the class `dummy_notices.py`.

To run the tests suite:
```
pytest -v voeventhandler/test
```

## The configuration file
A configuration file is mandatory to run the software. It contains the credentials to connect
to the database, customize the behaviour of the email sender and decides how to handle the test notices.
The file `config.template.json` shows the required key-values pairs.

* Section 1: Database
    * `database_user`: the username to connect to the database.
    * `database_password`: the password to connect to the database.
    * `database_host`: the host of the database.
    * `database_port`: the port of the database.
    * `database_name`: the name of the database.
    * `disable_test_notices_seconds`: the number of seconds to wait before processing the test notices.
* Section 2: Email sender
    * `enabled`: if true the email sender is enabled.
    * `packet_with_email_notification`: if true the email sender is enabled for the packet with the given id.
    * `skip_ligo_test`: if true the email sender is disabled for the notices with the ligo test flag.
    * `skip_ste`: if true the email sender is disabled for the notices with the sub-threshold flag (i.e. not-significant for LIGO).
    * `sender_email`: the email address of the sender.    
    * `sender_email_password`: the password of the sender email.  
    * `email_receivers`: the list of the email receivers.
    * `developer_email_receivers`: an email is sent to this list if any runtime exception occurs.
* Section 3: Brokers
    * this section can be empty if the software is not used in a kafka environment.
    * `kafka_client_id`: the client id to connect to the Kafka topics.
    * `kafka_client_secret`: the client secret to connect to the Kafka topics.
    * `topics_to_subscribe`: the list of the topics to subscribe.

## Update dependencies
To update the dependencies relax the packages version constraints in the `requirements.txt` file and run the following commands:
```
pip install pip-tools
pip-compile --generate-hashes --output-file=requirements.lock --resolver=backtracking requirements.txt
```

## Troubleshooting

### MySql
For developing was used mysql 5.7.40 with the option ONLY_FULL_GROUP_BY disabled. 

For checking what options are enabled use the command:
```
SELECT @@sql_mode;
```

For disabling ONLY_FULL_GROUP_BY use the mysql command: 
```
mysql > SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
```

Is important because this query conteined in the class databaseinterface.py can couse problems:
```
SELECT ins.name, max(n.seqnum),n.noticetime, n.receivedsciencealertid, rsa.triggerid,rsa.ste,rsa.time as `trigger_time` from notice n join correlations c on (n.receivedsciencealertid = c.rsaId2) join receivedsciencealert rsa on ( rsa.receivedsciencealertid = n.receivedsciencealertid) join instrument ins on (ins.instrumentid = rsa.instrumentid) where c.rsaId1 = {voeventdata.receivedsciencealertid} group by n.receivedsciencealertid
```

