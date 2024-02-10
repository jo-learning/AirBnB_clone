#!/usr/bin/python3
"""Defines the HBnB console."""

from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from shlex import split
import cmd
import re


def parse(arg):
    curly_brace = re.search(r"\{(.*?)\}", arg)
    bracket = re.search(r"\[(.*?)\]", arg)
    if curly_brace == None:
        if bracket == None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:bracket.span()[0]])
            retur = [i.strip(",") for i in lexer]
            retur.append(bracket.group())
            return retur
    else:
        lexer = split(arg[:curly_brace.span()[0]])
        retur = [i.strip(",") for i in lexer]
        retur.append(curly_brace.group())
        return retur


class HBNBCommand(cmd.Cmd):
    """HolbertonBnB command interpreter.

    Attributes:
        prompt (str): command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing when receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argumentdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match != None:
            argument1 = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argument1[1])
            if match != None:
                command = [argument1[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argumentdict.keys():
                    call = "{} {}".format(argument1[0], command[1])
                    return argumentdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        argument1 = parse(arg)
        if len(argument1) == 0:
            print("** class name missing **")
        elif argument1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argument1[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        argument1 = parse(arg)
        objdict = storage.all()
        if len(argument1) == 0:
            print("** class name missing **")
        elif argument1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argument1) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argument1[0], argument1[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argument1[0], argument1[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        argument1 = parse(arg)
        objdict = storage.all()
        if len(argument1) == 0:
            print("** class name missing **")
        elif argument1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argument1) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argument1[0], argument1[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argument1[0], argument1[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class."""
        argument1 = parse(arg)
        if len(argument1) > 0 and argument1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argument1) > 0 and argument1[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argument1) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argument1 = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argument1[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argument1 = parse(arg)
        objdict = storage.all()

        if len(argument1) == 0:
            print("** class name missing **")
            return False
        if argument1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argument1) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argument1[0], argument1[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argument1) == 2:
            print("** attribute name missing **")
            return False
        if len(argument1) == 3:
            try:
                type(eval(argument1[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argument1) == 4:
            obj = objdict["{}.{}".format(argument1[0],argument1[1])]
            if argument1[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argument1[2]])
                obj.__dict__[argument1[2]] = valtype(argument1[3])
            else:
                obj.__dict__[argument1[2]] = argument1[3]
        elif type(eval(argument1[2])) == dict:
            obj = objdict["{}.{}".format(argument1[0], argument1[1])]
            for k, v in eval(argument1[0]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
