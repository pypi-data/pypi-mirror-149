
from heapq import heappop, heappush


class PathfinderError(Exception): pass

class DublicateError(PathfinderError): pass

class PathError(PathfinderError): pass

class LowComby:
    def __init__(self) -> None:
        self.list = []
        self.set = set()
    
    def __getitem__(self, index):
        return self.list[index]
    
    def __setitem__(self, index: int, obj):
        self.list[index] = obj
        self.set.add(obj)
    
    def __len__(self):
        return len(self.list)
    
    def __contains__(self, obj):
        return obj in self.set
    
    def copy(self):
        lc = LowComby()
        lc.list = self.list.copy()
        lc.set = self.set.copy()
        return lc
    
    def append(self, obj):
        self.list.append(obj)
        self.set.add(obj)
    
    def insert(self, index: int, obj):
        self.list.insert(index, obj)
        self.set.add(obj)
    
    def pop(self, index):
        r = self.list.pop(index)
        self.set.pop(r)
        return r
    
    def sort(self, key=None):
        if key is None:
            key = lambda x: x.cost
        self.list.sort(key=key)

class HighComby(LowComby):
    def __getitem__(self, index):
        if index < 0 or index >= len(self.list):
            raise ValueError("index out of bounds")
        return super().__getitem__(index)
    
    def __setitem__(self, index: int, obj):
        if obj in self.set and self.list[index] != obj:
            raise DublicateError("object already exists")
        if index < 0 or index >= len(self.list):
            raise IndexError("index out of bounds")
        if not hasattr(obj, "__hash__"):
            raise TypeError("object can't be hashed")
        super().__setitem__(index, obj)
    
    def append(self, obj):
        if obj in self.set:
            raise DublicateError("object already exists")
        if not hasattr(obj, "__hash__"):
            raise TypeError("object can't be hashed")
        super().append(obj)
    
    def insert(self, index: int, obj):
        if obj in self.set and self.list[index] != obj:
            raise DublicateError("object already exists")
        if index < 0 or index >= len(self.list):
            raise IndexError("index out of bounds")
        if not hasattr(obj, "__hash__"):
            raise TypeError("object can't be hashed")
        
        super().insert(index, obj)
    
    def pop(self, index):
        try:
            r = self.list.pop(index)
            self.set.pop(r)
            return r
        except IndexError as e:
            raise IndexError("out of bounds") from e
        except KeyError as e:
            raise PathfinderError("set didn't contain item") from e

def get_pop(queue):
    return heappop if isinstance(queue, list) else lambda x: heappop(x.list)

def get_push(queue):
    return heappush if isinstance(queue, list) else lambda x,n: heappush(x.list, n)
