import unittest
from TestUtils import TestChecker
from AST import *


class CheckSuite(unittest.TestCase):
    def test_024(self):
        """
var v TIEN;
const b = v.b;        
type TIEN struct {
    a int;
    b int;
    c int;
}
const a = v.a;
const e = v.e;
        """
        input = Program([VarDecl("v", Id("TIEN"), None), ConstDecl("b", None, FieldAccess(Id("v"), "b")), StructType("TIEN", [("a", IntType()), ("b", IntType()), ("c", IntType())], []), ConstDecl("a", None, FieldAccess(Id("v"), "a")), ConstDecl("e", None, FieldAccess(Id("v"), "e"))])
        self.assertTrue(TestChecker.test(input, "Undeclared Field: e", 24))
