import os
from collections.abc import Iterable
from random import random
	
def cls():
	os.system('cls')
	
def is_iterable(x):
    attrs = ['__next__', '__iter__']
    if any(map(lambda a: hasattr(x,a), attrs)):
        return True

def make_plain_impl(x, ty):
    if not is_iterable(x):return [x]
    t = []
    for x0 in x:
        ty0 = type(x0)
        if ty0 == ty:
            t+=make_plain_impl(x0,ty)
        elif is_iterable(x0):
            t.append(make_plain(x0,ty))
        else:
            t.append(x0)
    return t

def make_plain(x, ty):
    if not is_iterable(x):return x
    tyx = type(x)
    if tyx != ty: return tyx(map(lambda x: make_plain(x,ty), x))
    ret = []
    for x0 in x:
        if type(x0) == ty:
            ret+=make_plain_impl(x0,ty)
        else:
            ret.append(x0)
    return tyx(ret)

def make_plain_self_impl(x):
    if not is_iterable(x):return [x]
    tyx = type(x)
    ret = []
    for x0 in x:
        if type(x0) == tyx:
            ret+=make_plain_self_impl(x0)
        elif is_iterable(x0):
            ret.append(make_plain_self(x0))
        else:
            ret.append(x0)
    return ret

def make_plain_self(x):
    if not is_iterable(x):return x
    tyx = type(x)
    ret = []
    for x0 in x:
        if type(x0) == tyx:
            ret+=make_plain_self_impl(x0)
        elif is_iterable(x0):
            ret.append(make_plain_self(x0))
        else:
            ret.append(x0)
    return tyx(ret)


def bisect_right(a, x, lo=0, hi=None, key=None):
    if hi == None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        midv = a[mid]
        if x < key(midv):
            hi = mid
        else:
            lo = mid + 1
    return lo


def bisect_left(a, x, lo=0, hi=None, key=None):
    if hi == None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        midv = a[mid]
        if key(midv) < x:
            lo = mid+1
        else:
            hi = mid
    return lo

def is_empty(x):
    return len(x) == 0

import heapq
from more_itertools import first as get_one

def get_min_gap_num(l:list, min_val:int = 1):
    if not len(l):
        return min_val
    heapq.heapify(l)
    v = heapq.heappop(l)
    if v>min_val:
        return min_val
    while len(l):
        v+=1
        u = heapq.heappop(l)
        if u != v:
            return v
    return v+1

def get_unique_name(name:str, src):
    if name not in src:
        return name
    d_nums = []
    for x in src:
        if f'{name}_' == f'{x[0:len(name)]}_':
            try: 
                d_num = int(x[len(name)+1: ])
            except ValueError:
                continue
            d_nums.append(d_num)
    uq_num = get_min_gap_num(d_nums,1)
    return f'{name}_{uq_num}'