class Variable:
    def get_name(self):
        pass


class Assignment:
    def get_var(self) -> Variable:
        pass

    def get_value(self) -> float:
        pass

    def set_value(self, f: float):
        pass


class Assignments:
    def __getitem__(self, v: Variable) -> float:
        pass

    def __iadd__(self, ass: Assignment):
        pass


class Expression:
    def evaluate(self, assgms: Assignments) -> float:
        pass

    def derivative(self, v: Variable):
        pass

    def __repr__(self) -> str:
        pass

    def __eq__(self, other):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __pow__(self, power: float, modulo=None):
        pass



class ValueAssignment(Assignment):


    def __init__(self, v:Variable, value:float):
       self.v=v
       self.value=value



    def __eq__(self, other) -> bool:
        return self.value == other.value and self.v==other.v


    def __repr__(self) -> str:
        return str(self.v) +'='+str(self.value)


    def get_var(self) -> Variable:
        return self.v

    def get_value(self) -> float:
        return self.value

    def set_value(self, f: float):
        f = self.value
        return f

    #TODO complete all Assignment interface methods

class SimpleDictionaryAssignments(Assignments):
    def __init__(self):
        self.mydict={}


    def __getitem__(self, v: Variable) -> float:

        return self.mydict[v]


    def __iadd__(self, ass: Assignment):
        fass=str(ass)
        lst=fass.split('=')

        if lst[0] in self.mydict:
            if self.mydict[lst[0]]==lst[1]:
                pass
        else:
            self.mydict[lst[0]]=lst[1]
        return self
    # TODO complete all Assignments interface methods


class Constant(Expression):

    def __init__(self, value: float=0.0):
        self.value=float(value)
    def evaluate(self, assgms='x=10') -> float:
        return self.value

    def derivative(self, v: Variable):
        return 0.0

    def __repr__(self) -> str:
        return str(self.value)

    def __eq__(self, other):
        return str(self.value)==str(other)

    def __add__(self, other):
        return self.value+other.value

    def __sub__(self, other):
        return self.value-other.value

    def __mul__(self, other):
        return self.value*other.value

    def __pow__(self, power: float, modulo=None):

        if type(power) is not float:
            try:
                a=float(power)

            except:
                raise ValueError
            if type (a) is not float:
                raise ValueError
            else:
                return self.value ** a
        else:
            return self.value**power



    # TODO complete all Expression interface methods


class VariableExpression(Variable,Expression):
    def __init__(self, variable_name):
        self.varname=variable_name
    def get_name(self):
        return str(self.varname)

    def evaluate(self, assgms: Assignments) -> float:
        try:
            return assgms[self.varname]
        except:
            try:
                return self.varname.evaluate(assgms)
            except:
                raise ValueError




    def derivative(self, v: Variable):
        lst=[]

        if isinstance(self.varname,Addition) or isinstance(self.varname,Multiplication) or isinstance(self.varname,Subtraction) or isinstance(self.varname,Power):
            h=self.varname.derivative(v)

            return h


        for i in range(len(str(self.varname))):
            if str(v) ==str(self.varname)[i:i+1] :
                lst.append( Constant(1.0) )
            else:
                if str(self.varname)[i:i+1].isalpha() or (str(self.varname)[i:i+1]).isdigit():
                    lst.append(Constant(0.0))
        a=lst[0]
        varlst=[]
        if len(lst)>1:
            for i in range(len(str(self.varname))):
                varlst.append(str(self.varname)[i:i+1])
            for k in range(1,len(lst)):
                if '+' in varlst:
                    a=Addition(a,lst[k])
                elif '-' in varlst:
                    a = Subtraction(a, lst[k])

        return a




    def __repr__(self) -> str:
        return str(self.varname)

    def __eq__(self, other):
        return str(self.varname)==str(other.varname)

    def __add__(self, other):

        return Addition(self.varname,other.varname)


    def __sub__(self, other):
        return Subtraction(self.varname,other.varname)

    def __mul__(self, other):
        return Multiplication(self.varname,other.varname)

    def __pow__(self, power: float, modulo=None):
        if type(power) is not float:
            try:
                a = float(power)

            except:
                raise ValueError
            if type(a) is not float:
                raise ValueError
            else:
                return Power(self.varname, a)
        else:
            return Power(self.varname, power)


    # TODO complete all Variable & Expression interface methods


class Addition(Expression):
    def __init__(self, A: Expression, B: Expression) -> Expression:
        try:
            self.firstvar=Constant(float(A))
        except:
            self.firstvar=VariableExpression(A)
        try:
            self.secondvar = Constant(float(B))
        except:
            self.secondvar = VariableExpression(B)
        pass
    def variables_number(self,exp):
        number=0
        for i in exp:
            if i == self.firstvar or self.secondvar:
                number+=1
        return number


    def evaluate(self, assgms: Assignments) -> float:
        try:
            res=float(self.firstvar.evaluate(assgms)) +float(self.secondvar.evaluate(assgms))

        except:
            raise ValueError
        if type(res) is not float:
            raise ValueError
        else:
            return res

    def derivative(self, v: Variable):
        return Addition(self.firstvar.derivative(v), self.secondvar.derivative(v))


    def __repr__(self) -> str:
        return "({}+{})".format(self.firstvar, self.secondvar)

    def __eq__(self, other):
        return str(self)==str(other)


    def __add__(self, other):

        return Addition(Addition(self.firstvar,self.secondvar),other)

    def __sub__(self, other):
        return Subtraction(Addition(self.firstvar,self.secondvar),other)

    def __mul__(self, other):
        return Multiplication(Addition(self.firstvar,self.secondvar),other)
    def __pow__(self, power: float, modulo=None):
        if type(power) is not float:
            try:
                a = float(power)

            except:
                raise ValueError
            if type(a) is not float:
                raise ValueError
            else:
                return Power(Addition(self.firstvar,self.secondvar),a)
        else:
            return Power(Addition(self.firstvar, self.secondvar), power)


    # TODO complete all Expression interface methods


class Subtraction(Expression):
    def __init__(self, A: Expression, B: Expression) -> Expression:
        try:
            self.firstvar = Constant(float(A))
        except:
            self.firstvar =VariableExpression(A)
        try:
            self.secondvar = Constant(float(B))
        except:
            self.secondvar =VariableExpression(B)


    def evaluate(self, assgms: Assignments) -> float:
        try:
            res = float(self.firstvar.evaluate(assgms)) - float(self.secondvar.evaluate(assgms))

        except:
            raise ValueError
        if type(res) is not float:
            raise ValueError
        else:
            return res

    def derivative(self, v: Variable):
        return Subtraction(self.firstvar.derivative(v), self.secondvar.derivative(v))

    def __repr__(self) -> str:
        return "({}-{})".format(self.firstvar, self.secondvar)

    def __eq__(self, other):
        return str(self)==str(other)

    def __add__(self, other):

        return Addition(Subtraction(self.firstvar, self.secondvar), other)

    def __sub__(self, other):
        return Subtraction(Subtraction(self.firstvar, self.secondvar), other)

    def __mul__(self, other):
        return Multiplication(Subtraction(self.firstvar, self.secondvar), other)

    def __pow__(self, power: float, modulo=None):
        if type(power) is not float:
            try:
                a = float(power)

            except:
                raise ValueError
            if type(a) is not float:
                raise ValueError
            else:
                return Power(Subtraction(self.firstvar, self.secondvar), a)
        else:
            return Power(Subtraction(self.firstvar, self.secondvar), power)

    # TODO complete all Expression interface methods


class Multiplication(Expression):
    def __init__(self, A: Expression, B: Expression) -> Expression:
        try:
            self.firstvar = Constant(float(A))
        except:
            self.firstvar = VariableExpression(A)
        try:
            self.secondvar = Constant(float(B))
        except:
            self.secondvar = VariableExpression(B)


    def evaluate(self, assgms: Assignments) -> float:
        try:
            res = float(self.firstvar.evaluate(assgms)) * float(self.secondvar.evaluate(assgms))

        except:
            raise ValueError
        if type(res) is not float:
            raise ValueError
        else:
            return res

    def derivative(self, v: Variable):
        return Addition(Multiplication(self.firstvar.derivative(v),self.secondvar),Multiplication( self.firstvar,self.secondvar.derivative(v)))

    def __repr__(self) -> str:
        return "({}*{})".format(self.firstvar, self.secondvar)

    def __eq__(self, other):
        return str(self)==str(other)


    def __add__(self, other):

        return Addition(Multiplication(self.firstvar, self.secondvar), other)

    def __sub__(self, other):
        return Subtraction(Multiplication(self.firstvar, self.secondvar), other)

    def __mul__(self, other):
        return Multiplication(Multiplication(self.firstvar, self.secondvar), other)

    def __pow__(self, power: float, modulo=None):
        if type(power) is not float:
            try:
                a = float(power)

            except:
                raise ValueError
            if type(a) is not float:
                raise ValueError
            else:
                return Power(Multiplication(self.firstvar, self.secondvar), a)
        else:
            return Power(Multiplication(self.firstvar, self.secondvar), power)

    # TODO complete all Expression interface methods

class Power(Expression):
    def __init__(self, exp: Expression, p: float) -> Expression:
        try:
            self.exp = Constant(float(exp))
        except:
            self.exp= exp
        try:
            self.p=float(p)
        except:
            raise ValueError
        pass
    # TODO complete all Expression interface methods
    def evaluate(self, assgms: Assignments) -> float:
        try:
            res=float(self.exp.evaluate(assgms))**self.p

        except:

            raise ValueError
        if type(res) is not float:
            raise ValueError
        else:
            return res


    def derivative(self, v: Variable):
        return Multiplication(Multiplication(self.p,Power(self.exp,str(self.p-1))),self.exp.derivative(v))

    def __repr__(self) -> str:
        return "({}^{})".format(self.exp, self.p)

    def __eq__(self, other):
        return str(self)==str(other)

    def __add__(self, other):
        return Addition(self,other)

    def __sub__(self, other):
        return Subtraction(self,other)

    def __mul__(self, other):
        return Multiplication(self,other)

    def __pow__(self, power: float, modulo=None):
        if type(power) is not float:
            try:
                a = float(power)

            except:
                raise ValueError
            if type(a) is not float:
                raise ValueError
            else:
                return Power(Power(self, a))
        else:
            return Power(Power(self, power))

class Polynomial(Expression):
    def __init__(self, v: Variable, coefs: list) -> Expression:
        self.var = v
        self.co = coefs


    def evaluate(self, assgms: Assignments) -> float:
        r=0.0

        for i in range (len(self.co)):
            r+=float(self.co[i])*((float(VariableExpression(self.var).evaluate(sda)))**float(i))
        return r

    def derivative(self, v: Variable):
        if  self.var==v:
            lst=[]
            for i in range(1, len(self.co)):
                lst.append(self.co[i] * i)

            return Polynomial(v, lst)
        else:
            return Constant(0.0)

    def __repr__(self) -> str:
        rep = '('

        for i in range(len(self.co) - 1, -1, -1):

            if self.co[i]!=0:
                bl=True
                if i !=(len(self.co) - 1) and bl:
                    rep += '+'

                if i == 0:
                    rep += str(self.co[i])
                    bl=True

                elif i == 1:
                    rep += str(self.co[i]) + '{}'.format(str(self.var))
                    bl=True

                elif i > 1:
                    rep += str(self.co[i]) + '{}'.format(str(self.var)) + '^' + str(i)
                    bl = True




        rep = rep.replace('++', '+')
        rep = rep.replace('+-', '-')
        rep = rep.replace('-+', '-')
        rep = rep.replace('--', '+')
        rep=rep.replace('0','')
        rep+=')'
        return str(rep)

    def __eq__(self, other):
        return self.var == other.v and co == other.co

    def __add__(self, other):
        return Addition(self, other)

    def __sub__(self, other):
        return Subtraction(self, other)

    def __mul__(self, other):
        return Multiplication(self, other)

    def __pow__(self, power: float, modulo=None):
        if type(power) is not float:
            try:
                a = float(power)

            except:
                raise ValueError
            if type(a) is not float:
                raise ValueError
            else:
                return Power(Power(self, a))
        else:
            return Power(Power(self, power))

    def NR_evaluate(self, assgms: Assignments, epsilon: int = 0.0001, times: int = 100):

        pass
    # TODO complete all Expression interface methods

