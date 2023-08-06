from functools import partial

g_str_len = 0

def compute_length(*args,**kwargs):
    sep = kwargs.get('sep')
    end = kwargs.get('end')
    arg_num = len(args)
    length = 0
    if sep: length+= max(arg_num-1,0)*len(sep)
    if end: length+=len(end)
    length+=sum(map(len,map(str,args)))
    return length

printa = partial(print, end='')

def printr(*args, len=0, **kwargs):
    printa('\r' + ' '*len)
    printa('\r')
    printa(*args, **kwargs)

class InlinePrinter:
    def __init__(self):
        self.is_first = True
        self.cur_len = 0
        
    def get_print_func(self):
        return self.print,self.printa,self.printr
    
    def print(self, *args,**kwargs):
        print(*args,**kwargs)
        self.cur_len = compute_length(*args, **kwargs)

    def printa(self, *args, **kwargs):
        printa(*args,**kwargs)
        self.cur_len = compute_length(*args, **kwargs)

    def printr(self, *args, **kwargs):
        printr(*args, len=self.cur_len,**kwargs)
        self.cur_len = compute_length(*args, **kwargs)


ginline_printer = InlinePrinter()
gprint, gprinta, gprintr = ginline_printer.get_print_func()


__all__ = ['printa', 'printr', 'InlinePrinter', 'gprint', 'gprinta', 'gprintr']