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

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def emptyline(self):
        """Don't execute anything."""
        pass

    def split(arg):
        """Splits the argument string by spaces"""
        return arg.split()

    def parse(arg):
        """split the input while keeping the contents within curly braces"""
        curlybraces = re.search(r"\{(.*?)\}", arg)
        brackets = re.search(r"\[(.*?)\]", arg)
        if curlybraces is None and brackets is None:
            return [inp.strip(",") for inp in split(arg)]
        elif brackets is not None:
            # handle input up to the point where brackets start
            hnpl = split(arg[:brackets.span()[0]])
            # remove any trailing commas in hnpl
            retl = [inp.strip(",") for inp in hnpl]
            retl.append(brackets.group())
            return retl
        else:
            hnpl = split(arg[:curlybraces.span()[0]])
            retl = [inp.strip(",") for inp in hnpl]
            retl.append(curlybraces.group())
            return retl

    def do_create(self, arg):
        """Create a new class instance and print its id."""
        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            #  map class names(as strings) to their corresponding class
            cls = HBNBCommand.__classes[argl[0]]
            new_instance = cls()
            print(new_instance.id)
            new_instance.save()
            storage.save()

    def do_show(self, arg):
        """ Display string representation of a class instance"""
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, arg):
        """Delete a class instance fro given id"""
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_all(self, arg):
        """Display string representations of all instances """
        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_update(self, arg):
        """Update a class instance of a given id by adding or updating
           a given attribute key/value or dict"""
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
            storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
