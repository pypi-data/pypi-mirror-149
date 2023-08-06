# import requests
# import contextlib
# from .path import Path
# from urllib.parse import urlparse
# from tqdm import tqdm
# from .pbar import file_proc_bar

# def download_bar(iterable, chunk_size = None, total_size = None, exist_size = 0):
#     def bar():
#         with file_proc_bar(total=total_size) as pbar:
#             pbar.update(exist_size)
#             for x in iterable:
#                 yield x
#                 pbar.update(chunk_size)
#     return bar()

# class URL:
#     def __init__(self, url):
#         self.url = url
#         self.o = urlparse(url)

#     def to_str(self, ts = str):
#         return ts(self.url)

#     def __str__(self):
#         return self.to_str(str)

#     def __repr__(self):
#         return self.to_str(repr)

#     @property
#     def path(self):
#         return self.o.path
    
#     @property
#     def name(self):
#         return self.path.split('/')[-1]

#     def download(self, save_path, continuous = False, enable_print = True, enable_bar = True, chunk_size = 4<<10):
#         url = self.url
#         save_path = Path(save_path)
#         r = requests.get(url, stream = True)
#         total_size = int(r.headers['Content-Length'] )
#         exist_size = 0

#         if continuous and save_path.exists():
#             assert(save_path.is_file())
#             exist_size = save_path.size
#             if exist_size:
#                 r.close()
#                 if exist_size == total_size:    #has downloaded
#                     if enable_print:
#                         print(f'Downloading: {url}')
#                         print(f'Save as: {save_path}')
#                         if enable_bar:
#                             with file_proc_bar(total=total_size) as pbar:
#                                 pbar.update(total_size)
#                     return

#                 #redo request
#                 r = requests.get(url, stream = True, headers = {'Range': f'bytes={exist_size}-'})
#                 fw = save_path.open('ab')
#             else:   #none was downloaded
#                 fw = save_path.open('wb')
#         else:
#             save_path.prnt.mkdir()
#             fw = save_path.open('wb')

#         it = r.iter_content(chunk_size=chunk_size)
#         if enable_print: 
#             if enable_bar: 
#                 it = download_bar(it, chunk_size = chunk_size, total_size = total_size, exist_size = exist_size)
#             print(f'Downloading: {url}')
#             print(f'Save as: {save_path}')
#         for data in it:
#             fw.write(data)
#         fw.close()
#         r.close()
            

# __all__ = ['URL']