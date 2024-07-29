#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
from shlex import split
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    """split the input while keeping the contents within curly braces"""
    curlybraces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curlybraces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            hnpl = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in hnpl]
            retl.append(brackets.group())
            return retl
    else:
        hnpl = split(arg[:curlybraces.span()[0]])
        retl = [i.strip(",") for i in hnpl]
        retl.append(curlybraces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines command interpreter"""

    prompt = "(hbnb)"
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
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

    def default(self, arg):
        """Default cmd module when input is invalid"""
        # map commmnad to thir methods
        cmddict = {
                "all": self.do_all,
                "show": self.do_show,
                "destory": self.do_destory,
                "count": self.do_count,
                "create": self.do_create,
                "update": self.do_update
                }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
        match = re.search(r"\((.*?)\)", argl[1])
        if match is not None:
            command = [argl[1][:match.span()[0]], match.group()[1:-1]]
            if command[0] in cmddict.keys():
                call = "{} {}".format(argl[0], command[1])
                return cmddict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_create(self, arg):
        """Create a new class instance and print its id.
        Usage: create <class> <id>
        """
        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argl[0])().id)
            storage.save()

    def do_show(self, arg):
        """ Display string representation of a class instance
        Usage: show <class> <id> or <class>.show(<id>)
        """
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
        """Delete a class instance from given id
        Usage: destroy <class> <id> or <class>.destroy(<id>)
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Delete an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, arg):
        """Display string representations of all instances
        Usage: all or all <class> or <class>.all()
        """
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

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances for a class."""
        argl = parse(arg)
        #  parse(arg) list not empty
        if not argl:
            print("** class name missing **")
            return
        clas_name = arg[0]
        #  verify class exists
        if clas_name not in self.classes:
            print("class doesn't exist")
            return
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
