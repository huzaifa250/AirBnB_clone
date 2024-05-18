#!/usr/bin/python3
"""Defines the BaseModel class for all other classes."""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Represents the BaseModel class for the  project."""
    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel."""
        self.id = str(uuid4())  # unique id for each BaseModel
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        time_f = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, time_f)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def __str__(self):
        """Return the print/str representation of the BaseModel obj."""
        # Get the class name of the instance
        clname = self.__class__.__name__
        # Format and return the string representation
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)

    def save(self):
        """Update updated_at with the current datetime"""
        # Update the 'updated_at' attribute with the current date and time
        self.updated_at = datetime.today()
        # Save the current state of the obj to persistent storage
        models.storage.save()

    def to_dict(self):
        """converts an instance of the BaseModel class into dictionary"""
        # Create a shallow copy of the instance's dictionary
        rsdict = self.__dict__.copy()
        # Convert datetime attributes to ISO format
        rsdict["created_at"] = self.created_at.isoformat()
        rsdict["updated_at"] = self.updated_at.isoformat()
        # Include the class name
        rsdict["__class__"] = self.__class__.__name__
        # Return the resulting dictionary
        return rsdict
