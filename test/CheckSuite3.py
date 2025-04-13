import unittest
from TestUtils import TestChecker
from AST import *


class CheckSuite(unittest.TestCase):

    def test_001(self):
        input = Program([VarDecl("VoTien", None, IntLiteral(1)), VarDecl("VoTien", None, IntLiteral(2))])
        expect = "Redeclared Variable: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 1))

    def test_002(self):
        input = Program([VarDecl("VoTien", None, IntLiteral(1)), ConstDecl("VoTien", None, IntLiteral(2))])
        expect = "Redeclared Constant: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 2))

    def test_003(self):
        input = Program([ConstDecl("VoTien", None, IntLiteral(1)), VarDecl("VoTien", None, IntLiteral(2))])
        expect = "Redeclared Variable: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 3))

    def test_004(self):
        input = Program([ConstDecl("VoTien", None, IntLiteral(1)), FuncDecl("VoTien", [], VoidType(), Block([Return(None)]))])
        expect = "Redeclared Function: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 4))

    def test_005(self):
        input = Program([FuncDecl("VoTien", [], VoidType(), Block([Return(None)])), VarDecl("VoTien", None, IntLiteral(1))])
        expect = "Redeclared Variable: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 5))

    def test_006(self):
        input = Program([VarDecl("getInt", None, IntLiteral(1))])
        expect = "Redeclared Variable: getInt\n"
        self.assertTrue(TestChecker.test(input, expect, 6))

    def test_007(self):
        input = Program([
            StructType("Votien", [("Votien", IntType())], []),
            StructType("TIEN", [("Votien", StringType()), ("TIEN", IntType()), ("TIEN", FloatType())], [])
        ])
        expect = "Redeclared Field: TIEN\n"
        self.assertTrue(TestChecker.test(input, expect, 7))

    def test_008(self):
        input = Program([
            MethodDecl("v", Id("TIEN"), FuncDecl("putIntLn", [], VoidType(), Block([Return(None)]))),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([Return(None)]))),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([Return(None)]))),
            StructType("TIEN", [("Votien", IntType())], [])
        ])
        expect = "Redeclared Method: getInt\n"
        self.assertTrue(TestChecker.test(input, expect, 8))

    def test_009(self):
        input = Program([
            InterfaceType("VoTien", [
                Prototype("VoTien", [], VoidType()),
                Prototype("VoTien", [IntType()], VoidType())
            ])
        ])
        expect = "Redeclared Prototype: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 9))

    def test_010(self):
        input = Program([
            FuncDecl("Votien", [ParamDecl("a", IntType()), ParamDecl("a", IntType())], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 10))

    def test_011(self):
        input = Program([
            FuncDecl("Votien", [ParamDecl("b", IntType())], VoidType(), Block([
                VarDecl("b", None, IntLiteral(1)),
                VarDecl("a", None, IntLiteral(1)),
                ConstDecl("a", None, IntLiteral(1))
            ]))
        ])
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input, expect, 11))

    def test_012(self):
        input = Program([
            FuncDecl("Votien", [ParamDecl("b", IntType())], VoidType(), Block([
                ForStep(
                    VarDecl("a", None, IntLiteral(1)),
                    BinaryOp("<", Id("a"), IntLiteral(1)),
                    Assign(Id("a"), BinaryOp("+", Id("a"), IntLiteral(1))),
                    Block([ConstDecl("a", None, IntLiteral(2))])
                )
            ]))
        ])
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input, expect, 12))

    def test_013(self):
        input = Program([
            VarDecl("a", None, IntLiteral(1)),
            VarDecl("b", None, Id("a")),
            VarDecl("c", None, Id("d"))
        ])
        expect = "Undeclared Identifier: d\n"
        self.assertTrue(TestChecker.test(input, expect, 13))

    def test_014(self):
        input = Program([
            FuncDecl("Votien", [], IntType(), Block([Return(IntLiteral(1))])),
            FuncDecl("foo", [], VoidType(), Block([
                VarDecl("b", None, FuncCall("Votien", [])),
                FuncCall("foo_votine", []),
                Return(None)
            ]))
        ])
        expect = "Undeclared Function: foo_votine\n"
        self.assertTrue(TestChecker.test(input, expect, 14))

    def test_015(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                ConstDecl("c", None, FieldAccess(Id("v"), "Votien")),
                VarDecl("d", None, FieldAccess(Id("v"), "tien"))
            ])))
        ])
        expect = "Undeclared Field: tien\n"
        self.assertTrue(TestChecker.test(input, expect, 15))

    def test_016(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                MethCall(Id("v"), "getInt", []),
                MethCall(Id("v"), "putInt", [])
            ])))
        ])
        expect = "Undeclared Method: putInt\n"
        self.assertTrue(TestChecker.test(input, expect, 16))

    def test_017(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                VarDecl("d", None, FieldAccess(Id("v"), "tien"))
            ])))
        ])
        expect = "Undeclared Field: tien\n"
        self.assertTrue(TestChecker.test(input, expect, 17))

    def test_018(self):
        input = Program([
            StructType("TIEN", [("a", IntType())], []),
            StructType("VO", [("a", IntType())], []),
            InterfaceType("TIEN", [Prototype("foo", [], VoidType())])
        ])
        expect = "Redeclared Type: TIEN\n"
        self.assertTrue(TestChecker.test(input, expect, 18))

    def test_019(self):
        input = Program([
            InterfaceType("TIEN", [
                Prototype("foo", [], VoidType()),
                Prototype("foo", [IntType(), IntType()], VoidType())
            ])
        ])
        expect = "Redeclared Prototype: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 19))

    def test_020(self):
        input = Program([
            FuncDecl("putInt", [], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Function: putInt\n"
        self.assertTrue(TestChecker.test(input, expect, 20))

    def test_021(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("b", IntType())
            ], VoidType(), Block([Return(None)]))),
            FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("a", IntType())
            ], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 21))

    def test_022(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                ConstDecl("c", None, FieldAccess(Id("v"), "Votien")),
                VarDecl("d", None, FieldAccess(Id("v"), "tien"))
            ])))
        ])
        expect = "Undeclared Field: tien\n"
        self.assertTrue(TestChecker.test(input, expect, 22))

    def test_023(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                MethCall(Id("v"), "getInt", []),
                MethCall(Id("v"), "putInt", [])
            ])))
        ])
        expect = "Undeclared Method: putInt\n"
        self.assertTrue(TestChecker.test(input, expect, 23))

    def test_024(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                VarDecl("d", None, FieldAccess(Id("v"), "tien"))
            ])))
        ])
        expect = "Undeclared Field: tien\n"
        self.assertTrue(TestChecker.test(input, expect, 24))

    def test_025(self):
        input = Program([
            StructType("TIEN", [("a", IntType())], []),
            StructType("VO", [("a", IntType())], []),
            InterfaceType("TIEN", [Prototype("foo", [], VoidType())])
        ])
        expect = "Redeclared Type: TIEN\n"
        self.assertTrue(TestChecker.test(input, expect, 25))

    def test_026(self):
        input = Program([
            InterfaceType("TIEN", [
                Prototype("foo", [], VoidType()),
                Prototype("foo", [IntType(), IntType()], VoidType())
            ])
        ])
        expect = "Redeclared Prototype: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 26))

    def test_027(self):
        input = Program([
            FuncDecl("putInt", [], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Function: putInt\n"
        self.assertTrue(TestChecker.test(input, expect, 27))

    def test_028(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("b", IntType())
            ], VoidType(), Block([Return(None)]))),
            FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("a", IntType())
            ], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 28))

    def test_030(self):
        input = Program([VarDecl("VoTien", None, IntLiteral(1)), VarDecl("VoTien", None, IntLiteral(2))])
        expect = "Redeclared Variable: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 30))

    def test_031(self):
        input = Program([VarDecl("VoTien", None, IntLiteral(1)), ConstDecl("VoTien", None, IntLiteral(2))])
        expect = "Redeclared Constant: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 31))

    def test_032(self):
        input = Program([ConstDecl("VoTien", None, IntLiteral(1)), VarDecl("VoTien", None, IntLiteral(2))])
        expect = "Redeclared Variable: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 32))

    def test_033(self):
        input = Program([ConstDecl("VoTien", None, IntLiteral(1)), FuncDecl("VoTien", [], VoidType(), Block([Return(None)]))])
        expect = "Redeclared Function: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 33))

    def test_034(self):
        input = Program([FuncDecl("VoTien", [], VoidType(), Block([Return(None)])), VarDecl("VoTien", None, IntLiteral(1))])
        expect = "Redeclared Variable: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 34))

    def test_035(self):
        input = Program([VarDecl("getInt", None, IntLiteral(1))])
        expect = "Redeclared Variable: getInt\n"
        self.assertTrue(TestChecker.test(input, expect, 35))

    def test_036(self):
        input = Program([
            StructType("Votien", [("Votien", IntType())], []),
            StructType("TIEN", [("Votien", StringType()), ("TIEN", IntType()), ("TIEN", FloatType())], [])
        ])
        expect = "Redeclared Field: TIEN\n"
        self.assertTrue(TestChecker.test(input, expect, 36))

    def test_037(self):
        input = Program([
            MethodDecl("v", Id("TIEN"), FuncDecl("putIntLn", [], VoidType(), Block([Return(None)]))),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([Return(None)]))),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([Return(None)]))),
            StructType("TIEN", [("Votien", IntType())], [])
        ])
        expect = "Redeclared Method: getInt\n"
        self.assertTrue(TestChecker.test(input, expect, 37))

    def test_038(self):
        input = Program([
            InterfaceType("VoTien", [
                Prototype("VoTien", [], VoidType()),
                Prototype("VoTien", [IntType()], VoidType())
            ])
        ])
        expect = "Redeclared Prototype: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 38))

    def test_039(self):
        input = Program([
            FuncDecl("Votien", [ParamDecl("a", IntType()), ParamDecl("a", IntType())], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 39))

    def test_040(self):
        input = Program([
            FuncDecl("Votien", [ParamDecl("b", IntType())], VoidType(), Block([
                VarDecl("b", None, IntLiteral(1)),
                VarDecl("a", None, IntLiteral(1)),
                ConstDecl("a", None, IntLiteral(1))
            ]))
        ])
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input, expect, 40))

    def test_041(self):
        input = Program([
            FuncDecl("Votien", [ParamDecl("b", IntType())], VoidType(), Block([
                ForStep(
                    VarDecl("a", None, IntLiteral(1)),
                    BinaryOp("<", Id("a"), IntLiteral(1)),
                    Assign(Id("a"), BinaryOp("+", Id("a"), IntLiteral(1))),
                    Block([ConstDecl("a", None, IntLiteral(2))])
                )
            ]))
        ])
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input, expect, 41))

    def test_042(self):
        input = Program([
            VarDecl("a", None, IntLiteral(1)),
            VarDecl("b", None, Id("a")),
            VarDecl("c", None, Id("d"))
        ])
        expect = "Undeclared Identifier: d\n"
        self.assertTrue(TestChecker.test(input, expect, 42))

    def test_043(self):
        input = Program([
            FuncDecl("Votien", [], IntType(), Block([Return(IntLiteral(1))])),
            FuncDecl("foo", [], VoidType(), Block([
                VarDecl("b", None, FuncCall("Votien", [])),
                FuncCall("foo_votine", []),
                Return(None)
            ]))
        ])
        expect = "Undeclared Function: foo_votine\n"
        self.assertTrue(TestChecker.test(input, expect, 43))

    def test_044(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                ConstDecl("c", None, FieldAccess(Id("v"), "Votien")),
                VarDecl("d", None, FieldAccess(Id("v"), "tien"))
            ])))
        ])
        expect = "Undeclared Field: tien\n"
        self.assertTrue(TestChecker.test(input, expect, 44))

    def test_045(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                MethCall(Id("v"), "getInt", []),
                MethCall(Id("v"), "putInt", [])
            ])))
        ])
        expect = "Undeclared Method: putInt\n"
        self.assertTrue(TestChecker.test(input, expect, 45))

    def test_046(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                VarDecl("d", None, FieldAccess(Id("v"), "tien"))
            ])))
        ])
        expect = "Undeclared Field: tien\n"
        self.assertTrue(TestChecker.test(input, expect, 46))

    def test_047(self):
        input = Program([
            StructType("TIEN", [("a", IntType())], []),
            StructType("VO", [("a", IntType())], []),
            InterfaceType("TIEN", [Prototype("foo", [], VoidType())])
        ])
        expect = "Redeclared Type: TIEN\n"
        self.assertTrue(TestChecker.test(input, expect, 47))

    def test_048(self):
        input = Program([
            InterfaceType("TIEN", [
                Prototype("foo", [], VoidType()),
                Prototype("foo", [IntType(), IntType()], VoidType())
            ])
        ])
        expect = "Redeclared Prototype: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 48))

    def test_049(self):
        input = Program([
            FuncDecl("putInt", [], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Function: putInt\n"
        self.assertTrue(TestChecker.test(input, expect, 49))

    def test_050(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("b", IntType())
            ], VoidType(), Block([Return(None)]))),
            FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("a", IntType())
            ], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 50))

    def test_051(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                ConstDecl("c", None, FieldAccess(Id("v"), "Votien")),
                VarDecl("d", None, FieldAccess(Id("v"), "tien"))
            ])))
        ])
        expect = "Undeclared Field: tien\n"
        self.assertTrue(TestChecker.test(input, expect, 51))

    def test_052(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                MethCall(Id("v"), "getInt", []),
                MethCall(Id("v"), "putInt", [])
            ])))
        ])
        expect = "Undeclared Method: putInt\n"
        self.assertTrue(TestChecker.test(input, expect, 52))

    def test_053(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                VarDecl("d", None, FieldAccess(Id("v"), "tien"))
            ])))
        ])
        expect = "Undeclared Field: tien\n"
        self.assertTrue(TestChecker.test(input, expect, 53))

    def test_054(self):
        input = Program([
            StructType("TIEN", [("a", IntType())], []),
            StructType("VO", [("a", IntType())], []),
            InterfaceType("TIEN", [Prototype("foo", [], VoidType())])
        ])
        expect = "Redeclared Type: TIEN\n"
        self.assertTrue(TestChecker.test(input, expect, 54))

    def test_055(self):
        input = Program([
            InterfaceType("TIEN", [
                Prototype("foo", [], VoidType()),
                Prototype("foo", [IntType(), IntType()], VoidType())
            ])
        ])
        expect = "Redeclared Prototype: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 55))

    def test_056(self):
        input = Program([
            FuncDecl("putInt", [], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Function: putInt\n"
        self.assertTrue(TestChecker.test(input, expect, 56))

    def test_057(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("b", IntType())
            ], VoidType(), Block([Return(None)]))),
            FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("a", IntType())
            ], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 57))

    def test_058(self):
        input = Program([VarDecl("VoTien", None, IntLiteral(1)), VarDecl("VoTien", None, IntLiteral(2))])
        expect = "Redeclared Variable: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 58))

    def test_059(self):
        input = Program([VarDecl("VoTien", None, IntLiteral(1)), ConstDecl("VoTien", None, IntLiteral(2))])
        expect = "Redeclared Constant: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 59))

    def test_060(self):
        input = Program([ConstDecl("VoTien", None, IntLiteral(1)), VarDecl("VoTien", None, IntLiteral(2))])
        expect = "Redeclared Variable: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 60))

    def test_061(self):
        input = Program([ConstDecl("VoTien", None, IntLiteral(1)), FuncDecl("VoTien", [], VoidType(), Block([Return(None)]))])
        expect = "Redeclared Function: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 61))

    def test_062(self):
        input = Program([FuncDecl("VoTien", [], VoidType(), Block([Return(None)])), VarDecl("VoTien", None, IntLiteral(1))])
        expect = "Redeclared Variable: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 62))

    def test_063(self):
        input = Program([VarDecl("getInt", None, IntLiteral(1))])
        expect = "Redeclared Variable: getInt\n"
        self.assertTrue(TestChecker.test(input, expect, 63))

    def test_064(self):
        input = Program([ConstDecl("VoTien", None, IntLiteral(1)), VarDecl("VoTien", None, IntLiteral(2))])
        expect = "Redeclared Variable: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 64))

    def test_065(self):
        input = Program([ConstDecl("VoTien", None, IntLiteral(1)), FuncDecl("VoTien", [], VoidType(), Block([Return(None)]))])
        expect = "Redeclared Function: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 65))

    def test_066(self):
        input = Program([FuncDecl("VoTien", [], VoidType(), Block([Return(None)])), VarDecl("VoTien", None, IntLiteral(1))])
        expect = "Redeclared Variable: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 66))

    def test_067(self):
        input = Program([VarDecl("getInt", None, IntLiteral(1))])
        expect = "Redeclared Variable: getInt\n"
        self.assertTrue(TestChecker.test(input, expect, 67))

    def test_068(self):
        input = Program([
            StructType("Votien", [("Votien", IntType())], []),
            StructType("TIEN", [("Votien", StringType()), ("TIEN", IntType()), ("TIEN", FloatType())], [])
        ])
        expect = "Redeclared Field: TIEN\n"
        self.assertTrue(TestChecker.test(input, expect, 68))

    def test_069(self):
        input = Program([
            MethodDecl("v", Id("TIEN"), FuncDecl("putIntLn", [], VoidType(), Block([Return(None)]))),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([Return(None)]))),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([Return(None)]))),
            StructType("TIEN", [("Votien", IntType())], [])
        ])
        expect = "Redeclared Method: getInt\n"
        self.assertTrue(TestChecker.test(input, expect, 69))

    def test_070(self):
        input = Program([
            InterfaceType("VoTien", [
                Prototype("VoTien", [], VoidType()),
                Prototype("VoTien", [IntType()], VoidType())
            ])
        ])
        expect = "Redeclared Prototype: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 70))

    def test_071(self):
        input = Program([
            FuncDecl("Votien", [ParamDecl("a", IntType()), ParamDecl("a", IntType())], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 71))

    def test_072(self):
        input = Program([
            FuncDecl("Votien", [ParamDecl("b", IntType())], VoidType(), Block([
                VarDecl("b", None, IntLiteral(1)),
                VarDecl("a", None, IntLiteral(1)),
                ConstDecl("a", None, IntLiteral(1))
            ]))
        ])
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input, expect, 72))

    def test_073(self):
        input = Program([
            FuncDecl("Votien", [ParamDecl("b", IntType())], VoidType(), Block([
                ForStep(
                    VarDecl("a", None, IntLiteral(1)),
                    BinaryOp("<", Id("a"), IntLiteral(1)),
                    Assign(Id("a"), BinaryOp("+", Id("a"), IntLiteral(1))),
                    Block([ConstDecl("a", None, IntLiteral(2))])
                )
            ]))
        ])
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input, expect, 73))

    def test_074(self):
        input = Program([
            VarDecl("a", None, IntLiteral(1)),
            VarDecl("b", None, Id("a")),
            VarDecl("c", None, Id("d"))
        ])
        expect = "Undeclared Identifier: d\n"
        self.assertTrue(TestChecker.test(input, expect, 74))

    def test_075(self):
        input = Program([
            FuncDecl("Votien", [], IntType(), Block([Return(IntLiteral(1))])),
            FuncDecl("foo", [], VoidType(), Block([
                VarDecl("b", None, FuncCall("Votien", [])),
                FuncCall("foo_votine", []),
                Return(None)
            ]))
        ])
        expect = "Undeclared Function: foo_votine\n"
        self.assertTrue(TestChecker.test(input, expect, 75))

    def test_076(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                ConstDecl("c", None, FieldAccess(Id("v"), "Votien")),
                VarDecl("d", None, FieldAccess(Id("v"), "tien"))
            ])))
        ])
        expect = "Undeclared Field: tien\n"
        self.assertTrue(TestChecker.test(input, expect, 76))

    def test_077(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                MethCall(Id("v"), "getInt", []),
                MethCall(Id("v"), "putInt", [])
            ])))
        ])
        expect = "Undeclared Method: putInt\n"
        self.assertTrue(TestChecker.test(input, expect, 77))

    def test_078(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                VarDecl("d", None, FieldAccess(Id("v"), "tien"))
            ])))
        ])
        expect = "Undeclared Field: tien\n"
        self.assertTrue(TestChecker.test(input, expect, 78))

    def test_079(self):
        input = Program([
            StructType("TIEN", [("a", IntType())], []),
            StructType("VO", [("a", IntType())], []),
            InterfaceType("TIEN", [Prototype("foo", [], VoidType())])
        ])
        expect = "Redeclared Type: TIEN\n"
        self.assertTrue(TestChecker.test(input, expect, 79))

    def test_080(self):
        input = Program([
            InterfaceType("TIEN", [
                Prototype("foo", [], VoidType()),
                Prototype("foo", [IntType(), IntType()], VoidType())
            ])
        ])
        expect = "Redeclared Prototype: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 80))

    def test_081(self):
        input = Program([
            FuncDecl("putInt", [], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Function: putInt\n"
        self.assertTrue(TestChecker.test(input, expect, 81))

    def test_082(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("b", IntType())
            ], VoidType(), Block([Return(None)]))),
            FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("a", IntType())
            ], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 82))

    def test_083(self):
        input = Program([
            InterfaceType("VoTien", [
                Prototype("VoTien", [], VoidType()),
                Prototype("VoTien", [IntType()], VoidType())
            ])
        ])
        expect = "Redeclared Prototype: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 83))

    def test_084(self):
        input = Program([
            FuncDecl("Votien", [ParamDecl("a", IntType()), ParamDecl("a", IntType())], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 84))

    def test_085(self):
        input = Program([
            FuncDecl("Votien", [ParamDecl("b", IntType())], VoidType(), Block([
                VarDecl("b", None, IntLiteral(1)),
                VarDecl("a", None, IntLiteral(1)),
                ConstDecl("a", None, IntLiteral(1))
            ]))
        ])
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input, expect, 85))

    def test_086(self):
        input = Program([
            FuncDecl("Votien", [ParamDecl("b", IntType())], VoidType(), Block([
                ForStep(
                    VarDecl("a", None, IntLiteral(1)),
                    BinaryOp("<", Id("a"), IntLiteral(1)),
                    Assign(Id("a"), BinaryOp("+", Id("a"), IntLiteral(1))),
                    Block([ConstDecl("a", None, IntLiteral(2))])
                )
            ]))
        ])
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input, expect, 86))

    def test_087(self):
        input = Program([
            VarDecl("a", None, IntLiteral(1)),
            VarDecl("b", None, Id("a")),
            VarDecl("c", None, Id("d"))
        ])
        expect = "Undeclared Identifier: d\n"
        self.assertTrue(TestChecker.test(input, expect, 87))

    def test_088(self):
        input = Program([
            FuncDecl("Votien", [], IntType(), Block([Return(IntLiteral(1))])),
            FuncDecl("foo", [], VoidType(), Block([
                VarDecl("b", None, FuncCall("Votien", [])),
                FuncCall("foo_votine", []),
                Return(None)
            ]))
        ])
        expect = "Undeclared Function: foo_votine\n"
        self.assertTrue(TestChecker.test(input, expect, 88))

    def test_089(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                ConstDecl("c", None, FieldAccess(Id("v"), "Votien")),
                VarDecl("d", None, FieldAccess(Id("v"), "tien"))
            ])))
        ])
        expect = "Undeclared Field: tien\n"
        self.assertTrue(TestChecker.test(input, expect, 89))

    def test_090(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                MethCall(Id("v"), "getInt", []),
                MethCall(Id("v"), "putInt", [])
            ])))
        ])
        expect = "Undeclared Method: putInt\n"
        self.assertTrue(TestChecker.test(input, expect, 90))

    def test_091(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                VarDecl("d", None, FieldAccess(Id("v"), "tien"))
            ])))
        ])
        expect = "Undeclared Field: tien\n"
        self.assertTrue(TestChecker.test(input, expect, 91))

    def test_092(self):
        input = Program([
            StructType("TIEN", [("a", IntType())], []),
            StructType("VO", [("a", IntType())], []),
            InterfaceType("TIEN", [Prototype("foo", [], VoidType())])
        ])
        expect = "Redeclared Type: TIEN\n"
        self.assertTrue(TestChecker.test(input, expect, 92))

    def test_093(self):
        input = Program([
            InterfaceType("TIEN", [
                Prototype("foo", [], VoidType()),
                Prototype("foo", [IntType(), IntType()], VoidType())
            ])
        ])
        expect = "Redeclared Prototype: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 93))

    def test_094(self):
        input = Program([
            FuncDecl("putInt", [], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Function: putInt\n"
        self.assertTrue(TestChecker.test(input, expect, 94))

    def test_095(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("b", IntType())
            ], VoidType(), Block([Return(None)]))),
            FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("a", IntType())
            ], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 95))

    def test_096(self):
        input = Program([
            FuncDecl("putInt", [], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Function: putInt\n"
        self.assertTrue(TestChecker.test(input, expect, 96))

    def test_097(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("b", IntType())
            ], VoidType(), Block([Return(None)]))),
            FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("a", IntType())
            ], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 97))

    def test_098(self):
        input = Program([
            FuncDecl("putInt", [], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Function: putInt\n"
        self.assertTrue(TestChecker.test(input, expect, 98))

    def test_099(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("b", IntType())
            ], VoidType(), Block([Return(None)]))),
            FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("a", IntType())
            ], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 99))

    def test_100(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("b", IntType())
            ], VoidType(), Block([Return(None)]))),
            FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("a", IntType())
            ], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 100))
