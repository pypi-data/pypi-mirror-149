#-*-conding:utf-8-*-
import os
import pathlib
import shutil
from zipfile import ZipFile

import chardet

# from .pbar import file_proc_bar
from .util import get_unique_name
# from itertools import chain

_Path = type(pathlib.Path(''))


class Path(_Path):
    _Path = _Path

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            p = args[0]
            if type(p) == Path:
                return p
        return super().__new__(cls, *args, **kwargs)

    @staticmethod
    def setcwd(path):
        os.chdir(path)
    
    @staticmethod
    def getcwd():
        return os.getcwd()

    @property
    def prnt(self):
        return Path(super().parent)

    @property
    def ext(self):
        return super().suffix[1:]

    @property
    def size(self):
        return self.stat().st_size
    
    @property
    def rsize(self):
        '''real size'''
        return self.stat().st_rsize

#begin iter

    def get_son_iter(self, *filters):
        if self.is_dir():
            if len(filters) == 0:
                return super().iterdir()
            return filter(lambda x: all(map(lambda f: f(x), filters)), super().iterdir())
        else:
            return iter([])

    def get_file_son_iter(self, *filters):
        return self.get_son_iter(Path.is_file, *filters)

    def get_dir_son_iter(self, *filters):
        return self.get_son_iter(Path.is_dir, *filters)

    def get_sibling_iter(self, *filters):
        return self.prnt.get_son_iter(lambda x: x!=self, *filters)

    @property
    def son_iter(self):
        return self.get_son_iter()

    @property
    def sibling_iter(self, *filters):
        return self.get_sibling_iter()

    @property
    def file_son_iter(self):
        return self.get_file_son_iter()

    @property
    def dir_son_iter(self):
        return self.get_dir_son_iter()

    @property
    def sons(self):
        return list(self.son_iter)
    
    @property
    def siblings(self):
        return list(self.sibling_iter)

    @property
    def file_sons(self):
        return list(self.file_son_iter)

    @property
    def dir_sons(self):
        return list(self.dir_son_iter)
#end iter


    @property
    def str(self):
        return self.__str__()

    @property
    def quote(self):
        if Path._Path == pathlib.WindowsPath:
            s = self.str.replace('"', r'\"')
            return f'"{s}"'

    def rel_to(self,path):
        return super().relative_to(path)

    def open(self,mode, buffering=-1, encoding=None, *args, **kwargs):
        if not self.prnt.exists():
            self.prnt.mkdir()
        if encoding == None:
            if mode in ('r','r+','rw'):
                with super().open('rb',buffering) as fr:
                    encoding = chardet.detect(fr.read(512))['encoding']
                    if encoding == 'ascii':
                        encoding = 'UTF-8'
        return super().open(mode,buffering, encoding,*args,**kwargs)
    
    def mkdir(self, *args, overwrite =False, parents =True, **kwargs):
        '''
        默认文件夹不存在则忽略，会自动创建不存在的父路径
        '''
        if self.exists():
            if overwrite:
                self.remove()
                super().mkdir(*args, parents=parents, **kwargs)
        else:
            super().mkdir(*args, parents=parents, **kwargs)

    def remove(self):
        if self.exists():
            if self.is_dir():
                shutil.rmtree(self.to_str())
            else:
                os.remove(self.to_str())

    def remove_sons(self):
        assert(self.is_dir())
        for son in self.son_iter:
            son.remove()
    
    def to_str(self):
        return str(self)

    def copy_to(self, dst, is_prefix = False, overwrite = True):
        '''
        会自动创建当前不存在的父目录
        
        若is_prefix == False:
        将该路径复制，复制后的路径为dst
        若is_prefix == True:
        则将该路径复制到dst目录下，复制后的名字不变
        
        若路径为目录，则会递归复制，
        '''
        a = self.to_str()
        if is_prefix:
            b = (Path(dst)/(self.name)).to_str()
        else:
            b = Path(dst).to_str()
        if self.is_dir():
            shutil.copytree(a,b, dirs_exist_ok=overwrite)
        else:
            if overwrite:
                shutil.copyfile(a,b)
            elif b.exists():
                raise FileExistsError()

    def copy_sons_to(self, dst, overwrite = True):
        dst = Path(dst)
        assert(self.is_dir() and dst.is_dir())
        if not dst.exists():
            dst.mkdir()
        for son in self.son_iter:
            son.copy_to(dst/son.name, overwrite=overwrite)

    def move_to(self, dst):
        a = self.to_str()
        b = Path(dst).to_str()
        shutil.move(a,b)

    def make_archive(self, dst, format = None):
        dst = Path(dst)
        if format == None:
            format = dst.detect_format_by_suffix()
            if format == None:
                format = 'zip'
        a = self.absolute().to_str()
        b = dst.absolute().to_str()
        shutil.make_archive(b, format, a)

    def unpack_archive_to(self, dst, format = None):
        if format == None:
            format = self.detect_format_by_suffix()
        a = self.absolute().to_str()
        b = Path(dst).absolute().to_str()
        shutil.unpack_archive(a,b,format)

    def detect_format_by_suffix(self):
        m = {
            'zip' : 'zip',
            'tar' : 'tar',
            'gz' : 'gztar',
            'bz' : 'bztar',
            'xz' : 'xztar'
        }
        ext = self.ext
        if ext:
            format = m.get(ext)
            if format:
                return format
            else:
                return ext
        
    def unzip(self, dst, print=lambda *args:None, show_state=lambda **kwargs:None):
        '''
        show_state(description='', size='', total_size='', total_compress_size='')
        '''
        dst = Path(dst).absolute().to_str()
        zf = ZipFile(self.to_str())
        l = zf.infolist()
        # file_num = len(l)
        # total_size = sum(f.file_size for f in l)
        # total_compress_size = sum(f.compress_size for f in l)
        print(f'Unzip: {self.absolute().to_str()}')
        print(f'Unzip to: {dst}')
        for i,f in enumerate(l):
            zf.extract(f, dst)
            show_state(desc=f'{i}')
            show_state(size=f.compress_size)

    def get_unique_path(self):
        '''
        return a path which is different from its siblings.
        '''
        ext = self.ext
        stem_list = [x.stem for x in self.siblings if x.ext == ext]
        stem = get_unique_name(self.stem, stem_list)
        name = f'{stem}.{ext}'
        return self.prnt/name

    def make_temp_dir(self):
        if self.is_file():
            dir_ = self.prnt
        else:
            dir_ = self
        uqtmp = (dir_/'temp').get_unique_path()
        uqtmp.mkdir()
        return uqtmp

    def remove_temp_sons(self):
        assert(self.is_dir())
        for son in self.sons:
            if son.name.startswith('temp'):
                son.remove()

    def rename_inplace(self, name:str):
        new_path = self.prnt/name
        self.rename(new_path)

    def move_all_sons_to(self, dst):
        for son in self.sons:
            son.move_to(dst)

    def move_all_out(self):
        assert(self.is_dir())
        uq_name = get_unique_name(self.name,[x.name for x in self.son_iter] + [x.name for x in self.siblings])
        if uq_name!=self.name:
            self.rename_inplace(uq_name)
            self = self.prnt/uq_name
        self.move_all_sons_to(self.prnt)
        self.remove()

del _Path
