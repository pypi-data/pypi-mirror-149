from collections.abc import Iterable
from collections import deque

from .util import is_iterable



#begin impl

def dfs1(n):
    '''
    example:
    list(dfs1([1,[2,3],4,[5],6])) == [1, 2, 3, 4, 5, 6]
    '''
    if(not is_iterable(n)):
        yield n
    else:
        for n_ in n:
            yield from dfs1(n_)


def dfs2(n, is_leaf):
    '''
    exmaple:
    list(dfs2(['01', ['02','03'], '04', ['05'], '06'], lambda n: type(n) == str)) 
    == ['01', '02', '03', '04', '05', '06']
    '''
    if is_leaf(n):
        yield n
    else:
        for n_ in n:
            yield from dfs2(n_, is_leaf)

def dfs3(n, get_sons):
    '''
    example:
    dfs([1, [2, 3], 4, [5], 6], reversed)) == [6, 5, 4, 3, 2, 1]
    '''
    if(not is_iterable(n)):
        yield n
    else:
        for n_ in get_sons(n):
            yield from dfs3(n_, get_sons)


def dfs4(n, get_sons, is_leaf):
    '''
    example:
    (list(dfs(['01', ['02', '03'], '04', ['05'], '06'], reversed, lambda n: type(n) == str)) 
    == ['06', '05', '04', '03', '02', '01']
    '''
    if(is_leaf(n)):
        yield n
    else:
        for n_ in get_sons(n):
            yield from dfs4(n_, get_sons, is_leaf)



def bfs1(n):
    q = deque()
    q.append(n)

    while len(q):
        for n_ in q.popleft():
            if is_iterable(n_):
                q.append(n_)
            else:
                yield n_

def bfs2(n, is_leaf):
    q = deque()
    q.append(n)

    while len(q):
        for n_ in q.popleft():
            if is_leaf(n_):
                yield n_
            else:
                q.append(n_)


def bfs3(n, get_sons):
    q = deque()
    q.append(n)

    while len(q):
        for n_ in get_sons(q.popleft()):
            if is_iterable(n_):
                q.append(n_)
            else:
                yield n_


def bfs4(n, get_sons, is_leaf):
    q = deque()
    q.append(n)

    while len(q):
        for n_ in get_sons(q.popleft()):
            if is_leaf(n_):
                yield n_
            else:
                q.append(n_)
#end impl


def dfs(n, get_sons = None, is_leaf = None):
    '''
    depth first search by preorder
    example:
    (list(dfs(['01', ['02', '03'], '04', ['05'], '06'], reversed, lambda n: type(n) == str)) 
    == ['06', '05', '04', '03', '02', '01']
    '''
    if get_sons is None and is_leaf is None:
        yield from dfs1(n)
    elif get_sons is None:
        yield from dfs2(n, is_leaf)
    elif is_leaf is None:
        yield from dfs3(n, get_sons)
    else:
        yield from dfs4(n, get_sons, is_leaf)



def bfs(n, get_sons = None, is_leaf = None):
    if get_sons == None and is_leaf == None:
        yield from bfs1(n)
    elif get_sons == None:
        yield from bfs2(n, is_leaf)
    elif is_leaf == None:
        yield from bfs3(n, get_sons)
    else:
        yield from bfs4(n, get_sons, is_leaf)




class TreeIter:
    '''
    search with record of path
    '''
    def __init__(self, root, get_sons = iter, is_leaf = lambda x: not is_iterable(x)):
        self.path = [root]
        self.get_sons = get_sons
        self.is_leaf = is_leaf

    @property
    def root(self):
        '''firt node of path'''
        return self.path[0]

    @root.setter
    def root(self,x):
        self.path[0] = x

    @property
    def cur(self):
        '''last node of path'''
        return self.path[-1]

    @cur.setter
    def cur(self,x):
        self.path[-1] = x

    @property
    def deepth(self):
        '''deepth of current path'''
        return len(self.path) -1


    def dfs(self):
        '''dfs preorder'''
        cur = self.cur
        is_leaf = self.is_leaf
        yield cur
        if is_leaf(cur):
            return

        path = self.path
        get_sons = self.get_sons
        path.append(None)
        for n in get_sons(cur):
            path[-1] = n
            yield from self.dfs()
        path.pop()

    def bfs(self):
        cur = self.cur
        is_leaf = self.is_leaf
        get_sons = self.get_sons
        path = self.path
        yield cur
        if is_leaf(cur):
            return

        q = deque()
        q.append(cur)
        prnt_num = 1
        sons_num = 0
        path.append(None)
        while len(q):
            for n_ in get_sons(q.popleft()):
                sons_num+=1
                cur = n_
                yield n_
                if is_leaf(n_):
                    continue
                else:
                    q.append(n_)
            prnt_num-=1
            if prnt_num == 0:
                # next level
                prnt_num = sons_num
                sons_num = 0
                path.append(None)
        self.path = path[0:]
            


__all__ = ['dfs', 'bfs','TreeIter']