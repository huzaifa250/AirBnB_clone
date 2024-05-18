#!/usr/bin/python3
"""Defines unittests for base_model"""
from models.base_model import BaseModel
import os
import models
import unittest
from datetime import datetime
from time import sleep


class TestBaseModel_instantiation(unittest.TestCase):
    """Testing instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_id_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_models_have_unique_ids(self):
        base_m1 = BaseModel()
        base_m2 = BaseModel()
        self.assertNotEqual(base_m1.id, base_m2.id)

    def test_models_created_at_diffrent_time(self):
        bm1 = BaseModel()
        sleep(0.06)
        bm2 = BaseModel()
        self.assertLess(bm1.created_at, bm2.created_at)

    def test_models_updated_at_different_time(self):
        bm1 = BaseModel()
        sleep(0.06)
        bm2 = BaseModel()
        self.assertLess(bm1.updated_at, bm2.updated_at)

    def test_unused_args(self):
        base_m = BaseModel(None)
        self.assertNotIn(None, base_m.__dict__.values())

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        base_m = BaseModel()
        base_m.id = "123456"
        base_m.created_at = base_m.updated_at = dt
        bmstr = base_m.__str__()
        self.assertIn("[BaseModel] (123456)", bmstr)
        self.assertIn("'id': '123456'", bmstr)
        self.assertIn("'created_at': " + dt_repr, bmstr)
        self.assertIn("'updated_at': " + dt_repr, bmstr)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_with_args_and_kwargs(self):
        dat = datetime.today()
        dat_iso = dat.isoformat()
        bm = BaseModel("12", id="345", created_at=dat_iso, updated_at=dat_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dat)
        self.assertEqual(bm.updated_at, dat)


class TestBaseModelSave(unittest.TestCase):
    """Testing save method of the BaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("temp", "file.json")
        except IOError:
            pass

    def test_one(self):
        base_m = BaseModel()
        sleep(0.06)
        first_updated_at = base_m.updated_at
        base_m.save()
        self.assertLess(first_updated_at, base_m.updated_at)

    def test_two(self):
        base_m = BaseModel()
        sleep(0.06)
        first_updated_at = base_m.updated_at
        base_m.save()
        second_updated_at = base_m.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.06)
        base_m.save()
        self.assertLess(second_updated_at, base_m.updated_at)

    def test_save_with_arg(self):
        base_m = BaseModel()
        with self.assertRaises(TypeError):
            base_m.save(None)

    def test_updates_file(self):
        base_mu = BaseModel()
        base_mu.save()
        bmid = "BaseModel." + base_mu.id
        with open("file.json", "r") as f:
            self.assertIn(bmid, f.read())


class TestToDict(unittest.TestCase):
    """Testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        base_m = BaseModel()
        self.assertTrue(dict, type(base_m.to_dict()))

    def test_contains_correct_keys(self):
        base_m = BaseModel()
        self.assertIn("id", base_m.to_dict())
        self.assertIn("created_at", base_m.to_dict())
        self.assertIn("updated_at", base_m.to_dict())
        self.assertIn("__class__", base_m.to_dict())

    def test_contains_added_attributes(self):
        base_m = BaseModel()
        base_m.name = "Test"
        base_m.my_number = 98
        self.assertIn("name", base_m.to_dict())
        self.assertIn("my_number", base_m.to_dict())

    def test_to_dict_output(self):
        dt = datetime.today()
        bmo = BaseModel()
        bmo.id = "12345"
        bmo.created_at = bmo.updated_at = dt
        tdict = {
            'id': '12345',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(bmo.to_dict(), tdict)

    def test_contrast_dunder_dict(self):
        bmc = BaseModel()
        self.assertNotEqual(bmc.to_dict(), bmc.__dict__)

    def test_with_arg(self):
        bm_arg = BaseModel()
        with self.assertRaises(TypeError):
            bm_arg.to_dict(None)


if __name__ == "__main__":
    unittest.main()
