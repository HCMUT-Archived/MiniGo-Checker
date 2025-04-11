import unittest
from TestUtils import TestChecker
from AST import *


class CheckSuite(unittest.TestCase):
    def test_001(self):
        """
var VoTien = 1; 
var VoTien = 2;
        """
        input = Program([VarDecl("VoTien", None, IntLiteral(1)), VarDecl("VoTien", None, IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: VoTien", 1))

    def test_002(self):
        """
var VoTien = 1; 
const VoTien = 2;
        """
        input = Program([VarDecl("VoTien", None, IntLiteral(1)), ConstDecl("VoTien", None, IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: VoTien", 2))

    def test_003(self):
        """
const VoTien = 1; 
var VoTien = 2;
        """
        input = Program([ConstDecl("VoTien", None, IntLiteral(1)), VarDecl("VoTien", None, IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: VoTien", 3))

    def test_004(self):
        """
const VoTien = 1; 
func VoTien () {return;}
        """
        input = Program([ConstDecl("VoTien", None, IntLiteral(1)), FuncDecl("VoTien", [], VoidType(), Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Function: VoTien", 4))

    def test_005(self):
        """ 
func VoTien () {return;}
var VoTien = 1;
        """
        input = Program([FuncDecl("VoTien", [], VoidType(), Block([Return(None)])), VarDecl("VoTien", None, IntLiteral(1))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: VoTien", 5))

    def test_006(self):
        """ 
var getInt = 1;
        """
        input = Program([VarDecl("getInt", None, IntLiteral(1))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: getInt", 6))

    def test_007(self):
        """ 
type  Votien struct {
    Votien int;
}
type TIEN struct {
    Votien string;
    TIEN int;
    TIEN float;
}
        """
        input = Program([StructType("Votien", [("Votien", IntType())], []), StructType("TIEN", [("Votien", StringType()), ("TIEN", IntType()), ("TIEN", FloatType())], [])])
        self.assertTrue(TestChecker.test(input, "Redeclared Field: TIEN", 7))

    def test_008(self):
        """ 
func (v TIEN) putIntLn () {return;}
func (v TIEN) getInt () {return;}
func (v TIEN) getInt () {return;}
type TIEN struct {
    Votien int;
}
        """
        input = Program([MethodDecl("v", Id("TIEN"), FuncDecl("putIntLn", [], VoidType(), Block([Return(None)]))), MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([Return(None)]))), MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([Return(None)]))), StructType("TIEN", [("Votien", IntType())], [])])
        self.assertTrue(TestChecker.test(input, "Redeclared Method: getInt", 8))

    def test_009(self):
        """ 
type VoTien interface {
    VoTien ();
    VoTien (a int);
}
        """
        input = Program([InterfaceType("VoTien", [Prototype("VoTien", [], VoidType()), Prototype("VoTien", [IntType()], VoidType())])])
        self.assertTrue(TestChecker.test(input, "Redeclared Prototype: VoTien", 9))

    def test_010(self):
        """ 
func Votien (a, a int) {return;}
        """
        input = Program([FuncDecl("Votien", [ParamDecl("a", IntType()), ParamDecl("a", IntType())], VoidType(), Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Parameter: a", 10))

    def test_011(self):
        """ 
func Votien (b int) {
    var b = 1;
    var a = 1;
    const a = 1;
}
        """
        input = Program([FuncDecl("Votien", [ParamDecl("b", IntType())], VoidType(), Block([VarDecl("b", None, IntLiteral(1)), VarDecl("a", None, IntLiteral(1)), ConstDecl("a", None, IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: a", 11))

    def test_012(self):
        """ 
func Votien (b int) {
    for var a = 1; a < 1; a += 1 {
        const a = 2;
    }
}
        """
        input = Program([FuncDecl("Votien", [ParamDecl("b", IntType())], VoidType(), Block([ForStep(VarDecl("a", None, IntLiteral(1)), BinaryOp("<", Id("a"), IntLiteral(1)), Assign(Id("a"), BinaryOp("+", Id("a"), IntLiteral(1))), Block([ConstDecl("a", None, IntLiteral(2))]))]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: a", 12))

    def test_013(self):
        """ 
var a = 1;
var b = a;
var c = d;
        """
        input = Program([VarDecl("a", None, IntLiteral(1)), VarDecl("b", None, Id("a")), VarDecl("c", None, Id("d"))])
        self.assertTrue(TestChecker.test(input, "Undeclared Identifier: d", 13))

    def test_014(self):
        """ 
func Votien () int {return 1;}

fun foo () {
    var b = Votien();
    foo_votine();
    return;
}
        """
        input = Program([FuncDecl("Votien", [], IntType(), Block([Return(IntLiteral(1))])), FuncDecl("foo", [], VoidType(), Block([VarDecl("b", None, FuncCall("Votien", [])), FuncCall("foo_votine", []), Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Undeclared Function: foo_votine", 14))

    def test_015(self):
        """ 
type TIEN struct {
    Votien int;
}

func (v TIEN) getInt () {
    const c = v.Votien;
    var d = v.tien;
}
        """
        input = Program([StructType("TIEN", [("Votien", IntType())], []), MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([ConstDecl("c", None, FieldAccess(Id("v"), "Votien")), VarDecl("d", None, FieldAccess(Id("v"), "tien"))])))])
        self.assertTrue(TestChecker.test(input, "Undeclared Field: tien", 15))

    def test_016(self):
        """ 
type TIEN struct {
    Votien int;
}

func (v TIEN) getInt () {
    v.getInt ();
    v.putInt ();
}
        """
        input = Program([StructType("TIEN", [("Votien", IntType())], []), MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([MethCall(Id("v"), "getInt", []), MethCall(Id("v"), "putInt", [])])))])
        self.assertTrue(TestChecker.test(input, "Undeclared Method: putInt", 16))

    def test_017(self):
        """ 
type TIEN struct {Votien int;}
type TIEN interface {VoTien ();}

        """
        input = Program([StructType("TIEN", [("Votien", IntType())], []), InterfaceType("TIEN", [Prototype("VoTien", [], VoidType())])])
        self.assertTrue(TestChecker.test(input, "Redeclared Type: TIEN", 17))

    def test_018(self):
        """func putInt() {return;}"""
        input = Program([FuncDecl("putInt", [], VoidType(), Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Function: putInt", 18))

    def test_019(self):
        """
type TIEN struct {
    Votien int;
}
func (v TIEN) foo (v int) {return;}
func foo () {return;}
        """
        input = Program([StructType("TIEN", [("Votien", IntType())], []), MethodDecl("v", Id("TIEN"), FuncDecl("foo", [ParamDecl("v", IntType())], VoidType(), Block([Return(None)]))), FuncDecl("foo", [], VoidType(), Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "VOTIEN", 19))

    def test_020(self):
        """
const a = 2;
func foo () {
    const a = 1;
    for a < 1 {
        const a = 1;
        for a < 1 {
            const a = 1;
            const b = 1;
        }
        const b = 1;
        var a = 1;
    }
}  
        """
        input = Program([ConstDecl("a", None, IntLiteral(2)), FuncDecl("foo", [], VoidType(), Block([ConstDecl("a", None, IntLiteral(1)), ForBasic(BinaryOp("<", Id("a"), IntLiteral(1)), Block([ConstDecl("a", None, IntLiteral(1)), ForBasic(BinaryOp("<", Id("a"), IntLiteral(1)), Block([ConstDecl("a", None, IntLiteral(1)), ConstDecl("b", None, IntLiteral(1))])), ConstDecl("b", None, IntLiteral(1)), VarDecl("a", None, IntLiteral(1))]))]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: a", 20))

    def test_021(self):
        """
func foo () {
    const a = 1;
    for a, b := range [3]int {1, 2, 3} {
        var b = 1;
    }
}
        """
        input = Program([FuncDecl("foo", [], VoidType(), Block([ConstDecl("a", None, IntLiteral(1)), ForEach(Id("a"), Id("b"), ArrayLiteral([IntLiteral(3)], IntType(), [IntLiteral(1), IntLiteral(2), IntLiteral(3)]), Block([VarDecl("b", None, IntLiteral(1))]))]))])
        self.assertTrue(TestChecker.test(input, "Undeclared Identifier: b", 21))

    def test_022(self):
        """
var a = foo();
func foo () int {
    var a =  koo();
    var c = getInt();
    putInt(c);
    putIntLn(c);
    return 1;
}
var d = foo();
func koo () int {
    var a =  foo ();
    return 1;
}
        """
        input = Program([VarDecl("a", None, FuncCall("foo", [])), FuncDecl("foo", [], IntType(), Block([VarDecl("a", None, FuncCall("koo", [])), VarDecl("c", None, FuncCall("getInt", [])), FuncCall("putInt", [Id("c")]), FuncCall("putIntLn", [Id("c")]), Return(IntLiteral(1))])), VarDecl("d", None, FuncCall("foo", [])), FuncDecl("koo", [], IntType(), Block([VarDecl("a", None, FuncCall("foo", [])), Return(IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(input, "VOTIEN", 22))

    def test_023(self):
        """
type TIEN struct {
    Votien int;
}
func (v TIEN) foo (a, b int) {return;}
func foo (a, a int) {return;}
        """
        input = Program([StructType("TIEN", [("Votien", IntType())], []), MethodDecl("v", Id("TIEN"), FuncDecl("foo", [ParamDecl("a", IntType()), ParamDecl("b", IntType())], VoidType(), Block([Return(None)]))), FuncDecl("foo", [ParamDecl("a", IntType()), ParamDecl("a", IntType())], VoidType(), Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Parameter: a", 23))

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

    def test_025(self):
        """
var v TIEN;      
type TIEN struct {
    a int;
} 
type VO interface {
    foo() int;
}

func (v TIEN) foo() int {return 1;}
func (b TIEN) koo() {b.koo();}
func foo() {
    var x VO;  
    const b = x.foo(); 
    x.koo(); 
}
        """
        input = Program([VarDecl("v", Id("TIEN"), None), StructType("TIEN", [("a", IntType())], []), InterfaceType("VO", [Prototype("foo", [], IntType())]), MethodDecl("v", Id("TIEN"), FuncDecl("foo", [], IntType(), Block([Return(IntLiteral(1))]))), MethodDecl("b", Id("TIEN"), FuncDecl("koo", [], VoidType(), Block([MethCall(Id("b"), "koo", [])]))), FuncDecl("foo", [], VoidType(), Block([VarDecl("x", Id("VO"), None), ConstDecl("b", None, MethCall(Id("x"), "foo", [])), MethCall(Id("x"), "koo", [])]))])
        self.assertTrue(TestChecker.test(input, "Undeclared Method: koo", 25))

    def test_026(self):
        """
func foo(){
    return
}
func foo1() int{
    return 1
}
func foo2() float{
    return 2
}
        """
        input = Program([FuncDecl("foo", [], VoidType(), Block([Return(None)])), FuncDecl("foo1", [], IntType(), Block([Return(IntLiteral(1))])), FuncDecl("foo2", [], FloatType(), Block([Return(IntLiteral(2))]))])
        self.assertTrue(TestChecker.test(input, "Type Mismatch: Return(IntLiteral(2))", 26))

    def test_027(self):
        """
var a = [2] int {1, 2}
var c [2] float = a
        """
        input = Program([VarDecl("a", None, ArrayLiteral([IntLiteral(2)], IntType(), [IntLiteral(1), IntLiteral(2)])), VarDecl("c", ArrayType([IntLiteral(2)], FloatType()), Id("a"))])
        self.assertTrue(TestChecker.test(input, "VOTIEN", 27))

    def test_028(self):
        """
type S1 struct {votien int;}
type I1 interface {votien();}
var a I1;
var c I1 = nil;
var d S1 = nil;
func foo(){
    c := a;
    a := nil;
}

var e int = nil;
"""
        input = Program([StructType("S1", [("votien", IntType())], []), InterfaceType("I1", [Prototype("votien", [], VoidType())]), VarDecl("a", Id("I1"), None), VarDecl("c", Id("I1"), NilLiteral()), VarDecl("d", Id("S1"), NilLiteral()), FuncDecl("foo", [], VoidType(), Block([Assign(Id("c"), Id("a")), Assign(Id("a"), NilLiteral())])), VarDecl("e", IntType(), NilLiteral())])
        self.assertTrue(TestChecker.test(input, "Type Mismatch: VarDecl(e,IntType,Nil)", 28))

    def test_029(self):
        """
var a boolean = 1 > 2;
var b boolean = 1.0 < 2.0;
var c boolean = "1" == "2";
var d boolean = 1 > 2.0;
        """
        input = Program([VarDecl("a", BoolType(), BinaryOp(">", IntLiteral(1), IntLiteral(2))),
                         VarDecl("b", BoolType(), BinaryOp("<", FloatLiteral(1.0), FloatLiteral(2.0))),
                         VarDecl("c", BoolType(), BinaryOp("==", StringLiteral(""" "1" """), StringLiteral(""" "2" """))),
                         VarDecl("d", BoolType(), BinaryOp(">", IntLiteral(1), FloatLiteral(2.0)))])
        self.assertTrue(TestChecker.test(input, "Type Mismatch: BinaryOp(IntLiteral(1),>,FloatLiteral(2.0))", 29))

    def test_030(self):
        """
var a = 1 + 2.0;
var b = 1 + 1;
func foo() int {
    return b;
    return a;
}
        """
        input = Program([VarDecl("a", None, BinaryOp("+", IntLiteral(1), FloatLiteral(2.0))), VarDecl("b", None, BinaryOp("+", IntLiteral(1), IntLiteral(1))), FuncDecl("foo", [], IntType(), Block([Return(Id("b")), Return(Id("a"))]))])
        self.assertTrue(TestChecker.test(input, "Type Mismatch: Return(Id(a))", 30))

    def test_031(self):
        """
type S1 struct {votien int;}
type I1 interface {votien() int;}
func (s S1) votien() int {return 1;}

var s S1;
var a int = s.votien(1);
        """
        input = Program([StructType("S1", [("votien", IntType())], []), InterfaceType("I1", [Prototype("votien", [], IntType())]), MethodDecl("s", Id("S1"), FuncDecl("votien", [], IntType(), Block([Return(IntLiteral(1))]))), VarDecl("s", Id("S1"), None), VarDecl("a", IntType(), MethCall(Id("s"), "votien", [IntLiteral(1)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Method: votien", 31))

    def test_032(self):
        """
type Person struct {
    name string ;
    age int ;
}

func  votien()  {
    var person = Person{name: "Alice", age: 30}
    person.name := "John";
    person.age := 30;
    putStringLn(person.name)
    putStringLn(person.Greet())
}

func (p Person) Greet() string {
return "Hello, " + p.name
}
        """
        input = Program([StructType("Person", [
            ("name", StringType()),
            ("age", IntType())
        ], []),
            FuncDecl("votien", [], VoidType(),
                     Block([VarDecl("person", None, StructLiteral("Person", [("name", StringLiteral(""" "Alice" """)), ("age", IntLiteral(30))])), Assign(FieldAccess(Id("person"), "name"), StringLiteral(""" "John" """)), Assign(FieldAccess(Id("person"), "age"), IntLiteral(30)), FuncCall("putStringLn", [FieldAccess(Id("person"), "name")]), FuncCall("putStringLn", [MethCall(Id("person"), "Greet", [])])])), MethodDecl("p", Id("Person"), FuncDecl("Greet", [], StringType(), Block([Return(BinaryOp("+", StringLiteral(""" "Hello, " """), FieldAccess(Id("p"), "name")))])))])
        self.assertTrue(TestChecker.test(input, "VOTIEN", 32))

    def test_033(self):
        """
type putLn struct {a int;};
        """
        input = Program([StructType("putLn", [("a", IntType())], [])])
        self.assertTrue(TestChecker.test(input, "Redeclared Type: putLn", 33))

    def test_034(self):
        """
type putLn interface {foo();};
        """
        input = Program([InterfaceType("putLn", [Prototype("foo", [], VoidType())])])
        self.assertTrue(TestChecker.test(input, "Redeclared Type: putLn", 34))

    def test_035(self):
        """
func foo() {
    putFloat(getInt());
}
"""
        input = Program([FuncDecl("foo", [], VoidType(), Block([FuncCall("putFloat", [FuncCall("getInt", [])])]))])
        self.assertTrue(TestChecker.test(input, "Type Mismatch: FuncCall(putFloat,[FuncCall(getInt,[])])", 35))

    def test_036(self):
        """
type TIEN struct {a [2]int;} 
type VO interface {foo() int;}

func (v TIEN) foo() int {return 1;}

func foo(a VO) {
    var b = TIEN{a: [2]int{1, 2}};
    foo(b)
}        
        """
        input = Program([StructType("TIEN", [("a", ArrayType([IntLiteral(2)], IntType()))], []), InterfaceType("VO", [Prototype("foo", [], IntType())]), MethodDecl("v", Id("TIEN"), FuncDecl("foo", [], IntType(), Block([Return(IntLiteral(1))]))), FuncDecl("foo", [ParamDecl("a", Id("VO"))], VoidType(), Block([VarDecl("b", None, StructLiteral("TIEN", [("a", ArrayLiteral([IntLiteral(2)], IntType(), [IntLiteral(1), IntLiteral(2)]))])), FuncCall("foo", [Id("b")])]))])
        self.assertTrue(TestChecker.test(input, "Type Mismatch: FuncCall(foo,[Id(b)])", 36))

    def test_037(self):
        """
var A = 1;
type A struct {a int;}
        """
        input = Program([VarDecl("A", None, IntLiteral(1)), StructType("A", [("a", IntType())], [])])
        self.assertTrue(TestChecker.test(input, "Redeclared Type: A", 37))

    def test_038(self):
        """
type A interface {foo();}
const A = 2;
        """
        input = Program([InterfaceType("A", [Prototype("foo", [], VoidType())]), ConstDecl("A", None, IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: A", 38))

    def test_039(self):
        """
func A() {
    return A;
}
"""
        input = Program([FuncDecl("A", [], VoidType(), Block([Return(Id("A"))]))])
        self.assertTrue(TestChecker.test(input, "Undeclared Identifier: A", 39))

    def test_040(self):
        """
type S1 struct {votien int;}
type I1 interface {votien();}

func (s S1) votien() {return;}

var b [2] S1;
var a [2] I1 = b;
        """
        input = Program([StructType("S1", [("votien", IntType())], []),
                         InterfaceType("I1", [Prototype("votien", [], VoidType())]),
                         MethodDecl("s", Id("S1"), FuncDecl("votien", [], VoidType(), Block([Return(None)]))),
                         VarDecl("b", ArrayType([IntLiteral(2)], Id("S1")), None),
                         VarDecl("a", ArrayType([IntLiteral(2)], Id("I1")), Id("b"))])
        self.assertTrue(TestChecker.test(input, "Redeclared Method: votien", 40))

    def test_041(self):
        """
func foo() [2] float {
    return [2] float {1.0, 2.0};
    return [2] int {1, 2};
}
        """
        input = Program([FuncDecl("foo", [], ArrayType([IntLiteral(2)], FloatType()), Block([Return(ArrayLiteral([IntLiteral(2)], FloatType(), [FloatLiteral(1.0), FloatLiteral(2.0)])), Return(ArrayLiteral([IntLiteral(2)], IntType(), [IntLiteral(1), IntLiteral(2)]))]))])
        self.assertTrue(TestChecker.test(input, "Type Mismatch: Return(ArrayLiteral([IntLiteral(2)],IntType,[IntLiteral(1),IntLiteral(2)]))", 41))

    def test_042(self):
        """
func votien(a  [2]int ) {
    votien([3] int {1,2,3})
}
        """
        input = Program([FuncDecl("votien", [ParamDecl("a", ArrayType([IntLiteral(2)], IntType()))], VoidType(), Block([FuncCall("votien", [ArrayLiteral([IntLiteral(3)], IntType(), [IntLiteral(1), IntLiteral(2), IntLiteral(3)])])]))])
        self.assertTrue(TestChecker.test(input, "Type Mismatch: FuncCall(votien,[ArrayLiteral([IntLiteral(3)],IntType,[IntLiteral(1),IntLiteral(2),IntLiteral(3)])])", 42))

    def test_043(self):
        """
var a [1 + 9] int;
var b [10] int = a;
        """
        input = Program([VarDecl("a", ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(9))], IntType()), None), VarDecl("b", ArrayType([IntLiteral(10)], IntType()), Id("a"))])
        self.assertTrue(TestChecker.test(input, "VOTIEN", 43))

    def test_044(self):
        """
const v = 3;
var c [3] int = [v * 1] int {1 , 2, 3};
        """
        input = Program([ConstDecl("v", None, IntLiteral(3)), VarDecl("c", ArrayType([IntLiteral(3)], IntType()), ArrayLiteral([BinaryOp("*", Id("v"), IntLiteral(1))], IntType(), [IntLiteral(1), IntLiteral(2), IntLiteral(3)]))])
        self.assertTrue(TestChecker.test(input, "VOTIEN", 44))

    def test_045(self):
        """
const v = 3;
const k = v + 1;
func foo(a [1 + 2] int) {
    foo([k - 1] int {1,2,3})
}
        """
        input = Program([ConstDecl("v", None, IntLiteral(3)), ConstDecl("k", None, BinaryOp("+", Id("v"), IntLiteral(1))), FuncDecl("foo", [ParamDecl("a", ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))], IntType()))], VoidType(), Block([FuncCall("foo", [ArrayLiteral([BinaryOp("-", Id("k"), IntLiteral(1))], IntType(), [IntLiteral(1), IntLiteral(2), IntLiteral(3)])])]))])
        self.assertTrue(TestChecker.test(input, "VOTIEN", 45))

    def test_046(self):
        """
type K struct {a int;}
func (k K) koo(a [1 + 2] int) {return;}
type H interface {koo(a [1 + 2] int);}

const c = 4;
func foo() {
    var k H;
    k.koo([c - 1] int {1,2,3})
} 
        """
        input = Program([StructType("K", [("a", IntType())], []), MethodDecl("k", Id("K"), FuncDecl("koo", [ParamDecl("a", ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))], IntType()))], VoidType(), Block([Return(None)]))), InterfaceType("H", [Prototype("koo", [ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))], IntType())], VoidType())]), ConstDecl("c", None, IntLiteral(4)), FuncDecl("foo", [], VoidType(), Block([VarDecl("k", Id("H"), None), MethCall(Id("k"), "koo", [ArrayLiteral([BinaryOp("-", Id("c"), IntLiteral(1))], IntType(), [IntLiteral(1), IntLiteral(2), IntLiteral(3)])])]))])
        self.assertTrue(TestChecker.test(input, "VOTIEN", 46))

    def test_047(self):
        """
type K struct {a int;}
func (k K) koo(a [1 + 2] int) [1 + 2] int {return [3*1] int {1,2,3};}
type H interface {koo(a [1 + 2] int) [1 + 2] int;}

const c = 4;
func foo() [1 + 2] int{
    return foo()
    var k K;
    return k.koo([c - 1] int {1,2,3})
    var h H;
    return h.koo([c - 1] int {1,2,3})
}
        """
        input = Program([StructType("K", [("a", IntType())], []), MethodDecl("k", Id("K"), FuncDecl("koo", [ParamDecl("a", ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))], IntType()))], ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))], IntType()), Block([Return(ArrayLiteral([BinaryOp("*", IntLiteral(3), IntLiteral(1))], IntType(), [IntLiteral(1), IntLiteral(2), IntLiteral(3)]))]))), InterfaceType("H", [Prototype("koo", [ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))], IntType())], ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))], IntType()))]), ConstDecl("c", None, IntLiteral(4)), FuncDecl("foo", [], ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))], IntType()), Block([Return(FuncCall("foo", [])), VarDecl("k", Id("K"), None), Return(MethCall(Id("k"), "koo", [ArrayLiteral([BinaryOp("-", Id("c"), IntLiteral(1))], IntType(), [IntLiteral(1), IntLiteral(2), IntLiteral(3)])])), VarDecl("h", Id("H"), None), Return(MethCall(Id("h"), "koo", [ArrayLiteral([BinaryOp("-", Id("c"), IntLiteral(1))], IntType(), [IntLiteral(1), IntLiteral(2), IntLiteral(3)])]))]))])
        self.assertTrue(TestChecker.test(input, "VOTIEN", 47))

    def test_048(self):
        """
type S1 struct {votien int;}
type S2 struct {votien int;}
type I1 interface {votien() S1;}
type I2 interface {votien() S2;}

func (s S1) votien() S1 {return s;}

var a S1;
var c I1 = a;
var d I2 = a;
        """
        input = Program([StructType("S1", [("votien", IntType())], []), StructType("S2", [("votien", IntType())], []), InterfaceType("I1", [Prototype("votien", [], Id("S1"))]), InterfaceType("I2", [Prototype("votien", [], Id("S2"))]), MethodDecl("s", Id("S1"), FuncDecl("votien", [], Id("S1"), Block([Return(Id("s"))]))), VarDecl("a", Id("S1"), None), VarDecl("c", Id("I1"), Id("a")), VarDecl("d", Id("I2"), Id("a"))])
        self.assertTrue(TestChecker.test(input, "Redeclared Method: votien", 48))

    def test_049(self):
        """
type S1 struct {votien int;}
type I1 interface {votien();}

func (s S1) votien() {return;}

func foo() S1 {
    var a S1;
    return a
}

func foo1() I1 {
    var a I1;
    return a
}

func foo2() S1 {
    var b I1;
    return b
}
        """
        input = Program([StructType("S1", [("votien", IntType())], []), InterfaceType("I1", [Prototype("votien", [], VoidType())]), MethodDecl("s", Id("S1"), FuncDecl("votien", [], VoidType(), Block([Return(None)]))), FuncDecl("foo", [], Id("S1"), Block([VarDecl("a", Id("S1"), None), Return(Id("a"))])), FuncDecl("foo1", [], Id("I1"), Block([VarDecl("a", Id("I1"), None), Return(Id("a"))])), FuncDecl("foo2", [], Id("S1"), Block([VarDecl("b", Id("I1"), None), Return(Id("b"))]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Method: votien", 49))

    def test_050(self):
        input = Program([VarDecl("a", Id("TIEN"), None), FuncDecl("foo", [], Id("TIEN"), Block([Return(Id("a")), Return(Id("TIEN"))])), StructType("TIEN", [("tien", IntType())], [])])
        self.assertTrue(TestChecker.test(input, "Undeclared Identifier: TIEN", 50))

    def test_051(self):
        """
type S1 struct {votien int;}
func (s S1) votien() int {
s.votien();
return 1;
}
        """
        input = Program([StructType("S1", [("votien", IntType())], []), MethodDecl("s", Id("S1"), FuncDecl("votien", [], IntType(), Block([MethCall(Id("s"), "votien", []), Return(IntLiteral(1))])))])
        self.assertTrue(TestChecker.test(input, "Redeclared Method: votien", 51))

    def test_052(self):
        """
func foo() {
    a := 1;
    var a = 1;
}
        """
        input = Program([FuncDecl("foo", [], VoidType(), Block([Assign(Id("a"), IntLiteral(1)), VarDecl("a", None, IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(input, """Redeclared Variable: a""", 52))

    def test_053(self):
        """
func Votien (b int) {
    for var a = 1; c < 1; a += c {
        const c = 2;
    }
}
        """
        input = Program([FuncDecl("Votien", [ParamDecl("b", IntType())], VoidType(), Block([ForStep(VarDecl("a", None, IntLiteral(1)), BinaryOp("<", Id("c"), IntLiteral(1)), Assign(Id("a"), BinaryOp("+", Id("a"), Id("c"))), Block([ConstDecl("c", None, IntLiteral(2))]))]))])
        self.assertTrue(TestChecker.test(input, """Undeclared Identifier: c""", 53))

    def test_054(self):
        """
var v TIEN;
func (v TIEN) foo (v int) int {
    return v;
}

type TIEN struct {
    Votien int;
}
        """
        input = Program([VarDecl("v", Id("TIEN"), None), MethodDecl("v", Id("TIEN"), FuncDecl("foo", [ParamDecl("v", IntType())], IntType(), Block([Return(Id("v"))]))), StructType("TIEN", [("Votien", IntType())], [])])
        self.assertTrue(TestChecker.test(input, "VOTIEN", 54))

    def test_055(self):
        """
const a = 2;
func foo () {
    const a = 1;
    for var a = 1; a < 1; b := 2 {
        const b = 1;
    }
}
        """
        input = Program([ConstDecl("a", None, IntLiteral(2)), FuncDecl("foo", [], VoidType(), Block([ConstDecl("a", None, IntLiteral(1)), ForStep(VarDecl("a", None, IntLiteral(1)), BinaryOp("<", Id("a"), IntLiteral(1)), Assign(Id("b"), IntLiteral(2)), Block([ConstDecl("b", None, IntLiteral(1))]))]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: b", 55))

    def test_056(self):
        """
var a int;
func (v TIEN) foo () int {
    return a;
    return v;
}
type TIEN struct {
    Votien int;
}
        """
        input = Program([VarDecl("a", IntType(), None), MethodDecl("v", Id("TIEN"), FuncDecl("foo", [], IntType(), Block([Return(Id("a")), Return(Id("v"))]))), StructType("TIEN", [("Votien", IntType())], [])])
        self.assertTrue(TestChecker.test(input, "Type Mismatch: Return(Id(v))", 56))

    def test_057(self):
        """
func (v TIEN) VO () {return ;}
func (v TIEN) Tien () {return ;}
type TIEN struct {
    Votien int;
    Tien int;
}
        """
        input = Program([MethodDecl("v", Id("TIEN"), FuncDecl("VO", [], VoidType(), Block([Return(None)]))), MethodDecl("v", Id("TIEN"), FuncDecl("Tien", [], VoidType(), Block([Return(None)]))), StructType("TIEN", [("Votien", IntType()), ("Tien", IntType())], [])])
        self.assertTrue(TestChecker.test(input, """Redeclared Method: Tien""", 57))

    def test_058(self):
        input = """
func foo() int {
    const foo = 1;
    return foo()
}
        """
        input = Program([FuncDecl("foo", [], IntType(), Block([ConstDecl("foo", None, IntLiteral(1)), Return(FuncCall("foo", []))]))])
        self.assertTrue(TestChecker.test(input, """Undeclared Function: foo""", 58))

    def test_059(self):
        """
var a = 1;
func foo() {
    a := 3;
    var a = 1.0
    for var a = 1; a > 1; a := 1 {
        return
    }
}
        """
        input = Program([VarDecl("a", None, IntLiteral(1)), FuncDecl("foo", [], VoidType(), Block([Assign(Id("a"), IntLiteral(3)), VarDecl("a", None, FloatLiteral(1.0)), ForStep(VarDecl("a", None, IntLiteral(1)), BinaryOp(">", Id("a"), IntLiteral(1)), Assign(Id("a"), IntLiteral(1)), Block([Return(None)]))]))])
        self.assertTrue(TestChecker.test(input, """VOTIEN""", 59))

    def test_060(self):
        """
func foo() {
    foo := 1;
    var foo = 1;
}
        """
        input = Program([FuncDecl("foo", [], VoidType(), Block([Assign(Id("foo"), IntLiteral(1)), VarDecl("foo", None, IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(input, """Redeclared Variable: foo""", 60))

    def test_061(self):
        """
func foo() {
    var a = foo
}
        """
        input = Program([FuncDecl("foo", [], VoidType(), Block([VarDecl("a", None, Id("foo"))]))])
        self.assertTrue(TestChecker.test(input, """Undeclared Identifier: foo""", 61))

    def test_062(self):
        """
var v TIEN;      
type TIEN struct {
    a int;
} 
type VO interface {
    fooA();
    fooB();
    fooC();
}

func (v TIEN) fooA() {return ;}
func (foo TIEN) fooB() {
    foo()
    return ;
}
func (v TIEN) fooC()  {return ;}

func foo() {
    var x VO = TIEN{a:1};  
}
        """
        input = Program([VarDecl("v", Id("TIEN"), None), StructType("TIEN", [("a", IntType())], []), InterfaceType("VO", [Prototype("fooA", [], VoidType()), Prototype("fooB", [], VoidType()), Prototype("fooC", [], VoidType())]), MethodDecl("v", Id("TIEN"), FuncDecl("fooA", [], VoidType(), Block([Return(None)]))), MethodDecl("foo", Id("TIEN"), FuncDecl("fooB", [], VoidType(), Block([FuncCall("foo", []), Return(None)]))), MethodDecl("v", Id("TIEN"), FuncDecl("fooC", [], VoidType(), Block([Return(None)]))), FuncDecl("foo", [], VoidType(), Block([VarDecl("x", Id("VO"), StructLiteral("TIEN", [("a", IntLiteral(1))]))]))])
        self.assertTrue(TestChecker.test(input, """Undeclared Function: foo""", 62))

    def test_063(self):
        """
func Votien () {
    var array = [2] int {1,2}
    var index int;
    var value float;
    for index, value := range array {
        return;
    }
}
        """
        input = Program([FuncDecl("Votien", [], VoidType(), Block([VarDecl("array", None, ArrayLiteral([IntLiteral(2)], IntType(), [IntLiteral(1), IntLiteral(2)])), VarDecl("index", IntType(), None), VarDecl("value", FloatType(), None), ForEach(Id("index"), Id("value"), Id("array"), Block([Return(None)]))]))])
        self.assertTrue(TestChecker.test(input, """Type Mismatch: ForEach(Id(index),Id(value),Id(array),Block([Return()]))""", 63))

    def test_064(self):
        """
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
        """
        input = Program([FuncDecl("foo", [], VoidType(), Block([VarDecl("arr", ArrayType([IntLiteral(2), IntLiteral(3)], IntType()), None), VarDecl("a", None, IntLiteral(1)), VarDecl("b", ArrayType([IntLiteral(3)], IntType()), None), ForEach(Id("a"), Id("b"), Id("arr"), Block([VarDecl("c", IntType(), Id("a")), VarDecl("d", ArrayType([IntLiteral(3)], IntType()), Id("b")), VarDecl("e", ArrayType([IntLiteral(2)], StringType()), Id("a"))]))]))])
        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl(e,ArrayType(StringType,[IntLiteral(2)]),Id(a))""", 64))

#     def test_301(self):
#         input = Program([
#             VarDecl("x", IntType(), None),
#             VarDecl("x", IntType(), None)
#         ])
#         expect = "Redeclared Variable: x"
#         self.assertTrue(TestChecker.test(input, expect, 301))

#     def test_302(self):
#         input = Program([
#             FuncDecl("foo", [], VoidType(), Block([])),
#             FuncDecl("foo", [], VoidType(), Block([]))
#         ])
#         expect = "Redeclared Function: foo"
#         self.assertTrue(TestChecker.test(input, expect, 302))

#     def test_303(self):
#         input = Program([
#             VarDecl("x", IntType(), Id("y"))
#         ])
#         expect = "Undeclared Identifier: y"
#         self.assertTrue(TestChecker.test(input, expect, 303))

#     def test_304(self):
#         input = Program([
#             VarDecl("x", IntType(), FloatLiteral(1.2))
#         ])
#         expect = "Type Mismatch: VarDecl(x,IntType,FloatLiteral(1.2))"
#         self.assertTrue(TestChecker.test(input, expect, 304))

#     def test_305(self):
#         input = Program([
#             StructType("Person", [("name", StringType()),
#                        ("name", IntType())], [])
#         ])
#         expect = "Redeclared Field: name"
#         self.assertTrue(TestChecker.test(input, expect, 305))

#     def test_306(self):
#         """Struct decl after method still ok"""
#         input = Program([
#             MethodDecl("p", Id("Person"), FuncDecl(
#                 "getName", [], StringType(), Block([]))),
#             MethodDecl("p", Id("Person"), FuncDecl(
#                 "getName", [], StringType(), Block([]))),
#             StructType("Person", [], [])
#         ])
#         expect = "Redeclared Method: getName"
#         self.assertTrue(TestChecker.test(input, expect, 306))

#     def test_307(self):
#         """"Focus on this case"""
#         input = Program([
#             MethodDecl("p", Id("Person"), FuncDecl(
#                 "getName", [], StringType(), Block([]))),
#             StructType("Person", [("getName", StringType())], []),
#         ])
#         expect = "Redeclared Method: getName"
#         self.assertTrue(TestChecker.test(input, expect, 307))

#     def test_308(self):
#         input = Program([
#             MethodDecl("p", Id("UnknownStruct"), FuncDecl(
#                 "foo", [], VoidType(), Block([])))
#         ])
#         expect = "Undeclared Type: UnknownStruct"
#         self.assertTrue(TestChecker.test(input, expect, 308))

#     def test_309(self):
#         input = Program([
#             InterfaceType("Animal", [
#                 Prototype("speak", [], StringType()),
#                 Prototype("speak", [], StringType())
#             ])
#         ])
#         expect = "Redeclared Prototype: speak"
#         self.assertTrue(TestChecker.test(input, expect, 309))

#     def test_310(self):
#         input = Program([
#             MethodDecl("p", Id("Person"), FuncDecl(
#                 "getName", [], StringType(), Block([]))),
#             StructType("Person", [("name", StringType())], [])
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 310))

#     def test_311(self):
#         input = Program([
#             StructType("Person", [("name", StringType())], []),
#             MethodDecl("p", Id("Person"), FuncDecl(
#                 "name", [], StringType(), Block([])))
#         ])
#         expect = "Redeclared Method: name"
#         self.assertTrue(TestChecker.test(input, expect, 311))

#     def test_312(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          FuncCall("print", [Id("x")])
#                      ])
#                      )
#         ])
#         expect = "Undeclared Function: print"
#         self.assertTrue(TestChecker.test(input, expect, 312))

#     def test_313(self):
#         """Hoisting works - function can invoke before declaration"""
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          FuncCall("print", [Id("x")])
#                      ])
#                      ),
#             FuncDecl("print", [ParamDecl("msg", StringType())],
#                      VoidType(), Block([]))
#         ])
#         expect = "Undeclared Identifier: x"
#         self.assertTrue(TestChecker.test(input, expect, 313))

#     def test_314(self):
#         input = Program([
#             StructType("Person", [("name", StringType())], []),
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("p", Id("Person"), None),
#                          MethCall(Id("p"), "unknownMethod", [])
#                      ])
#                      ),
#             MethodDecl("p", Id("Person"), FuncDecl(
#                 "getName", [], StringType(), Block([]))),
#         ])
#         expect = "Undeclared Method: unknownMethod"
#         self.assertTrue(TestChecker.test(input, expect, 314))

#     def test_315(self):
#         """Hoisting works - method can invoke before declaration"""
#         input = Program([
#             StructType("Person", [("name", StringType())], []),
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("p", Id("Person"), None),
#                          MethCall(Id("p"), "getName", [])
#                      ])
#                      ),
#             MethodDecl("p", Id("Person"), FuncDecl(
#                 "getName", [], StringType(), Block([]))),
#         ])
#         expect = "Type Mismatch: MethodCall(Id(p),getName,[])"
#         self.assertTrue(TestChecker.test(input, expect, 315))

#     def test_316(self):
#         """Hoisting works - can use struct/field before declaration"""
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("p", Id("Person"), None),
#                          FieldAccess(Id("p"), "name")
#                      ])
#                      ),
#             StructType("Person", [("name", StringType())], []),
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 316))

#     def test_317(self):
#         input = Program([
#             StructType("Person", [("name", StringType())], []),
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("p", Id("Person"), None),
#                          FieldAccess(Id("p"), "age")
#                      ])
#                      ),
#         ])
#         expect = "Undeclared Field: age"
#         self.assertTrue(TestChecker.test(input, expect, 317))

#     def test_318(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          FuncCall("foo", [])
#                      ])
#                      ),
#             FuncDecl("foo", [], IntType(), Block([])),
#         ])
#         expect = "Type Mismatch: FuncCall(foo,[])"
#         self.assertTrue(TestChecker.test(input, expect, 318))

#     def test_319(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("x", IntType(), None),
#                          Assign(Id("x"), IntLiteral(5))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 319))

#     def test_320(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("x", IntType(), None),
#                          Assign(Id("x"), FloatLiteral(5.0))
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: Assign(Id(x),FloatLiteral(5.0))"
#         self.assertTrue(TestChecker.test(input, expect, 320))

#     def test_321(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("x", IntType(), None),
#                          Assign(Id("x"), BooleanLiteral(True))
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: Assign(Id(x),BooleanLiteral(true))"
#         self.assertTrue(TestChecker.test(input, expect, 321))

#     def test_322(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("x", FloatType(), None),
#                          Assign(Id("x"), IntLiteral(2))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 322))

#     def test_323(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("x", ArrayType(
#                              [IntLiteral(3)], IntType()), None),
#                          VarDecl("y", ArrayType(
#                              [IntLiteral(3)], IntType()), None),
#                          Assign(Id("x"), Id("y"))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 323))

#     def test_324(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("x", ArrayType(
#                              [IntLiteral(3), IntLiteral(3)], IntType()), None),
#                          VarDecl("y", ArrayType(
#                              [IntLiteral(3)], IntType()), None),
#                          Assign(Id("x"), Id("y"))
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: Assign(Id(x),Id(y))"
#         self.assertTrue(TestChecker.test(input, expect, 324))

#     def test_325(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("x", ArrayType(
#                              [IntLiteral(3)], IntType()), None),
#                          Assign(Id("x"), ArrayLiteral([IntLiteral(3)], IntType(), [
#                            IntLiteral(1), IntLiteral(2), IntLiteral(3)]))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 325))

#     def test_326(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("x", ArrayType(
#                              [IntLiteral(3)], IntType()), None),
#                          Assign(Id("x"), ArrayLiteral(
#                              [IntLiteral(2)], IntType(), [IntLiteral(1), IntLiteral(2)]))
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: Assign(Id(x),ArrayLiteral([IntLiteral(2)],IntType,[IntLiteral(1),IntLiteral(2)]))"
#         self.assertTrue(TestChecker.test(input, expect, 326))

#     def test_327(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("x", ArrayType(
#                              [IntLiteral(2), IntLiteral(3)], IntType()), None),
#                          Assign(Id("x"), ArrayLiteral(
#                              [IntLiteral(2), IntLiteral(3)], IntType(),
#                              [[IntLiteral(1), IntLiteral(2), IntLiteral(3)],
#                               [IntLiteral(4), IntLiteral(5), IntLiteral(6)]]
#                          ))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 327))

#     def test_328(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("x", ArrayType(
#                              [IntLiteral(3)], IntType()), None),
#                          Assign(Id("x"), ArrayLiteral(
#                              [IntLiteral(4)], IntType(),
#                              [IntLiteral(1), IntLiteral(
#                                  2), IntLiteral(3), IntLiteral(4)]
#                          ))
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: Assign(Id(x),ArrayLiteral([IntLiteral(4)],IntType,[IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(4)]))"
#         self.assertTrue(TestChecker.test(input, expect, 328))

#     def test_329(self):
#         input = Program([
#             InterfaceType("Animal", [Prototype("speak", [], StringType())]),
#             StructType("Dog", [], [
#                 MethodDecl("p", Id("Animal"), FuncDecl(
#                     "speak", [], StringType(), Block([])))
#             ]),
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("a", Id("Animal"), None),
#                          VarDecl("d", Id("Dog"), None),
#                          Assign(Id("a"), Id("d"))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 329))

#     def test_330(self):
#         input = Program([
#             InterfaceType("Animal", [Prototype("speak", [], StringType())]),
#             StructType("Cat", [], [
#                 MethodDecl("p", Id("Animal"), FuncDecl(
#                     "meow", [], StringType(), Block([])))  # Không có `speak`
#             ]),
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("a", Id("Animal"), None),
#                          VarDecl("c", Id("Cat"), None),
#                          Assign(Id("a"), Id("c"))
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: Assign(Id(a),Id(c))"
#         self.assertTrue(TestChecker.test(input, expect, 330))

#     def test_331(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          Assign(Id("x"), IntLiteral(10)),
#                          Assign(Id("x"), FloatLiteral(2.5)),
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: Assign(Id(x),FloatLiteral(2.5))"
#         self.assertTrue(TestChecker.test(input, expect, 331))

#     def test_332(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          Assign(Id("x"), IntLiteral(10))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 332))

#     def test_333(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          Assign(Id("x"), BinaryOp(
#                              "+", IntLiteral(10), IntLiteral(5))),
#                          Assign(Id("y"), BinaryOp(
#                              "*", FloatLiteral(2.5), IntLiteral(2)))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 333))

#     def test_334(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          Assign(Id("x"), BinaryOp(
#                              "+", BooleanLiteral(True), IntLiteral(5)))
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: BinaryOp(BooleanLiteral(true),+,IntLiteral(5))"
#         self.assertTrue(TestChecker.test(input, expect, 334))

#     def test_335(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          Assign(Id("x"), BinaryOp(
#                              ">", IntLiteral(10), FloatLiteral(5.5))),
#                          Assign(Id("y"), BinaryOp(
#                              "==", FloatLiteral(3.3), FloatLiteral(3.3)))
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: BinaryOp(IntLiteral(10),>,FloatLiteral(5.5))"
#         # Confused: expect = "Type Mismatch: BinaryOp(IntLiteral(10),>,FloatLiteral(5.5))"
#         self.assertTrue(TestChecker.test(input, expect, 335))

#     def test_336(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          Assign(Id("x"), BinaryOp(
#                              "&&", IntLiteral(1), BooleanLiteral(False)))
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: BinaryOp(IntLiteral(1),&&,BooleanLiteral(false))"
#         self.assertTrue(TestChecker.test(input, expect, 336))

#     def test_337(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          Assign(Id("x"), UnaryOp("-", IntLiteral(10))),
#                          Assign(Id("y"), UnaryOp("-", FloatLiteral(2.5)))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 337))

#     def test_338(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          Assign(Id("x"), UnaryOp("-", BooleanLiteral(True)))
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: UnaryOp(-,BooleanLiteral(true))"
#         self.assertTrue(TestChecker.test(input, expect, 338))

#     def test_339(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          Assign(Id("x"), UnaryOp("!", BooleanLiteral(False))),
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 339))

#     def test_340(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          Assign(Id("x"), UnaryOp("!", IntLiteral(10)))
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: UnaryOp(!,IntLiteral(10))"
#         self.assertTrue(TestChecker.test(input, expect, 340))

#     def test_341(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          If(BooleanLiteral(True), Block(
#                              [Assign(Id("x"), IntLiteral(10))]), None),
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 341))

#     def test_342(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          If(IntLiteral(1), Block(
#                              [Assign(Id("x"), IntLiteral(10))]), None),
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: If(IntLiteral(1),Block([Assign(Id(x),IntLiteral(10))]))"
#         self.assertTrue(TestChecker.test(input, expect, 342))

#     def test_343(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          If(BinaryOp("&&", BooleanLiteral(True), BooleanLiteral(False)),
#                             Block([Assign(Id("y"), FloatLiteral(2.5))]),
#                             None
#                             ),
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 343))

#     def test_344(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          If(BinaryOp("+", IntLiteral(5), IntLiteral(3)),
#                             Block([Assign(Id("z"), BooleanLiteral(True))]),
#                             None
#                             ),
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: If(BinaryOp(IntLiteral(5),+,IntLiteral(3)),Block([Assign(Id(z),BooleanLiteral(true))]))"
#         self.assertTrue(TestChecker.test(input, expect, 344))

#     def test_345(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("x", IntType(), None),
#                          VarDecl("y", FloatType(), None),
#                          VarDecl("z", BoolType(), BooleanLiteral(True)),

#                          If(BinaryOp("==", Id("x"), IntLiteral(0)), Block([]), None),
#                          If(BinaryOp("!=", Id("y"), FloatLiteral(1.5)),
#                             Block([]), Block([])),
#                          If(BinaryOp("<", Id("x"), Id("y")), Block([]), None),

#                          If(BinaryOp("&&", Id("z"), BooleanLiteral(True)),
#                             Block([]), None),
#                          If(BinaryOp("||", Id("z"), BooleanLiteral(False)),
#                             Block([]), Block([])),
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: BinaryOp(Id(x),<,Id(y))"
#         # Confused: expect ="Type Mismatch: BinaryOp(Id(x),<,Id(y))"
#         self.assertTrue(TestChecker.test(input, expect, 345))

#     def test_346(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("a", IntType(), None),
#                          VarDecl("b", FloatType(), None),
#                          VarDecl("c", BoolType(), None),
#                          If(UnaryOp("!", Id("c")), Block([]), None),
#                          If(UnaryOp("-", Id("a")), Block([]), None),
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: If(UnaryOp(-,Id(a)),Block([]))"
#         self.assertTrue(TestChecker.test(input, expect, 346))

#     def test_347(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("x", IntType(), None),
#                          ForBasic(Id("x"), Block([]))
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: For(Id(x),Block([]))"
#         self.assertTrue(TestChecker.test(input, expect, 347))

#     def test_348(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("x", BoolType(), None),
#                          ForBasic(Id("x"), Block([]))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 348))

#     def test_349(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("i", IntType(), None),
#                          ForStep(
#                              Assign(Id("i"), IntLiteral(0)),
#                              BinaryOp(">", Id("i"), IntLiteral(10)),
#                              Assign(Id("i"), BinaryOp(
#                                  "+", Id("i"), IntLiteral(1))), Block([])
#                          )
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 349))

#     def test_350(self):
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          ForStep(
#                              Assign(Id("i"), IntLiteral(0)),
#                              BinaryOp("+", Id("i"), IntLiteral(10)),
#                              Assign(Id("i"), BinaryOp(
#                                  "+", Id("i"), IntLiteral(1))),
#                              Block([])
#                          )
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: For(Assign(Id(i),IntLiteral(0)),BinaryOp(Id(i),+,IntLiteral(10)),Assign(Id(i),BinaryOp(Id(i),+,IntLiteral(1))),Block([]))"
#         self.assertTrue(TestChecker.test(input, expect, 350))

#     def test_351(self):
#         """ForEach with valid array iteration"""
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("arr", ArrayType([IntLiteral(3)], IntType()),
#                                  ArrayLiteral([IntLiteral(3)], IntType(),
#                                               [IntLiteral(10), IntLiteral(20), IntLiteral(30)])),
#                          ForEach(Id("index"), Id("value"), Id("arr"),
#                                  Block([
#                                      Assign(Id("sum"), BinaryOp(
#                                          "+", Id("index"), Id("value")))
#                                  ])
#                                  )
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 351))

#     def test_352(self):
#         """ForEach with incorrect collection type (non-array)"""
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("x", IntType(), IntLiteral(100)),
#                          ForEach(Id("index"), Id("value"), Id("x"), Block([]))
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: ForEach(Id(index),Id(value),Id(x),Block([]))"
#         self.assertTrue(TestChecker.test(input, expect, 352))

#     def test_353(self):
#         """ForEach with mismatched value type"""
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("arr", ArrayType([IntLiteral(3)], FloatType()),
#                                  ArrayLiteral([IntLiteral(3)], FloatType(),
#                                               [FloatLiteral(1.1), FloatLiteral(2.2), FloatLiteral(3.3)])),
#                          VarDecl("sum", IntType(), IntLiteral(0)),
#                          ForEach(Id("index"), Id("sum"), Id("arr"), Block([]))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 353))

#     def test_354(self):
#         """ForEach with blank identifier as index"""
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("arr", ArrayType([IntLiteral(3)], IntType()),
#                                  ArrayLiteral([IntLiteral(3)], IntType(),
#                                               [IntLiteral(1), IntLiteral(2), IntLiteral(3)])),
#                          ForEach(Id("_"), Id("value"), Id("arr"),
#                                  Block([
#                                      Assign(Id("sum"), BinaryOp(
#                                          "+", FloatLiteral(2.5), Id("value")))
#                                  ])
#                                  )
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 354))

#     def test_355(self):
#         """Return type mismatch: function declared with VoidType but returns IntType"""
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          Return(IntLiteral(5))
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: Return(IntLiteral(5))"
#         self.assertTrue(TestChecker.test(input, expect, 355))

#     def test_356(self):
#         """Return type mismatch: function declared with IntType but returns VoidType"""
#         input = Program([
#             FuncDecl("main", [], IntType(),
#                      Block([
#                          Return(None)
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: Return()"
#         self.assertTrue(TestChecker.test(input, expect, 356))

#     def test_357(self):
#         """Return type mismatch: function declared with FloatType but returns IntType"""
#         input = Program([
#             FuncDecl("main", [], FloatType(),
#                      Block([
#                          Return(IntLiteral(10))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 357))

#     def test_358(self):
#         """Valid return: function declared with IntType and correctly returns IntLiteral"""
#         input = Program([
#             FuncDecl("main", [], IntType(),
#                      Block([
#                          Return(IntLiteral(42))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 358))

#     def test_359(self):
#         """Valid return: function declared with VoidType and correctly has no return statement"""
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("x", IntType(), IntLiteral(10))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 359))

#     def test_360(self):
#         """Valid array indexing with integer indices"""
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("arr", ArrayType([IntLiteral(3)], IntType()),
#                                  ArrayLiteral([IntLiteral(3)], IntType(),
#                                               [IntLiteral(1), IntLiteral(2), IntLiteral(3)])),
#                          Assign(Id("x"), ArrayCell(Id("arr"), [IntLiteral(2)]))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 360))

#     def test_361(self):
#         """Array indexing with non-integer index (float)"""
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("arr", ArrayType([IntLiteral(5)], IntType()),
#                                  ArrayLiteral([IntLiteral(5)], IntType(),
#                                               [IntLiteral(i) for i in range(5)])),
#                          Assign(Id("x"), ArrayCell(
#                              Id("arr"), [FloatLiteral(1.5)]))
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: ArrayCell(Id(arr),[FloatLiteral(1.5)])"
#         self.assertTrue(TestChecker.test(input, expect, 361))

#     def test_362(self):
#         """Accessing a non-array variable as if it were an array"""
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("x", IntType(), IntLiteral(10)),
#                          Assign(Id("y"), ArrayCell(Id("x"), [IntLiteral(0)]))
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: ArrayCell(Id(x),[IntLiteral(0)])"
#         self.assertTrue(TestChecker.test(input, expect, 362))

#     def test_363(self):
#         """Valid multi-dimensional array access"""
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("matrix", ArrayType([IntLiteral(3), IntLiteral(3)], IntType()),
#                                  ArrayLiteral([IntLiteral(3), IntLiteral(3)], IntType(),
#                                               [[IntLiteral(i * 3 + j) for j in range(3)] for i in range(3)])),
#                          Assign(Id("x"), ArrayCell(Id("matrix"),
#                            [IntLiteral(1), IntLiteral(2)]))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 363))

#     def test_364(self):
#         """Valid multi-dimensional array access"""
#         input = Program([
#             FuncDecl("main", [], VoidType(), Block([
#                 Assign(Id("matrix"), ArrayLiteral([IntLiteral(2), IntLiteral(3)], IntType(),
#                                                   [[IntLiteral(1), IntLiteral(2), IntLiteral(3)], [IntLiteral(4), IntLiteral(5), IntLiteral(6)]])),
#                 Assign(Id("x"),
#                        ArrayCell(Id("matrix"), [IntLiteral(1), IntLiteral(2), IntLiteral(1)]))
#             ]))
#         ])
#         expect = "Type Mismatch: ArrayCell(Id(matrix),[IntLiteral(1),IntLiteral(2),IntLiteral(1)])"
#         self.assertTrue(TestChecker.test(input, expect, 364))

#     def test_365(self):
#         """Valid field access for a struct"""
#         input = Program([
#             StructType("Person", [("name", StringType()),
#                        ("age", IntType())], []),
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("person", Id("Person"), None),
#                          Assign(Id("name"), FieldAccess(Id("person"), "name"))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 365))

#     def test_366(self):
#         """Valid field access for struct with different field types"""
#         input = Program([
#             StructType("Person", [("name", StringType()),
#                        ("age", IntType())], []),
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("person", Id("Person"), None),
#                          Assign(Id("age"), FieldAccess(Id("person"), "age"))
#                      ])
#                      )
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 366))

#     def test_367(self):
#         """Accessing field in struct that is not declared"""
#         input = Program([
#             StructType("Person", [("name", StringType())], []),
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("person", Id("Person"), None),
#                          Assign(Id("age"), FieldAccess(Id("person"), "age"))
#                      ])
#                      )
#         ])
#         expect = "Undeclared Field: age"
#         self.assertTrue(TestChecker.test(input, expect, 367))

#     def test_368(self):
#         """Accessing field of a non-struct type"""
#         input = Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("x", IntType(), IntLiteral(5)),
#                          Assign(Id("y"), FieldAccess(Id("x"), "value"))
#                      ])
#                      )
#         ])
#         expect = "Type Mismatch: FieldAccess(Id(x),value)"
#         self.assertTrue(TestChecker.test(input, expect, 368))

#     def test_369(self):
#         input = Program([
#             StructType("Person", [("name", StringType())], []),
#             MethodDecl("p", Id("Person"), FuncDecl(
#                 "sayHello", [], VoidType(), Block([]))),
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("p", Id("Person"), None),
#                          MethCall(Id("p"), "sayHello", [])
#                      ])
#                      ),
#         ])
#         expect = "VOTIEN"
#         self.assertTrue(TestChecker.test(input, expect, 369))

#     def test_370(self):
#         input = Program([
#             StructType("Person", [("name", StringType())], []),
#             MethodDecl("p", Id("Person"), FuncDecl(
#                 "getName", [], StringType(), Block([]))),
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("p", Id("Person"), None),
#                          MethCall(Id("p"), "getName", [])
#                      ])
#                      ),
#         ])
#         expect = "Type Mismatch: MethodCall(Id(p),getName,[])"
#         self.assertTrue(TestChecker.test(input, expect, 370))

#     # def test_373(self):
#     #     input = Program([
#     #         StructType("Person", [("name", StringType())], []),
#     #         MethodDecl("p", Id("Person"), FuncDecl(
#     #             "getName", [], VoidType(), Block([]))),
#     #         FuncDecl("main", [], IntType(),
#     #                  Block([
#     #                      VarDecl("p", Id("Person"), None),
#     #                      Assign(Id("x"), BinaryOp("+", MethCall(Id("p"),
#     #                        "getName", []), MethCall(Id("p"), "getName", [])))
#     #                  ])
#     #                  ),
#     #     ])
#     #     expect = "Type Mismatch: MethodCall(Id(p),getName,[])"
#     #     self.assertTrue(TestChecker.test(input, expect, 373))

# #     def test_374(self):
# #         input = Program([
# #             FuncDecl("getPi", [], FloatType(), Block([])),
# #             FuncDecl("main", [], IntType(),
# #                      Block([
# #                          Assign(Id("x"), BinaryOp(
# #                              "+", FuncCall("getPi", []), FuncCall("getPi", [])))
# #                      ])
# #                      ),
# #         ])
# #         expect = ""
# #         self.assertTrue(TestChecker.test(input, expect, 374))

# #     def test_375(self):
# #         input = Program([
# #             StructType("Person", [("name", StringType())], []),
# #             MethodDecl("p", Id("Person"), FuncDecl(
# #                 "getPi", [], FloatType(), Block([]))),
# #             FuncDecl("main", [], IntType(),
# #                      Block([
# #                          VarDecl("p", Id("Person"), None),
# #                          VarDecl("y", FloatType(), FloatLiteral(2.5)),
# #                          Assign(Id("x"), BinaryOp("+", Id("y"),
# #                            MethCall(Id("p"), "getPi", [])))
# #                      ])
# #                      ),
# #         ])
# #         expect = ""
# #         self.assertTrue(TestChecker.test(input, expect, 375))

#     def test_376(self):
#         input = Program([
#             FuncDecl("log", [], VoidType(), Block([])),
#             FuncDecl("main", [], IntType(),
#                      Block([
#                          Assign(Id("x"), UnaryOp("-", FuncCall("log", [])))
#                      ])
#                      ),
#         ])
#         expect = "Type Mismatch: FuncCall(log,[])"
#         self.assertTrue(TestChecker.test(input, expect, 376))

#     def test_377(self):
#         input = Program([
#             FuncDecl("add", [ParamDecl("a", IntType()), ParamDecl("b", IntType())], IntType(),
#                      Block([Return(BinaryOp("+", Id("a"), Id("b")))])
#                      ),
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          Assign(Id("x"), FuncCall(
#                              "add", [IntLiteral(3), IntLiteral(5)]))
#                      ])
#                      ),
#         ])
#         expect = ""
#         self.assertTrue(TestChecker.test(input, expect, 377))

#     def test_378(self):
#         input = Program([
#             FuncDecl("add", [ParamDecl("a", IntType()), ParamDecl("b", IntType())], IntType(),
#                      Block([Return(BinaryOp("+", Id("a"), Id("b")))])
#                      ),
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          Assign(Id("x"), FuncCall(
#                              "add", [IntLiteral(3), FloatLiteral(5.0)]))
#                      ])
#                      ),
#         ])
#         expect = "Type Mismatch: FuncCall(add,[IntLiteral(3),FloatLiteral(5.0)])"
#         self.assertTrue(TestChecker.test(input, expect, 378))

#     def test_379(self):
#         input = Program([
#             StructType("Person", [("name", StringType())], []),
#             MethodDecl("p", Id("Person"), FuncDecl(
#                 "getName", [], StringType(), Block([Return(FieldAccess(Id("p"), "name"))]))),
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("p", Id("Person"), None),
#                          Assign(Id("x"), MethCall(
#                              Id("p"), "getName", [IntLiteral(3)]))
#                      ])
#                      ),
#         ])
#         expect = "Type Mismatch: MethodCall(Id(p),getName,[IntLiteral(3)])"
#         self.assertTrue(TestChecker.test(input, expect, 379))

#     # def test_380(self):
#     #     input = Program([
#     #         StructType("Person", [("name", StringType())], []),
#     #         MethodDecl("p", Id("Person"), FuncDecl(
#     #             "getName", [ParamDecl("x", FloatType())], StringType(), Block([Return(FieldAccess(Id("p"), "name"))]))),
#     #         FuncDecl("main", [], VoidType(),
#     #                  Block([
#     #                      VarDecl("p", Id("Person"), None),
#     #                      Assign(Id("x"), MethCall(
#     #                          Id("p"), "getName", [IntLiteral(3)]))
#     #                  ])
#     #                  ),
#     #     ])
#     #     expect = "Type Mismatch: MethodCall(Id(p),getName,[IntLiteral(3)])"
#     #     self.assertTrue(TestChecker.test(input, expect, 380))

#     def test_381(self):
#         input = Program([
#             StructType("Person", [("name", StringType())], []),
#             MethodDecl("p", Id("Person"), FuncDecl(
#                 "getName", [ParamDecl("x", FloatType()), ParamDecl("y", IntType())], StringType(), Block([Return(FieldAccess(Id("p"), "name"))]))),
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("p", Id("Person"), None),
#                          Assign(Id("x"), MethCall(
#                              Id("p"), "getName", [FloatLiteral(3)]))
#                      ])
#                      ),
#         ])
#         expect = "Type Mismatch: MethodCall(Id(p),getName,[FloatLiteral(3)])"
#         self.assertTrue(TestChecker.test(input, expect, 381))

#     def test_382(self):
#         input = Program([
#             StructType("Person", [("name", StringType())], []),
#             MethodDecl("p", Id("Person"), FuncDecl(
#                 "getName", [ParamDecl("x", FloatType()), ParamDecl("y", IntType())], StringType(), Block([Return(FieldAccess(Id("p"), "name"))]))),
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("p", Id("Person"), None),
#                          Assign(Id("x"), MethCall(Id("p"), "getName",
#                                                   [FloatLiteral(3), IntLiteral(10)]))
#                      ])
#                      ),
#         ])
#         expect = ""
#         self.assertTrue(TestChecker.test(input, expect, 382))

#     def test_383(self):
#         input = Program([
#             FuncDecl("log", [], VoidType(), Block([Return(IntLiteral(5))])),
#             FuncDecl("main", [], IntType(),
#                      Block([])
#                      ),
#         ])
#         expect = "Type Mismatch: Return(IntLiteral(5))"
#         self.assertTrue(TestChecker.test(input, expect, 383))

#     def test_384(self):
#         input = Program([
#             FuncDecl("log", [], VoidType(), Block([Return(None)])),
#             FuncDecl("main", [], IntType(),
#                      Block([])
#                      ),
#         ])
#         expect = ""
#         self.assertTrue(TestChecker.test(input, expect, 384))

#     # def test_385(self):
#     #     input = Program([
#     #         FuncDecl("main", [], VoidType(),
#     #                  Block([
#     #                      VarDecl("p", None,
#     #                              StructLiteral("Person", [
#     #                                  ("name", StringLiteral("\"John\"")),
#     #                                  ("age", IntLiteral(25))
#     #                              ])
#     #                              )
#     #                  ])
#     #                  )
#     #     ])
#     #     expect = "Undeclared Type: Person"
#     #     self.assertTrue(TestChecker.test(input, expect, 385))

# #     def test_386(self):
# #         input = Program([
# #             StructType("Person", [
# #                 ("name", StringType()),
# #                 ("age", IntType())
# #             ], []),
# #             FuncDecl("main", [], VoidType(),
# #                      Block([
# #                          VarDecl("p", None,
# #                                  StructLiteral("Person", [
# #                                      ("name", StringLiteral("\"John\"")),
# #                                      ("name", StringLiteral("\"Doe\""))
# #                                  ])
# #                                  )
# #                      ])
# #                      )
# #         ])
# #         expect = "Type Mismatch: StructLiteral(Person,[(name,StringLiteral(\"John\")),(name,StringLiteral(\"Doe\"))])"
# #         self.assertTrue(TestChecker.test(input, expect, 386))

# #     def test_387(self):
# #         input = Program([
# #             StructType("Person", [
# #                 ("name", StringType()),
# #                 ("age", IntType())
# #             ], []),
# #             FuncDecl("main", [], VoidType(),
# #                      Block([
# #                          VarDecl("p", None,
# #                                  StructLiteral("Person", [
# #                                      ("name", StringLiteral("\"John\""))
# #                                  ])
# #                                  )
# #                      ])
# #                      )
# #         ])
# #         expect = "Type Mismatch: StructLiteral(Person,[(name,StringLiteral(\"John\"))])"
# #         self.assertTrue(TestChecker.test(input, expect, 387))

# #     def test_388(self):
# #         input = Program([
# #             StructType("Person", [
# #                 ("name", StringType()),
# #                 ("age", IntType())
# #             ], []),
# #             FuncDecl("main", [], VoidType(),
# #                      Block([
# #                          VarDecl("p", None,
# #                                  StructLiteral("Person", [
# #                                      ("name", IntLiteral(123)),
# #                                      ("age", IntLiteral(25))
# #                                  ])
# #                                  )
# #                      ])
# #                      )
# #         ])
# #         expect = "Type Mismatch: StructLiteral(Person,[(name,IntLiteral(123)),(age,IntLiteral(25))])"
# #         self.assertTrue(TestChecker.test(input, expect, 388))

#     def test_389(self):
#         input = Program([
#             StructType("Person", [
#                 ("name", StringType()),
#                 ("age", IntType())
#             ], []),
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("p", None,
#                                  StructLiteral("Person", [
#                                      ("name", StringLiteral("\"John\"")),
#                                      ("age", IntLiteral(25))
#                                  ])
#                                  )
#                      ])
#                      )
#         ])
#         expect = ""
#         self.assertTrue(TestChecker.test(input, expect, 389))

#     def test_390(self):
#         input = Program([
#             StructType("Person", [
#                 ("name", StringType()),
#                 ("age", IntType())
#             ], []),
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("p", None,
#                                  StructLiteral("Person", [
#                                      ("name", StringLiteral("\"Alice\"")),
#                                      ("age", IntLiteral(30))
#                                  ])
#                                  ),
#                          Block([
#                              VarDecl("p", None,
#                                      StructLiteral("Person", [
#                                          ("name", StringLiteral("\"Bob\"")),
#                                          ("age", IntLiteral(28))
#                                      ])
#                                      ),
#                              Block([
#                                  VarDecl("p", None,
#                                          StructLiteral("Person", [
#                                              ("name", StringLiteral(
#                                                  "\"Charlie\"")),
#                                              ("age", IntLiteral(22))
#                                          ])
#                                          )
#                              ])
#                          ])
#                      ])
#                      )
#         ])
#         expect = ""
#         self.assertTrue(TestChecker.test(input, expect, 390))
