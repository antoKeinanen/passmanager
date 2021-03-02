# Passmanager
Passmanager is password manager  made in Python. It uses AES encryption standard.

![](https://img.shields.io/github/stars/antoKeinanen/passmanager) 
![](https://img.shields.io/github/forks/antoKeinanen/passmanager)
![](https://img.shields.io/github/release/antoKeinanen/passmanager) 
![](https://img.shields.io/github/issues/antoKeinanen/passmanager)

## Installation
Enter the following commands to in commandline or shell.

``git clone https://github.com/antoKeinanen/passmanager.git``

``cd passmanager``

If you don't have PIP you can install it [HERE](https://pip.pypa.io/en/stable/installing/).

``pip install -r requirements.txt``

## Usage
You can run the passmanager with command ```python3 passmanager.py```

If you open passmanager for the first time it will ask you to create master password. I recommend using at least 10 characters with upper and lowercase letters, numbers, and symbols.
 
Then you will be moved into passmanager mode. You can exit this mode by typing quit.

### Commands
```
help: lists all avaiable commands
list: lists all of your saved passwords
view: view saved password
quit: quits passmanager
add: add a password
refresh: reload your password database
delete: delete password (this can't be undone)
destroy: destroys your whole database (this can't be undone)
copyuser: copies username
copypass: copies password
```

## Roadmap
I will only fix bugs. No new features will be added.

## Support/Ideas/Feedback
Leave me a message in discussions tab!

## Found a bug?
Report it [here](https://github.com/antoKeinanen/passmanager/issues/new?assignees=&labels=&template=bug_report.md&title=)!

## License
[gpl-3.0](https://choosealicense.com/licenses/gpl-3.0/)
