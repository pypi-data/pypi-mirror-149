import abc
import json
import sys


class MessagePrinter(abc.ABC):

    @abc.abstractmethod
    def print_message(self, key, value):
        pass


class SimpleMessagePrinter(MessagePrinter):

    def __init__(self, show_key: bool, show_msg: bool, filter_empty: bool, output):
        self.show_key = show_key
        self.show_msg = show_msg
        self.filter_empty = filter_empty
        if output is None:
            self.output = sys.stdout
        else:
            self.output = output


    def print_message(self, key, value):
        def print_output(str: str):
            print(str, file=self.output)

        if self.filter_empty:
            if len(value.strip()) == 0:
                return
            try:
                value_obj = json.loads(value)
                if len(value_obj) == 0:
                    return
            except:
                pass

        if self.show_key:
            print_output(key)
            key_len = len(key)
            key_ul = '=' * key_len
            if self.show_msg:
                print_output(key_ul)
        if self.show_msg:
            print_output(value)
        if self.show_key or self.show_msg:
            print_output('')


class JsonMessagePrinter(MessagePrinter):

    def __init__(self, incl: list[str], excl: list[str], printer: MessagePrinter):
        self.simple_printer = printer
        self.incl = incl
        self.excl = excl

    @staticmethod
    def __parse_selector(sel_str: str):
        return Selector(list(sel_str.split('.')))

    def print_message(self, key_str, value_str):
        try:
            value = json.loads(value_str)
        except:
            value = {}

        sel_map = JsonMessagePrinter.__parse_selector

        for excl_str in self.excl:
            try:
                excl_path = sel_map(excl_str)
                excl_path.remove_from(value)
            except:
                pass

        if len(self.incl) == 0:
            self.simple_printer.print_message(key_str, json.dumps(value, indent=4))
        else:
            new_value = {}
            for incl_str in self.incl:
                try:
                    incl_path = sel_map(incl_str)
                    new_value[incl_str] = incl_path.retrieve_from(value)
                except:
                    pass
            self.simple_printer.print_message(key_str, json.dumps(new_value, indent=4))


class IllegalSelectionError(Exception):
    pass


class Selector:

    def __init__(self, path: list[str]):
        self.path = path

    def __retrieve_sel(self, sel: str, obj):
        try:
            if sel in obj:
                return obj[sel]
        except TypeError:
            # sel must be on iterable obj
            raise IllegalSelectionError(f'cannot select from non-iterable object {obj}')

        if isinstance(obj, list):
            # for list, if sel is int, take it
            try:
                int_sel = int(sel)
                if int_sel in obj:
                    return obj[int_sel]
            except ValueError:
                # if sel is not int, sel nested elements
                try:
                    mapped_value = list(map(lambda ele : self.__retrieve_sel(sel, ele), obj))
                    return mapped_value
                except IllegalSelectionError as nested_e:
                    raise IllegalSelectionError('unable to select from list elements ') from nested_e
            except IndexError as i_err:
                raise IllegalSelectionError('unable to select index {sel} from {obj}') from i_err

        raise IllegalSelectionError(f'selection not found in object: {obj}')

    def __remove_sel(self, sel: str, obj):
        # test if selection exists in object
        self.__retrieve_sel(sel, obj)

        if sel in obj:
            del obj[sel]
            return

        if isinstance(obj, list):
            # for list, if sel is int, remove it as index
            try:
                int_sel = int(sel)
                if int_sel in obj:
                    obj.pop(int_sel)
                    return
            except ValueError:
                # if sel is not int, remove sel from nested elements
                for ele in obj:
                    self.__remove_sel(sel, ele)

    def __retrieve_path(self, path: list[str], obj):
        if len(path) == 0:
            return obj
        this_sel = path[0]
        new_obj = self.__retrieve_sel(this_sel, obj)
        return self.__retrieve_path(path[1:], new_obj)

    def __remove_path(self, path: list[str], obj):
        if len(path) < 1:
            raise IllegalSelectionError('cannot remove empty path')

        if len(path) == 1:
            self.__remove_sel(path[0], obj)
            return
        this_sel = path[0]
        next_path = path[1:]
        if this_sel in obj:
            self.__remove_path(next_path, obj[this_sel])
            return

        if isinstance(obj, list):
            # for list, if sel is int, remove remaining path from sel as index
            try:
                int_sel = int(this_sel)
                if int_sel in obj:
                    self.__remove_path(next_path, obj[int_sel])
                    return
            except ValueError:
                # if sel is not int, remove path from nested elements
                for ele in obj:
                    self.__remove_path(path, ele)

    def retrieve_from(self, obj):
        return self.__retrieve_path(self.path, obj)

    def remove_from(self, obj):
        self.__remove_path(self.path, obj)
