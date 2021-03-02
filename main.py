import os
import json
import string
import random
import hashlib
import getpass
import clipboard
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

print("  ___     _     ___   ___   __  __     _     _  _     _      ___   ___   ___  ")
print(" | _ \   /_\   / __| / __| |  \/  |   /_\   | \| |   /_\    / __| | __| | _ \ ")
print(" |  _/  / _ \  \__ \ \__ \ | |\/| |  / _ \  | .` |  / _ \  | (_ | | _|  |   / ")
print(" |_|   /_/ \_\ |___/ |___/ |_|  |_| /_/ \_\ |_|\_| /_/ \_\  \___| |___| |_|_\ ")
print("                                                                              ")


# region encryption and decryption
class AESCipher(object):
    def __init__(self, key):
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def __pad(self, plain_text):
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text

    @staticmethod
    def __unpad(plain_text):
        last_character = plain_text[len(plain_text) - 1:]
        bytes_to_remove = ord(last_character)
        return plain_text[:-bytes_to_remove]

    def encrypt(self, plain_text):
        plain_text = self.__pad(self, plain_text)
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        f = open("data.crypt", "w")
        f.write(b64encode(iv + encrypted_text).decode("utf-8"))

    def decrypt(self):
        f = open("data.crypt", "r")
        encrypted_text = f.read()
        encrypted_text = b64decode(encrypted_text)
        iv = encrypted_text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
        return self.__unpad(plain_text)


# endregion

# region commands
def list():
    _data = json.loads(data)
    items = [key for key, value in _data.items()]
    print()
    print("Listing all passwords: ")
    for item in items:
        print(" ", item)
    print()


def help():
    return "Listing all avaiable commands:\n help \n list \n view \n quit \n add \n refresh \n delete \n copyuser \n copypass \n destroy"


def view(name):
    _data = json.loads(data)
    return f"{name} \n User: {_data[name]['username']} \n Password: {_data[name]['password']} \n Notes: {_data[name]['notes']}"


def quit():
    exit()


def add():
    print("This WILL OVERWRITE all the SAME NAMED PASSWORDS!")
    name = input("Name: ")
    username = input("Username: ")
    password = input("Password: ")
    if "*#*random" in password:
        _pass = password.split()
        if len(_pass) >= 2:
            if _pass[1].isdigit():
                randomSource = string.ascii_letters + string.digits + string.punctuation
                password = ""
                for i in range(int(_pass[1])):
                    password += random.choice(randomSource)
    notes = input("Notes leave empsaty if none: ")
    _data = json.loads(f"{data}")
    dataToAdd = {
        f"{name if not name == '' else ' '}": {
            "name": f"{name if not name == '' else ' '}",
            "username": f"{username if not username == '' else ' '}",
            "password": f"{password if not password == '' else ' '}",
            "notes": f"{notes if not notes == '' else ' '}"
        }
    }
    _data.update(dataToAdd)
    return json.dumps(_data)


def refresh():
    data = AESCipher.decrypt(AESCipher)


def delete(key):
    ans = input(
        "To confirm that you are deleting the correct password retype the password you whant to delete (this cant be undone): ")
    if ans.lower() == key.lower():
        _data = json.loads(f"{data}")
        del _data[key]
        print(f"Deleted {key}!")
        return json.dumps(_data)
    else:
        _data = json.loads(f"{data}")
        print("Deletion canceled!")
        return json.dumps(_data)


def edit(key):
    _data = json.loads(f"{data}")

    print("Leave empty to skip!")
    name = input(f"Name:{_data[key]['name']}: ")
    username = input(f"Username:{_data[key]['username']}: ")
    password = input(f"Password:{_data[key]['password']}: ")
    notes = input(f"Notes:{_data[key]['notes']}: ")

    if name == "":
        name = _data[key]['name']
        print("saved name")
    if username == "":
        username = _data[key]['username']
        print("saved user")
    if password == "":
        password = _data[key]['password']
        print("saved password")
    elif "*#*random" in password:
        _pass = password.split()
        if len(_pass) >= 2:
            if _pass[1].isdigit():
                randomSource = string.ascii_letters + string.digits + string.punctuation
                password = ""
                for i in range(int(_pass[1])):
                    password += random.choice(randomSource)
    if notes == "":
        notes = _data[key]['notes']

    dataToEdit = {
        f"{name}": {
            "name": f"{name}",
            "username": f"{username}",
            "password": f"{password}",
            "notes": f"{notes}"
        }
    }
    del _data[key]
    _data.update(dataToEdit)
    return json.dumps(_data)


def destroy():
    print("Are you sure you want to DESTROY ALL your passwords? This action can't be undone.")
    ans = input("Yes/no: ")

    if (ans.lower() == "yes"):
        fi = open("data.crypt", "w")
        fi.write("a" for i in range(10000))
        fi.close()
        os.remove("data.crypt")
        exit()
    else:
        print("Destruction cancelled!")


def copyuser(key):
    _data = json.loads(f"{data}")
    clipboard.copy(_data[key]["username"])
    print(f"username for: {key} copied!")


def copypass(key):
    _data = json.loads(f"{data}")
    clipboard.copy(_data[key]["password"])
    print(f"password for: {key} copied!")


# endregion

# region login
if __name__ == "__main__":
    if os.path.isfile("data.crypt"):
        try:
            password = getpass.getpass()
            AESCipher.__init__(AESCipher, password)
            data = AESCipher.decrypt(AESCipher)
        except UnicodeDecodeError:
            print("Incorrect password!")
            exit()
    else:
        password = getpass.getpass(prompt="New password: ")
        AESCipher.__init__(AESCipher, password)
        AESCipher.encrypt(AESCipher, "{}")
        data = AESCipher.decrypt(AESCipher)
        print("Data created succesfuly!")

# endregion

# region loop
while True:
    cmd = input("passmanager: ~$ ").split()
    if not cmd:
        print("Please input command. Type: quit to quit!")
    else:
        if cmd[0].lower() == "help":
            if 1 >= len(cmd):
                print(help())

        elif cmd[0].lower() == "list":
            list()

        elif cmd[0].lower() == "view":
            if 2 <= len(cmd):
                if cmd[1] in data:
                    print(view(cmd[1]))
                else:
                    print(f"No password with name {cmd[1]} found! Use list to list all names!")
            else:
                print("Incorrect usage! Usage: view [name]")

        elif cmd[0].lower() == "quit":
            quit()

        elif cmd[0].lower() == "add":
            data = add()
            AESCipher.encrypt(AESCipher, data)
            refresh()
        elif cmd[0].lower() == "refresh":
            AESCipher.encrypt(AESCipher, data)
            refresh()

        elif cmd[0].lower() == "delete":
            if len(cmd) >= 2:
                if cmd[1] in json.loads(data):
                    data = delete(cmd[1])
                    AESCipher.encrypt(AESCipher, data)
                    refresh()
                else:
                    print(f"{cmd[1]} not found")
            else:
                print("Incorrect usage! Usage: delete [name]")

        elif cmd[0].lower() == "edit":
            if len(cmd) >= 2:
                if cmd[1] in data:
                    data = edit(cmd[1])
                    AESCipher.encrypt(AESCipher, data)
                    refresh()
                else:
                    print(f"No password with name {cmd[1]} found! Use list to list all names!")
            else:
                print("Incorrect usage! Usage: edit [name]")

        elif cmd[0].lower() == "destroy":
            destroy()

        elif cmd[0].lower() == "copyuser":
            if len(cmd) >= 2:
                if cmd[1] in data:
                    copyuser(cmd[1])
                else:
                    print(f"No password with name {cmd[1]} found! Use list to list all names!")
            else:
                print("Incorrect usage! Usage: copyuser [name]")

        elif cmd[0].lower() == "copypass":
            if len(cmd) >= 2:
                if cmd[1] in data:
                    copypass(cmd[1])
                else:
                    print(f"No password with name {cmd[1]} found! Use list to list all names!")
            else:
                print("Incorrect usage! Usage: copypass [name]")

        else:
            print("Command", cmd[0], "not recognised. Use help for help!")
# endregion
