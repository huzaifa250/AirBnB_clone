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


if __name__ == "__main__":
    unittest.main()
