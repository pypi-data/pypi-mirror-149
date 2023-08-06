import sys
import unittest

sys.path.append("..")
from readycheck import ReadyCheck, NotReadyError


class TestReadyCheck(unittest.TestCase):
    """Test ReadyCheck class"""

    def test_default_check(self):
        """Test top-level await statements are not rejected"""
        class Default(ReadyCheck):
            foo = None
            bar = 3
            baz = 0

        with self.assertRaises(NotReadyError):
            Default.foo
        self.assertEqual(Default.bar, 3)
        self.assertEqual(Default.baz, 0)

    def test_type_check(self):
        """Test type-based ready check"""
        class TypeCheck(ReadyCheck, check_type=list):
            foo = None
            bar = 3
            baz = []

        with self.assertRaises(NotReadyError):
            TypeCheck.foo
        with self.assertRaises(NotReadyError):
            TypeCheck.bar
        self.assertEqual(TypeCheck.baz, [])

    def test_custom_check(self):
        """Test custom ready check"""
        class CustomCheck(ReadyCheck, check=lambda val: len(val) == 4):
            foo = "oh"
            bar = "allo"
            baz = [1, 2, 3, 4]

        with self.assertRaises(NotReadyError):
            CustomCheck.foo
        self.assertEqual(CustomCheck.bar, "allo")
        self.assertEqual(CustomCheck.baz, [1, 2, 3, 4])

    def test_combined_check(self):
        """Test custom ready check"""
        class CombinedCheck(
            ReadyCheck, check_type=list, check=lambda val: len(val) == 4
        ):
            foo = None
            bar = "allo"
            baz = [1, 2, 3, 4]

        with self.assertRaises(NotReadyError):
            CombinedCheck.foo
        with self.assertRaises(NotReadyError):
            CombinedCheck.bar
        self.assertEqual(CombinedCheck.baz, [1, 2, 3, 4])

    def test_set_attr(self):
        """Test setting attributes"""
        class Default(ReadyCheck):
            foo = None

        with self.assertRaises(NotReadyError):
            Default.foo
        Default.foo = 3
        self.assertEqual(Default.foo, 3)
        Default.new = None
        with self.assertRaises(NotReadyError):
            Default.new
        Default.new = 7
        self.assertEqual(Default.new, 7)

    def test_del_attr(self):
        """Test deleting attributes"""
        class Default(ReadyCheck):
            foo = 3

        delattr(Default, "foo")
        with self.assertRaises(AttributeError):
            Default.foo

    def test_get_raw(self):
        """Test get_raw method"""
        class Default(ReadyCheck):
            foo = None
            bar = 3

        self.assertIsNone(Default.get_raw("foo"))
        self.assertEqual(Default.get_raw("bar"), 3)

    def test_private_attribute(self):
        """Test private attributes access"""
        class Default(ReadyCheck):
            _foo = None

        self.assertIsNone(Default._foo)

    def test_get_raw(self):
        """Test get_raw method"""
        class Default(ReadyCheck):
            foo = None
            bar = 3

        self.assertEqual(Default.get_raw("foo"), None)
        self.assertEqual(Default.get_raw("bar"), 3)

    def test_iter(self):
        """Test iterating protocol"""
        class Default(ReadyCheck):
            foo = None
            bar = 3

        self.assertEqual(list(Default), ["foo", "bar"])
        Default.new = 4
        self.assertEqual(list(Default), ["foo", "bar", "new"])
        delattr(Default, "bar")
        self.assertEqual(list(Default), ["foo", "new"])

    def test_exception_attributes(self):
        """Test NotReadyError attributes"""
        class Default(ReadyCheck):
            foo = None

        with self.assertRaises(NotReadyError) as cm:
            Default.foo
        self.assertEqual(cm.exception.class_, Default)
        self.assertEqual(cm.exception.attr, "foo")
