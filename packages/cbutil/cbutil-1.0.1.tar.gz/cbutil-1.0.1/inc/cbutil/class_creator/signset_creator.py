from copy import copy
#00 01 10 11

sign_table_ = [
    [0,0,0,1],   #|
    [0,1,1,1],   #&
    [1,1,0,0],   #-
    [1,0,0,1]    #^
]

op_table_ = [
    [lambda a,b: a&b, lambda a,b: b-a,  lambda a,b: a-b, lambda a,b: a|b,],   #|
    [lambda a,b: a|b, lambda a,b: a-b,  lambda a,b: b-a, lambda a,b: a&b,],   #&
    [lambda a,b: b-a, lambda a,b: a&b,  lambda a,b: a|b, lambda a,b: a-b,],   #-
    [lambda a,b: a^b, lambda a,b: a^b,  lambda a,b: a^b, lambda a,b: a^b,],   #^
    [lambda a,b: b<a, lambda a,b: len(a&b)==0, lambda a,b: False, lambda a,b: a<b],    #<
    [lambda a,b: b<=a, lambda a,b: len(a&b)==0, lambda a,b: False, lambda a,b: a<=b],    #<=
]

iop_table_ = [
    [lambda a,b: a.__iand__(b), lambda a,b: b.__isub__(a),  lambda a,b: a.__isub__(b), lambda a,b: a.__ior__(b),],  #|=
    [lambda a,b: a.__ior__(b), lambda a,b: a.__isub__(b),  lambda a,b: b.__isub__(a), lambda a,b: a.__iand__(b),],  #&=
    [lambda a,b: b.__isub__(a), lambda a,b: a.__iand__(b),  lambda a,b: a.__ior__(b), lambda a,b: a.__isub__(b),],  #-=
    [lambda a,b: a.__ixor__(b), lambda a,b: a.__ixor__(b),  lambda a,b: a.__ixor__(b), lambda a,b: a.__ixor__(b),]  #^=
]

def _aux1(table):
    return [[arr[0:2], arr[2:4]] for arr in table]

sign_table = _aux1(sign_table_)
op_table = _aux1(op_table_)
iop_table = _aux1(iop_table_)

def create_signset(set_cls):
    def _op_gen(tb_idx):
        def f(self, x):
            funcs, signs = op_table[tb_idx], sign_table[tb_idx]
            a,b = self._data,x._data
            m,n = self.sign,x.sign
            ret = SignSet(sign = signs[m][n])
            ret._data = funcs[m][n](a,b)
            return ret            
        return f

    def _iop_gen(tb_idx):
        def f(self, x):
            funcs, signs = iop_table[tb_idx], sign_table[tb_idx]
            a,b = self._data,x._data
            m,n = self.sign,x.sign
            funcs[m][n](a,b)
            self.sign = signs[m][n]
            return self
        return f

    def _cmp_op_gen(tb_idx):
        def f(self, x):
            funcs = op_table[tb_idx]
            a,b = self._data,x._data
            m,n = self.sign,x.sign
            return funcs[m][n](a,b)
        return f  
                        
    _op_impls = list(map(_op_gen, range(4)))
    _iop_impls = list(map(_iop_gen, range(4)))
    _cmp_op_impls = list(map(_cmp_op_gen, (4,5)))

    class SignSet:
        def __init__(self, *args ,sign = 1):
            self.sign = sign
            self._data = set_cls(*args)

        def __or__(self,x):
            return _op_impls[0](self,x)

        def __and__(self,x):
            return _op_impls[1](self,x)

        def __sub__(self,x):
            return _op_impls[2](self,x)

        def __xor__(self,x):
            return _op_impls[3](self,x)

        def __ior__(self,x):
            return _iop_impls[0](self,x)

        def __iand__(self,x):
            return _iop_impls[1](self,x)

        def __isub__(self,x):
            return _iop_impls[2](self,x)

        def __ixor__(self,x):
            return _iop_impls[3](self,x)

        def __lt__(self,x):
            return _cmp_op_impls[0](self,x)

        def __le__(self,x):
            return _cmp_op_impls[1](self,x)

        def __gt__(self,x):
            return x<self

        def __ge__(self,x):
            return x>=self

        def __eq__(self,x):
            return self.sign == x and self._data == x._data
        
        def __neq__(self,x):
            return not (self == x)

        def __neg__(self):
            ret = self.copy()
            ret.neg_self()
            return ret

        def __contains__(self,x):
            return self.sign == (x in self._data)

        def copy(self):
            return copy(self)

        def neg_self(self):
            self.sign = not self.sign

        def is_empty(self):
            return (not self.sign) or (len(self._data) == 0)

        def clear(self):
            self.sign = 1
            self._data.clear()

        def add(self,x):
            return self._data.add(x)

        def remove(self,x):
            return self._data.remove(x)

        def discard(self, x):
            return self._data.discard(x)

        def to_str(self, ts = str):
            s = ts(self._data)
            if not self.sign: s = '-'+s
            return s

        def __str__(self):
            return self.to_str()

        def __repr__(self):
            return self.to_str(repr)

    return SignSet