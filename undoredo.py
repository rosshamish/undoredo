"""
module undoredo provides undo/redo functionality for arbitrary classes.

See README.md for a detailed usage example.
"""
import logging

__author__ = 'Ross Anderson <ross.anderson@ualberta.ca>'
__version__ = '0.1.2'


class UndoManager(object):
    """
    class UndoManager manages a stack of Command objects for the purpose of
    implementing undo/redo functionality.

    Usage:
        undo_mgr = UndoManager()
        undo_mgr.do(Command(params...))
        if undo_mgr.can_undo():
            undo_mgr.undo()
        if undo_mgr.can_redo():
            undo_mgr.redo()
    """
    def __init__(self):
        self._undo_stack = list()
        self._redo_stack = list()

    def do(self, command):
        self._redo_stack.clear()
        self._undo_stack.append(command)
        result = command.do()
        logging.debug('{}.do() called, stack now={}'.format(type(command), self._undo_stack))
        return result

    def can_undo(self):
        return len(self._undo_stack) > 0

    def can_redo(self):
        return len(self._redo_stack) > 0

    def undo(self):
        if len(self._undo_stack) < 1:
            raise Exception('Cannot perform undo, undo stack is empty')
        command = self._undo_stack.pop()
        self._redo_stack.append(command)
        result = command.undo()
        logging.debug('{}.undo() called, undo stack now={}'.format(type(command), self._undo_stack))
        return result

    def redo(self):
        if len(self._redo_stack) < 1:
            raise Exception('Cannot perform redo, redo stack is empty')
        command = self._redo_stack.pop()
        self._undo_stack.append(command)
        result = command.do()
        logging.debug('{}.redo() called, redo stack now={}'.format(type(command), self._redo_stack))
        return result


class Command(object):
    """
    A Command wraps a method call in an object which can do() and undo(). It's used with UndoManager.
    """
    def __init__(self, obj, do_method, *args):
        """
        Create a Command by passing an object, a method to call on the object, and a variable number
        of arguments to pass to the method.

        The object must support methods .copy() and .restore(obj).
        - copy() returns a copy of the object
        - restore(obj) restores the calling object to the state of the passed object

        These methods allow undo to work properly.

        :param obj: object to call the method on
        :param do_method: method to call
        :param args: arguments to pass to the method
        :return: Command object representing the method call
        """
        assert(hasattr(obj, 'copy'))
        assert(hasattr(obj, 'restore'))
        self.obj = obj
        self.do_method = do_method
        self.args = list(args)

        self.restore_point = None

    def do(self):
        """
        Set a restore point (copy the object), then call the method.
        :return: obj.do_method(*args)
        """
        self.restore_point = self.obj.copy()
        return self.do_method(self.obj, *self.args)

    def undo(self):
        """
        Restore the object to the restore point created during do()
        :return: obj.restore(restore_point)
        """
        return self.obj.restore(self.restore_point)


def undoable(method):
    """
    Decorator undoable allows an instance method to be undone.

    It does this by wrapping the method call as a Command, then calling self.do() on the command.

    Classes which use this decorator should implement a do() method like such:

        def do(self, command):
            return self.undo_manager.do(command)
    """
    def undoable_method(self, *args):
        return self.do(Command(self, method, *args))
    return undoable_method


