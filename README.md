# Serial port service in Flask

This repository contains the code required for the service to communicate with a Serial port. At this version is just to write a control message to a specific port.


## Getting Started (Python 3.x)
To get started with the Serive please read the following document below.

**Requirements & Setup**
This setup is done with my personal laptop (MacOS Mojave)
- **Python 3**  
`brew install pyenv` (defaults to python3) [version 3.9.6]  
I suggest to use pyvenv to initiate a separate py environment and only use with this project. 
After you get pyenv, run:  
`pyenv install 3.9.6`  
`pyenv local 3.9.6` (when you are in the folder of project)
- **pip** - A python package installer  
`pip`is included with the brew install
- **venv** - Creates python virtual environments for newer versions of python  
`venv` is bundled with python since python 3.3

1. In the root directory of the freshly cloned repo run `python3 -m venv /path/to/the/project/.venv`  
`.venv` is the recommended location for virtual environments
2. Activate the virtual environment by running `source .venv/bin/activate`  
Using python and pip will now draw from the local virtual environment instead of your global system packages
3. Install the project dependencies `pip install -r requirements.txt`  
`requirements.txt` represents the python dependencies required to run the project

## How to start server
In the root directory, open terminal and type `python manage.py run -s dev`
regarding option of -s (setting), we have 3 options: dev, test, prod which will launch project with the config you want  
If you want to run all the tests in project, type the following command:  
`python manage.py test`  
  
After you start the server, in case you don't have any available serial port on your computer, you might want to start some virtual ones to use.  
- On Windows you can use [com0com](http://com0com.sourceforge.net/) or some other paid software to create virtural port [link](https://www.virtual-serial-port.org/articles/top-6-virtual-com-port-apps/)
- On Mac, I found this command is perfect to use: `socat PTY,link=COM8 PTY,link=COM9`
  - first you need to setup socat from brew `brew install socat`
  - then you go to root directory on your computer and run the command above to create two COM8 and COM9 ports, when you write to COM8, you can view the result
  on COM9 by open a terminal and type `screen /COM9` (if you create two ports in root directory, if not you will need to type a full path to COM9
  - **UPDATE**: Pyserial have built-in module to read port: `python -m serial.tools.miniterm <path/to/your/port/port-name>`

## List of Apis
1. `POST /auth`: this to get the access_token to call some other apis that require token
```json
{
    "email": "abc@abc.com", 
    "password": "password"
}
```
2. `POST /sign-up/`: this to register an account
```json
{
    "email": "abc@abc.com", 
    "password": "password"
}
```
3. `GET /ports/`: to get the list of ports on the machine
4. `POST /init-port/`: to create and open a port with the configs
```json
{
    "port": "COM8", //required
    "baudrate": 9600, 
    "bytesize": 8, 
    "stopbits": 1, 
    "parity": "your-option", 
    "flow_control": "your-option", 
    "write_timeout": 1000, 
    "timeout": 1000
}
```
5. `POST /send-msg/`: to send a control message to the serial port
```json
{
  "message": "The message cannot have more than 500 characters including special ones like space"
}
```
