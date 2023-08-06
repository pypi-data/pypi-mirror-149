# from tqdm import tqdm
# from functools import partial

# class tqdmc(tqdm):
#     def __iter__(self):
#         def it_():
#            yield from iter(super())
#            self.close()
#         return it_() 
    

# file_proc_bar = partial(tqdm, unit = 'b', unit_scale = True)


# __all__ = ['file_proc_bar', 'tqdmc']