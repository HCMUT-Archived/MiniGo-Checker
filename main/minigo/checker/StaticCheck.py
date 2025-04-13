# 2210736

"""
 * @author nhphung
"""
from AST import *
from Visitor import *
from Utils import Utils
import StaticError as SErr
from functools import reduce
from typing import Dict, Tuple


class MType:
    def __init__(self, partype, rettype):
        self.partype = partype
        self.rettype = rettype

    def __str__(self):
        return "MType([" + ",".join(str(x) for x in self.partype) + "]," + str(self.rettype) + ")"


class Symbol:
    def __init__(self, name: str, mtype, value=None):
        self.name = name
        self.mtype = mtype
        self.value = value

    def __str__(self):
        return "Symbol(" + str(self.name) + "," + str(self.mtype) + ("" if self.value is None else "," + str(self.value)) + ")"

    # Compare symbols using == not is
    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def getName(self):
        if '.' in self.name:
            return self.name.split('.')[-1]
        return self.name


# region Env
# CUSTOM ENV MANAGER
class EnvManager:

    def __init__(self):
        # for type/function/method
        # HAVE TO DO THIS TO CHECK FOR FUNC/METH CALL TOO
        self.preCheck: Dict[Symbol, Tuple[Symbol, bool]] = {}
        self.scopeStack: List[List[Symbol]] = []
        # built-in functions is set in global scope
        self.scopeStack.append([
            Symbol("getInt", MType([], IntType())),
            Symbol("putInt", MType([IntType()], VoidType())),
            Symbol("putIntLn", MType([IntType()], VoidType())),
            Symbol('getFloat', MType([], FloatType())),
            Symbol('putFloat', MType([FloatType()], VoidType())),
            Symbol('putFloatLn', MType([FloatType()], VoidType())),
            Symbol('getBool', MType([], BoolType())),
            Symbol('putBool', MType([BoolType()], VoidType())),
            Symbol('putBoolLn', MType([BoolType()], VoidType())),
            Symbol('getString', MType([], StringType())),
            Symbol('putString', MType([StringType()], VoidType())),
            Symbol('putStringLn', MType([StringType()], VoidType())),
            Symbol('putLn', MType([], VoidType())),
        ])

    def isEmpty(self):
        return len(self.scopeStack) == 0

    def createScope(self):
        self.scopeStack.append([])

    def getCurrentScope(self):
        if self.isEmpty():
            self.createScope()
        return self.scopeStack[-1]

    def removeLastScope(self):
        if self.isEmpty():
            return
        if self.scopeStack:
            self.scopeStack.pop()

    def addSymbolToCurrentScope(self, symbol: Symbol):
        if self.isEmpty():
            self.createScope()
        self.getCurrentScope().append(symbol)

    def addSymbolToGlobalScope(self, symbol: Symbol):
        if self.isEmpty():
            self.createScope()
        if self.scopeStack:
            self.scopeStack[0].append(symbol)

    def lookupCurrentScope(self, name):
        if self.isEmpty():
            return None
        for sym in self.getCurrentScope():
            if sym.name == name:
                return sym
        return None

    def lookupAllScope(self, name):
        if self.isEmpty():
            return None
        for scope in reversed(self.scopeStack):
            for sym in scope:
                if sym.name == name:
                    return sym
        return None

    def lookupGlobalScope(self, name):
        if self.isEmpty():
            return None
        for sym in self.scopeStack[0]:
            if sym.name == name:
                return sym
        return None

    def addPreCheck(self, symbol: Symbol):
        if self.lookupPreCheck(symbol.name) is None:
            self.preCheck[symbol] = (symbol, False)

    def lookupPreCheck(self, name: str):
        return self.preCheck.get(Symbol(name, None))

    def togglePreCheck(self, name: str):
        s = Symbol(name, None)
        self.preCheck[s] = (self.preCheck[s][0], not self.preCheck[s][1])
# endregion

# region Hoisting
# all methods come after the last struct/interface


def hoist(decl: List[Decl]):
    meth = []
    newdecl = []
    lst = -1
    for ele in decl:
        if isinstance(ele, MethodDecl):
            meth.append(ele)
        else:
            newdecl.append(ele)
            if isinstance(ele, (StructType, InterfaceType)):
                lst = len(newdecl) - 1

    for ele in meth:
        newdecl.insert(lst + 1, ele)
        lst += 1

    return newdecl

# endregion


class StaticChecker(BaseVisitor, Utils):
    def __init__(self, ast):
        self.ast = ast
        self.env = EnvManager()
        self.preCheck = True
        self.isCheckingExp = 0

    def check(self):
        self.visit(self.ast, self.env)

    def isTypeEq(self, lhs, rhs):
        if isinstance(lhs, VoidType) and isinstance(rhs, VoidType):
            return True
        for t in [IntType, FloatType, BoolType, StringType]:
            if isinstance(lhs, t) and isinstance(rhs, t):
                return True
        if isinstance(lhs, FloatType) and isinstance(rhs, IntType):
            return True
        # special type
        if isinstance(lhs, ArrayType) and isinstance(rhs, ArrayType):
            if len(lhs.dimens) != len(rhs.dimens):
                return False
            for i in range(len(lhs.dimens)):
                if lhs.dimens[i] != rhs.dimens[i]:
                    return False
            return self.isTypeEq(lhs.eleType, rhs.eleType)
        if isinstance(lhs, StructType) and isinstance(rhs, StructType):
            return lhs.name == rhs.name
        if isinstance(lhs, InterfaceType) and isinstance(rhs, InterfaceType):
            return lhs.name == rhs.name
        if isinstance(lhs, InterfaceType) and isinstance(rhs, StructType):
            iname = lhs.name
            sname = rhs.name
            iproto = [sym for sym in self.env.preCheck if sym.name.startswith(iname + '.')]
            for proto in iproto:
                smeth = self.env.lookupPreCheck(sname + '.' + proto.getName())
                if smeth is None:
                    return False
                if not self.isTypeEq(proto.mtype, smeth[0].mtype):
                    return False
            return True
        if isinstance(lhs, MType) and isinstance(rhs, MType):
            return self.isTypeEq(lhs.rettype, rhs.rettype) and len(lhs.partype) == len(rhs.partype) and all(self.isTypeEq(lhs.partype[i], rhs.partype[i]) for i in range(len(lhs.partype)))
        return type(lhs) == type(rhs)

    def isStrictTypeEq(self, lhs, rhs):
        if isinstance(lhs, VoidType) and isinstance(rhs, VoidType):
            return True
        for t in [IntType, FloatType, BoolType, StringType]:
            if isinstance(lhs, t) and isinstance(rhs, t):
                return True
        if isinstance(lhs, ArrayType) and isinstance(rhs, ArrayType):
            if len(lhs.dimens) != len(rhs.dimens):
                return False
            for i in range(len(lhs.dimens)):
                if lhs.dimens[i] != rhs.dimens[i]:
                    return False
            return self.isStrictTypeEq(lhs.eleType, rhs.eleType)
        if isinstance(lhs, StructType) and isinstance(rhs, StructType):
            return lhs.name == rhs.name
        if isinstance(lhs, InterfaceType) and isinstance(rhs, InterfaceType):
            return lhs.name == rhs.name
        if isinstance(lhs, InterfaceType) and isinstance(rhs, StructType):
            iname = lhs.name
            sname = rhs.name
            iproto = [sym for sym in self.env.preCheck if sym.name.startswith(iname + '.')]
            for proto in iproto:
                smeth = self.env.lookupPreCheck(sname + '.' + proto.getName())
                if smeth is None:
                    return False
                if not self.isStrictTypeEq(proto.mtype, smeth[0].mtype):
                    return False
            return True
        return type(lhs) == type(rhs)

    # decl : List[Decl]

    def visitProgram(self, ast: Program, env: EnvManager):
        # first, find all the typeDecl/funcDecl/methodDecl (precheck)
        ast.decl = hoist(ast.decl)
        for ele in ast.decl:
            self.visit(ele, env)
        self.preCheck = False

        # then, check for errors
        reduce(lambda acc, ele: self.visit(ele, acc), ast.decl, env)

    # region Decl
    # varName : str
    # varType : Type # None if there is no type
    # varInit : Expr # None if there is no initialization
    def visitVarDecl(self, ast: VarDecl, env: EnvManager):
        if self.preCheck:
            return

        # after precheck
        # check if the variable is declared in the current scope
        res = env.lookupCurrentScope(ast.varName)
        if not res is None:
            raise SErr.Redeclared(SErr.Variable(), ast.varName)

        if isinstance(ast.varType, Id):
            t = env.lookupPreCheck(ast.varType.name)
            if t is None:
                raise SErr.Undeclared(SErr.Identifier(), ast.varType.name)
            if not isinstance(t[0].mtype, (StructType, InterfaceType)):
                raise SErr.TypeMismatch(ast)
            ast.varType = t[0].mtype
        elif not ast.varType is None:
            ast.varType = self.visit(ast.varType, env).mtype

        val = None
        if ast.varInit:
            self.isCheckingExp += 1
            initSym = self.visit(ast.varInit, env)
            self.isCheckingExp -= 1
            if ast.varType is None:
                ast.varType = initSym.mtype

            # if not (type(ast.varType) == type(initType)):
            if isinstance(ast.varType, MType):
                raise SErr.TypeMismatch(ast)
            if not (self.isTypeEq(ast.varType, initSym.mtype)):
                raise SErr.TypeMismatch(ast)
            val = initSym.value

        s = Symbol(ast.varName, ast.varType, val)
        env.addSymbolToCurrentScope(s)
        return env

    # conName : str
    # conType : Type # None if there is no type
    # iniExpr : Expr
    def visitConstDecl(self, ast: ConstDecl, env: EnvManager):
        if self.preCheck:
            return

        # after precheck
        res = env.lookupCurrentScope(ast.conName)
        if not res is None:
            raise SErr.Redeclared(SErr.Constant(), ast.conName)
        # conType
        if isinstance(ast.conType, Id):
            t = env.lookupPreCheck(ast.conType.name)
            if t is None:
                raise SErr.Undeclared(SErr.Identifier(), ast.conType.name)
            if not isinstance(t[0].mtype, (StructType, InterfaceType)):
                raise SErr.TypeMismatch(ast)
            ast.conType = t[0].mtype
        elif not ast.conType is None:
            ast.conType = self.visit(ast.conType, env).mtype
        # visit iniExpr
        self.isCheckingExp += 1
        initSym = self.visit(ast.iniExpr, env)
        self.isCheckingExp -= 1
        if ast.conType is None:
            ast.conType = initSym.mtype
        if isinstance(ast.conType, MType):
            raise SErr.TypeMismatch(ast)
        # if not (type(ast.conType) == type(initType)):
        if not (self.isTypeEq(ast.conType, initSym.mtype)):
            raise SErr.TypeMismatch(ast)
        s = Symbol(ast.conName, ast.conType, initSym.value)
        env.addSymbolToCurrentScope(s)
        return env

    # name: str
    # params: List[ParamDecl]
    # retType: Type # VoidType if there is no return type
    # body: Block

    def visitFuncDecl(self, ast: FuncDecl, env: EnvManager):
        if self.preCheck:
            paramTypes = list(map(lambda x: x.parType, ast.params))
            s = Symbol(ast.name, MType(paramTypes, ast.retType))
            return env.addPreCheck(s)

        # after precheck
        # check precheck list and global scope
        f = env.lookupPreCheck(ast.name)
        isDeclared = f[1] or (not env.lookupGlobalScope(ast.name) is None)
        if isDeclared:
            raise SErr.Redeclared(SErr.Function(), ast.name)
        env.togglePreCheck(ast.name)
        # add function to globalscope
        env.addSymbolToGlobalScope(f[0])

        # works with inner scope
        env.createScope()
        newParTypes = []
        # params
        for param in ast.params:
            res = env.lookupCurrentScope(param.parName)
            if not res is None:
                raise SErr.Redeclared(SErr.Parameter(), param.parName)
            s = Symbol(param.parName, self.visit(param.parType, env).mtype)
            newParTypes.append(s.mtype)
            env.addSymbolToCurrentScope(s)
        f[0].mtype.partype = newParTypes
        # retType
        if isinstance(ast.retType, Id):
            t = env.lookupPreCheck(ast.retType.name)
            if t is None:
                raise SErr.Undeclared(SErr.Identifier(), ast.retType.name)
            if not isinstance(t[0].mtype, (StructType, InterfaceType)):
                raise SErr.TypeMismatch(ast)
            ast.retType = t[0].mtype
        elif not ast.retType is None:
            ast.retType = self.visit(ast.retType, env).mtype
        f[0].mtype.rettype = ast.retType
        # body
        bsym = self.visit(ast.body, env)
        # remove inner scope
        env.removeLastScope()
        # type mismatch return

        last_return = next((m for m in reversed(ast.body.member) if isinstance(m, Return)), ast.body.member)
        if not self.isStrictTypeEq(bsym.mtype, ast.retType):
            raise SErr.TypeMismatch(last_return)
        return env

    # receiver: str
    # recType: Type
    # fun: FuncDecl
    def visitMethodDecl(self, ast: MethodDecl, env: EnvManager):
        methodName = ast.recType.name + '.' + ast.fun.name
        # precheck
        if self.preCheck:
            paramTypes = list(map(lambda x: x.parType, ast.fun.params))
            s = Symbol(methodName, MType(paramTypes, ast.fun.retType))
            return env.addPreCheck(s)

        # after precheck
        f = env.lookupPreCheck(methodName)
        isDeclared = f[1] or (not env.lookupGlobalScope(methodName) is None)
        if isDeclared:
            raise SErr.Redeclared(SErr.Method(), ast.fun.name)
        env.togglePreCheck(methodName)

        # add method to globalscope
        env.addSymbolToGlobalScope(f[0])

        # works with inner scope
        env.createScope()
        # add receiver to current scope
        if isinstance(ast.recType, Id):
            t = env.lookupAllScope(ast.recType.name)
            if t is None:
                raise SErr.Undeclared(SErr.Identifier(), ast.recType.name)
            if not isinstance(t.mtype, (StructType, InterfaceType)):
                raise SErr.TypeMismatch(ast)
        s = Symbol(ast.receiver, t.mtype)
        env.addSymbolToCurrentScope(s)
        newParTypes = []
        # params
        env.createScope()
        for param in ast.fun.params:
            res = env.lookupCurrentScope(param.parName)
            if not res is None:
                raise SErr.Redeclared(SErr.Parameter(), param.parName)
            s = Symbol(param.parName, self.visit(param.parType, env).mtype)
            newParTypes.append(s.mtype)
            env.addSymbolToCurrentScope(s)
        f[0].mtype.partype = newParTypes
        # rettype
        if isinstance(ast.fun.retType, Id):
            t = env.lookupPreCheck(ast.retType.name)
            if t is None:
                raise SErr.Undeclared(SErr.Identifier(), ast.fun.retType.name)
            if not isinstance(t[0].mtype, (StructType, InterfaceType)):
                raise SErr.TypeMismatch(ast)
            ast.fun.retType = t[0].mtype
        elif not ast.fun.retType is None:
            ast.fun.retType = self.visit(ast.fun.retType, env).mtype
        f[0].mtype.rettype = ast.fun.retType
        print('METHDECL', f[0])
        # body
        bsym = self.visit(ast.fun.body, env)
        # remove params scope
        env.removeLastScope()
        # remove inner scope
        env.removeLastScope()
        # type mismatch return
        last_return = next((m for m in reversed(ast.fun.body.member) if isinstance(m, Return)), ast.fun.body.member)
        if not self.isStrictTypeEq(bsym.mtype, ast.fun.retType):
            raise SErr.TypeMismatch(last_return)
        return env

    # name: str
    # elements:List[Tuple[str,Type]]
    # methods:List[MethodDecl]
    # BASICALLY STRUCT DECLARATION
    def visitStructType(self, ast: StructType, env: EnvManager):
        if self.preCheck:
            s = Symbol(ast.name, StructType(ast.name, [], []))
            for ele in ast.elements:
                e = Symbol(ast.name + '.' + ele[0], ele[1])
                env.addPreCheck(e)
            for method in ast.methods:
                self.visit(method, env)
            return env.addPreCheck(s)

        # after precheck
        # check precheck list and global scope
        s = env.lookupPreCheck(ast.name)
        isDeclared = s[1] or (not env.lookupGlobalScope(ast.name) is None)
        if isDeclared:
            raise SErr.Redeclared(SErr.Type(), ast.name)
        env.togglePreCheck(ast.name)

        # add struct to globalscope
        env.addSymbolToGlobalScope(s[0])

        # visits elements
        for ele in ast.elements:
            ename = ast.name + '.' + ele[0]
            e = env.lookupPreCheck(ename)
            isEleDeclared = e[1] or (not env.lookupGlobalScope(ename) is None)
            if isEleDeclared:
                raise SErr.Redeclared(SErr.Field(), ele[0])
            env.togglePreCheck(ename)
            env.addSymbolToGlobalScope(e[0])

        # visits methods
        for method in ast.methods:
            m = self.visit(method, env)
        return env

    # name: str
    # methods:List[Prototype]
    # BASICALLY INTERFACE DECLARATION
    def visitInterfaceType(self, ast: InterfaceType, env: EnvManager):
        if self.preCheck:
            s = Symbol(ast.name, InterfaceType(ast.name, []))
            for method in ast.methods:
                m = self.visit(method, env)
                m.name = ast.name + '.' + m.name
                env.addPreCheck(m)
            return env.addPreCheck(s)

        # after precheck
        # check precheck list and global scope
        s = env.lookupPreCheck(ast.name)
        isDeclared = s[1] or (not env.lookupGlobalScope(ast.name) is None)
        if isDeclared:
            raise SErr.Redeclared(SErr.Type(), ast.name)
        env.togglePreCheck(ast.name)

        # add interface to globalscope
        env.addSymbolToGlobalScope(s[0])

        # visits prototype
        for method in ast.methods:
            mName = ast.name + '.' + method.name
            f = env.lookupPreCheck(mName)
            isDeclared = f[1] or (not env.lookupGlobalScope(mName) is None)
            if isDeclared:
                raise SErr.Redeclared(SErr.Prototype(), method.name)
            env.togglePreCheck(mName)
            # params
            newParTypes = []
            for param in method.params:
                newParTypes.append(self.visit(param, env).mtype)
            f[0].mtype.partype = newParTypes
            # rettype
            if isinstance(method.retType, Id):
                t = env.lookupPreCheck(method.retType.name)
                if t is None:
                    raise SErr.Undeclared(SErr.Identifier(), method.retType.name)
                if not isinstance(t[0].mtype, (StructType, InterfaceType)):
                    raise SErr.TypeMismatch(ast)
                method.retType = t[0].mtype
            elif not method.retType is None:
                method.retType = self.visit(method.retType, env).mtype
            f[0].mtype.rettype = method.retType

            # add method to globalscope
            env.addSymbolToGlobalScope(f[0])
        return env

    # name: str
    # params:List[Type]
    # retType: Type # VoidType if there is no return type
    # THIS IS INTERFACE METHOD
    def visitPrototype(self, ast: Prototype, env: EnvManager):

        if self.preCheck:
            s = Symbol(ast.name, MType(ast.params, ast.retType))
            return s

        # after precheck

        # this was done in interface already
    # endregion

    # region Type

    def visitIntType(self, ast: IntType, env: EnvManager):
        return Symbol(None, IntType(), None)

    def visitFloatType(self, ast: FloatType, env: EnvManager):
        return Symbol(None, FloatType(), None)

    def visitBoolType(self, ast: BoolType, env: EnvManager):
        return Symbol(None, BoolType(), None)

    def visitStringType(self, ast: StringType, env: EnvManager):
        return Symbol(None, StringType(), None)

    def visitVoidType(self, ast: VoidType, env: EnvManager):
        return Symbol(None, VoidType(), None)

    # dimens:List[Expr]
    # eleType:Type
    def visitArrayType(self, ast: ArrayType, env: EnvManager):
        dimensCalc = []
        for ele in ast.dimens:
            self.isCheckingExp += 1
            d = self.visit(ele, env)
            self.isCheckingExp -= 1
            if not isinstance(d.mtype, IntType):
                raise SErr.TypeMismatch(ast)
            if d.value is None:
                d.value = 0
            dimensCalc.append(IntLiteral(d.value))
        t = self.visit(ast.eleType, env).mtype
        return Symbol(None, ArrayType(dimensCalc, t), None)
    # endregion

    # region Stmt
    # member:List[BlockMember]
    def visitBlock(self, ast: Block, env: EnvManager):
        r = Symbol(None, VoidType(), None)
        env.createScope()
        for ele in ast.member:
            e = self.visit(ele, env)
            if isinstance(ele, Return):
                r = e
        env.removeLastScope()
        return r

    # lhs: LHS
    # rhs: Expr # if assign operator is +=, rhs is BinaryOp(+,lhs,rhs), similar to -=,*=,/=,%=
    def visitAssign(self, ast: Assign, env: EnvManager):
        # if LHS is undeclared this is an var decl
        isDecl = False
        lhs = None
        if isinstance(ast.lhs, Id):
            res = env.lookupCurrentScope(ast.lhs.name)
            if res is None:
                lhs = Symbol(ast.lhs.name, None)
                env.addSymbolToCurrentScope(lhs)
                isDecl = True

        lhsSym = lhs
        if lhsSym is None:
            self.isCheckingExp += 1
            lhsSym = self.visit(ast.lhs, env)
            self.isCheckingExp -= 1

        self.isCheckingExp += 1
        rhsSym = self.visit(ast.rhs, env)
        self.isCheckingExp -= 1

        if not isDecl:
            if not self.isTypeEq(lhsSym.mtype, rhsSym.mtype):
                raise SErr.TypeMismatch(ast)
        lhsSym.value = rhsSym.value

    # expr:Expr
    # thenStmt:Stmt
    # elseStmt:Stmt # None if there is no else
    def visitIf(self, ast: If, env: EnvManager):
        self.isCheckingExp += 1
        exprSym = self.visit(ast.expr, env)
        self.isCheckingExp -= 1

        if not isinstance(exprSym.mtype, BoolType):
            raise SErr.TypeMismatch(ast)
        self.visit(ast.thenStmt, env)
        if not ast.elseStmt is None:
            self.visit(ast.elseStmt, env)

    # cond:Expr
    # loop:Block
    def visitForBasic(self, ast: ForBasic, env: EnvManager):
        self.isCheckingExp += 1
        condSym = self.visit(ast.cond, env)
        self.isCheckingExp -= 1

        if not isinstance(condSym.mtype, BoolType):
            raise SErr.TypeMismatch(ast)
        self.visit(ast.loop, env)

    # init:Stmt
    # cond:Expr
    # upda:Assign
    # loop:Block
    def visitForStep(self, ast: ForStep, env: EnvManager):
        env.createScope()
        # init
        self.visit(ast.init, env)
        # cond
        self.isCheckingExp += 1
        condSym = self.visit(ast.cond, env)
        self.isCheckingExp -= 1
        if not isinstance(condSym.mtype, BoolType):
            raise SErr.TypeMismatch(ast)
        # upda
        self.visit(ast.upda, env)
        # loop
        for ele in ast.loop.member:
            self.visit(ele, env)
        env.removeLastScope()

    # idx: Id
    # value: Id
    # arr: Expr
    # loop:Block
    def visitForEach(self, ast: ForEach, env: EnvManager):
        # idx
        idxSym = self.visit(ast.idx, env)
        if not isinstance(idxSym.mtype, IntType):
            raise SErr.TypeMismatch(ast)
        # value
        valueSym = self.visit(ast.value, env)
        # arr
        self.isCheckingExp += 1
        arr = self.visit(ast.arr, env)
        if not self.isTypeEq(valueSym.mtype, arr.mtype.eleType):
            raise SErr.TypeMismatch(ast)
        if not isinstance(arr.mtype, ArrayType):
            raise SErr.TypeMismatch(ast)
        self.isCheckingExp -= 1
        # block
        self.visit(ast.loop, env)

    def visitContinue(self, ast: Continue, env: EnvManager):
        return None

    def visitBreak(self, ast: Break, env: EnvManager):
        return None

    # expr:Expr # None if there is no expr
    def visitReturn(self, ast: Return, env: EnvManager):
        ret = Symbol(None, VoidType(), None)
        if ast.expr is not None:
            self.isCheckingExp += 1
            ret = self.visit(ast.expr, env)
            self.isCheckingExp -= 1
        return ret
    # endregion

    # region Expr
    # op:str
    # left:Expr
    # right:Expr
    def visitBinaryOp(self, ast: BinaryOp, env: EnvManager):
        # exp check flag

        self.isCheckingExp += 1
        lsym = self.visit(ast.left, env)
        self.isCheckingExp -= 1
        self.isCheckingExp += 1
        rsym = self.visit(ast.right, env)
        self.isCheckingExp -= 1

        if lsym.value is None:
            if isinstance(lsym.mtype, (IntType, FloatType)):
                lsym.value = 0
            elif isinstance(lsym.mtype, StringType):
                lsym.value = ""
            elif isinstance(lsym.mtype, BoolType):
                lsym.value = False
        if rsym.value is None:
            if isinstance(rsym.mtype, (IntType, FloatType)):
                rsym.value = 0
            elif isinstance(rsym.mtype, StringType):
                rsym.value = ""
            elif isinstance(rsym.mtype, BoolType):
                rsym.value = False

        l = lsym.mtype
        r = rsym.mtype
        match ast.op:
            case '+':
                # return
                for t in [IntType, FloatType, StringType]:
                    if isinstance(l, t) and isinstance(r, t):
                        return Symbol(None, l, lsym.value + rsym.value)
                if isinstance(l, IntType) and isinstance(r, FloatType):
                    return Symbol(None, FloatType(), lsym.value + rsym.value)
                if isinstance(l, FloatType) and isinstance(r, IntType):
                    return Symbol(None, FloatType(), lsym.value + rsym.value)
                # throw
                raise SErr.TypeMismatch(ast)
            case '-':
                # return
                for t in [IntType, FloatType]:
                    if isinstance(l, t) and isinstance(r, t):
                        return Symbol(None, l, lsym.value - rsym.value)
                if isinstance(l, IntType) and isinstance(r, FloatType):
                    return Symbol(None, FloatType(), lsym.value - rsym.value)
                if isinstance(l, FloatType) and isinstance(r, IntType):
                    return Symbol(None, FloatType(), lsym.value - rsym.value)
                # throw
                raise SErr.TypeMismatch(ast)
            case '*':
                # return
                for t in [IntType, FloatType]:
                    if isinstance(l, t) and isinstance(r, t):
                        return Symbol(None, l, lsym.value * rsym.value)
                if isinstance(l, IntType) and isinstance(r, FloatType):
                    return Symbol(None, FloatType(), lsym.value * rsym.value)
                if isinstance(l, FloatType) and isinstance(r, IntType):
                    return Symbol(None, FloatType(), lsym.value * rsym.value)
                # throw
                raise SErr.TypeMismatch(ast)
            case '/':
                # return
                for t in [IntType, FloatType]:
                    if isinstance(l, t) and isinstance(r, t):
                        return Symbol(None, l, lsym.value / rsym.value)
                if isinstance(l, IntType) and isinstance(r, FloatType):
                    return Symbol(None, FloatType(), lsym.value / rsym.value)
                if isinstance(l, FloatType) and isinstance(r, IntType):
                    return Symbol(None, FloatType(), lsym.value / rsym.value)
                # throw
                raise SErr.TypeMismatch(ast)
            case '%':
                # return
                if isinstance(l, IntType) and isinstance(r, IntType):
                    return Symbol(None, IntType(), lsym.value % rsym.value)
                # throw
                raise SErr.TypeMismatch(ast)
            case '==':
                # return
                for t in [IntType, FloatType, StringType]:
                    if isinstance(l, t) and isinstance(r, t):
                        return Symbol(None, BoolType(), lsym.value == rsym.value)
                # throw
                raise SErr.TypeMismatch(ast)
            case '!=':
                # return
                for t in [IntType, FloatType, StringType]:
                    if isinstance(l, t) and isinstance(r, t):
                        return Symbol(None, BoolType(), lsym.value != rsym.value)
                # throw
                raise SErr.TypeMismatch(ast)
            case '<':
                # return
                for t in [IntType, FloatType, StringType]:
                    if isinstance(l, t) and isinstance(r, t):
                        return Symbol(None, BoolType(), lsym.value < rsym.value)
                # throw
                raise SErr.TypeMismatch(ast)
            case '<=':
                # return
                for t in [IntType, FloatType, StringType]:
                    if isinstance(l, t) and isinstance(r, t):
                        return Symbol(None, BoolType(), lsym.value <= rsym.value)
                # throw
                raise SErr.TypeMismatch(ast)
            case '>':
                # return
                for t in [IntType, FloatType, StringType]:
                    if isinstance(l, t) and isinstance(r, t):
                        return Symbol(None, BoolType(), lsym.value > rsym.value)
                # throw
                raise SErr.TypeMismatch(ast)
            case '>=':
                # return
                for t in [IntType, FloatType, StringType]:
                    if isinstance(l, t) and isinstance(r, t):
                        return Symbol(None, BoolType(), lsym.value >= rsym.value)
                # throw
                raise SErr.TypeMismatch(ast)
            case '&&':
                # return
                if isinstance(l, BoolType) and isinstance(r, BoolType):
                    return Symbol(None, BoolType(), lsym.value and rsym.value)
                # throw
                raise SErr.TypeMismatch(ast)
            case '||':
                # return
                if isinstance(l, BoolType) and isinstance(r, BoolType):
                    return Symbol(None, BoolType(), lsym.value or rsym.value)
                # throw
                raise SErr.TypeMismatch(ast)
        # exp check flag

        return l

    # op:str
    # body:Expr
    def visitUnaryOp(self, ast: UnaryOp, env: EnvManager):
        # exp check flag

        self.isCheckingExp += 1
        b = self.visit(ast.body, env)
        self.isCheckingExp -= 1

        if b.value is None:
            if isinstance(b.mtype, (IntType, FloatType)):
                b.value = 0
            elif isinstance(b.mtype, StringType):
                b.value = ""
            elif isinstance(b.mtype, BoolType):
                b.value = False
        match ast.op:
            case '-':
                if isinstance(b, (IntType, FloatType)):
                    return Symbol(None, b.mtype, -b.value)
                raise SErr.TypeMismatch(ast)
            case '!':
                if isinstance(b, BoolType):
                    return Symbol(None, BoolType(), not b.value)
                raise SErr.TypeMismatch(ast)
        # exp check flag

        return b

    # funName:str
    # args:List[Expr] # [] if there is no arg
    def visitFuncCall(self, ast: FuncCall, env: EnvManager):
        res = env.lookupPreCheck(ast.funName)
        l = env.lookupAllScope(ast.funName)

        ret = None

        if not l is None:
            if not isinstance(l.mtype, MType):
                raise SErr.Undeclared(SErr.Function(), ast.funName)
            if self.isCheckingExp == 0 and not isinstance(l.mtype.rettype, VoidType):
                raise SErr.TypeMismatch(ast)
            if self.isCheckingExp > 0 and isinstance(l.mtype.rettype, VoidType):
                raise SErr.TypeMismatch(ast)
            ret = Symbol(None, l.mtype.rettype, None)
        elif not res is None:
            if not isinstance(res[0].mtype, MType):
                raise SErr.Undeclared(SErr.Function(), ast.funName)
            if self.isCheckingExp == 0 and not isinstance(res[0].mtype.rettype, VoidType):
                raise SErr.TypeMismatch(ast)
            if self.isCheckingExp > 0 and isinstance(res[0].mtype.rettype, VoidType):
                raise SErr.TypeMismatch(ast)
            ret = Symbol(None, res[0].mtype.rettype, None)
        else:
            raise SErr.Undeclared(SErr.Function(), ast.funName)

        # check params
        x = None
        if not l is None:
            x = l
        elif not res is None:
            x = res[0]
        if len(x.mtype.partype) != len(ast.args):
            raise SErr.TypeMismatch(ast)
        for i in range(len(ast.args)):
            self.isCheckingExp += 1
            arg = self.visit(ast.args[i], env)
            self.isCheckingExp -= 1
            if not self.isStrictTypeEq(arg.mtype, x.mtype.partype[i]):
                raise SErr.TypeMismatch(ast)

        return ret

    # receiver: Expr
    # metName: str
    # args:List[Expr]
    def visitMethCall(self, ast: MethCall, env: EnvManager):
        self.isCheckingExp += 1
        rsym = self.visit(ast.receiver, env)
        self.isCheckingExp -= 1
        # check if receiver type is a struct/interface
        if not isinstance(rsym.mtype, (StructType, InterfaceType)):
            raise SErr.TypeMismatch(ast)
        # check if method is declared
        res = env.lookupPreCheck(rsym.mtype.name + '.' + ast.metName)
        if (res is None) or (not isinstance(res[0].mtype, MType)):
            raise SErr.Undeclared(SErr.Method(), ast.metName)
        if self.isCheckingExp == 0 and not isinstance(res[0].mtype.rettype, VoidType):
            raise SErr.TypeMismatch(ast)
        if self.isCheckingExp > 0 and isinstance(res[0].mtype.rettype, VoidType):
            raise SErr.TypeMismatch(ast)

        # check params
        if len(res[0].mtype.partype) != len(ast.args):
            raise SErr.TypeMismatch(ast)
        for i in range(len(ast.args)):
            self.isCheckingExp += 1
            arg = self.visit(ast.args[i], env)
            self.isCheckingExp -= 1
            if not self.isStrictTypeEq(arg.mtype, res[0].mtype.partype[i]):
                raise SErr.TypeMismatch(ast)
        return Symbol(None, res[0].mtype.rettype, None)

    # name : str
    def visitId(self, ast: Id, env: EnvManager):
        res = env.lookupAllScope(ast.name)
        if res is None:
            raise SErr.Undeclared(SErr.Identifier(), ast.name)
        return res

    # arr:Expr
    # idx:List[Expr]

    def visitArrayCell(self, ast: ArrayCell, env: EnvManager):
        # exp check flag
        self.isCheckingExp += 1
        arrSym = self.visit(ast.arr, env)
        self.isCheckingExp -= 1
        if not isinstance(arrSym.mtype, ArrayType):
            raise SErr.TypeMismatch(ast)
        for ele in ast.idx:
            self.isCheckingExp += 1
            tsym = self.visit(ele, env)
            self.isCheckingExp -= 1
            if not isinstance(tsym.mtype, IntType):
                raise SErr.TypeMismatch(ast)
        # exp check flag

        return Symbol(None, arrSym.mtype.eleType, None)

    # receiver:Expr
    # field:str
    def visitFieldAccess(self, ast: FieldAccess, env: EnvManager):
        # exp check flag
        self.isCheckingExp += 1
        rsym = self.visit(ast.receiver, env)
        self.isCheckingExp -= 1
        # check if receiver is a struct/interface
        if not isinstance(rsym.mtype, (StructType, InterfaceType)):
            raise SErr.TypeMismatch(ast)
        # check if field is declared
        res = env.lookupPreCheck(rsym.mtype.name + '.' + ast.field)
        if (res is None) or (isinstance(res[0].mtype, MType)):
            raise SErr.Undeclared(SErr.Field(), ast.field)
        return Symbol(None, res[0].mtype, None)
    # endregion

    # region PrimLit
    # value:int
    def visitIntLiteral(self, ast: IntLiteral, env: EnvManager):
        return Symbol(None, IntType(), int(ast.value))

    # value:float
    def visitFloatLiteral(self, ast: FloatLiteral, env: EnvManager):
        return Symbol(None, FloatType(), float(ast.value))

    # value:bool
    def visitBooleanLiteral(self, ast: BooleanLiteral, env: EnvManager):
        return Symbol(None, BoolType(), True if ast.value == 'true' else False)

    # value:str
    def visitStringLiteral(self, ast: StringLiteral, env: EnvManager):
        return Symbol(None, StringType(), ast.value)
    # endregion

    # region OtherLit
    # dimens:List[Expr]
    # eleType: Type
    # value: NestedList
    def visitArrayLiteral(self, ast: ArrayLiteral, env: EnvManager):
        # return ArrayType(ast.dimens, ast.eleType)
        calcDimens = []
        for dimen in ast.dimens:
            self.isCheckingExp += 1
            d = self.visit(dimen, env)
            self.isCheckingExp -= 1
            if not isinstance(d.mtype, IntType):
                raise SErr.TypeMismatch(ast)
            calcDimens.append(IntLiteral(d.value))
        t = self.visit(ast.eleType, env).mtype
        return Symbol(None, ArrayType(calcDimens, t), ast.value)

    # name:str
    # elements: List[Tuple[str,Expr]] # [] if there is no elements
    def visitStructLiteral(self, ast: StructLiteral, env: EnvManager):
        # return StructType(ast.name, [], [])
        for elem in ast.elements:
            self.isCheckingExp += 1
            e = self.visit(elem[1], env)
            self.isCheckingExp -= 1
        return Symbol(None, StructType(ast.name, [], []), ast.elements)

    def visitNilLiteral(self, ast: NilLiteral, env: EnvManager):
        return Symbol(None, None, None)
    # endregion


# Expr: BinaryOp, UnaryOp, FuncCall, MethCall, Literal
# Literal: PrimLit, ArrayLit, StructLit, NilLit
# PrimLit: IntLit, FloatLit, BoolLit, StringLit
