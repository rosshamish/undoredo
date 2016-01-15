undoredo
--------

undo/redo functionality for arbitrary python classes

Supports Python 3. Might work in Python 2.

> Author: Ross Anderson ([rosshamish](https://github.com/rosshamish))

### Installation

```
pip install undoredo
```

### Usage 

Any class can gain undo/redo functionality by doing the following:

- keep around an instance of UndoManager
- annotate undoable methods with the @undoable decorator
- implement do(), undo(), and redo() methods as shown in the following example
- implement copy(), and restore(obj) methods
  - where copy() returns a copy of the object (probably a deep copy)
  - where restore(obj) restores the calling object to the state of the passed object

### Example

```
import undoredo

class Counter(object):
    def __init__(self, value=0):
        self.undo_mgr = undoredo.UndoManager()
        self.value = value

    @undoredo.undoable
    def increment(self):
        self.value += 1

    @undoredo.undoable
    def decrement(self):
        self.value -= 1

    def do(self, command):
        return self.undo_mgr.do(command)

    def undo(self):
        return self.undo_mgr.undo()

    def redo(self):
        return self.undo_mgr.redo()

    def copy(self):
        return Counter(self.value)

    def restore(self, counter):
        self.value = counter.value

c = Counter(0)  # 0
c.increment()   # 1
c.increment()   # 2
c.undo()        # 1
c.redo()        # 2
```

### License

GPLv3
