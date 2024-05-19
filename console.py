#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
from shlex import split
import re
from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """Defines command interpreter"""

    prompt = "(hbnb)"
    __classes = {
            "BaseModel",
            "User"
            }

    def define_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def define_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
