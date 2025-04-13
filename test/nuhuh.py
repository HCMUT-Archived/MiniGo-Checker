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
