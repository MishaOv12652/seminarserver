import re
import types
import string


class ReqRes(object):

    def __init__(self, data):
        self.data = data

    def handle_math_string_exp(self, sand_box):
        banned_commands = {
            'exec': 'exec',
            'eval': 'eval',
            'import': 'import',
            'type': 'type'
        }
        for key, value in banned_commands.iteritems():
            if re.search(value, self.data) is not None:
                return 'you tried to use a banned command ' + str(value)
        # if re.search('type', self.data) is not None:
        #     if self.handle_num_args() > 1:
        #         return 'you are trying to use type method to create a class dynamically, this is not allowed!'
        try:
            result = eval(str(self.data), sand_box)
        except (ValueError, NameError, SyntaxError, ZeroDivisionError, KeyError) as e:
            result = 'Error:' + str(e)
        return str(result)

    def handle_print(self):
        print_exp = re.search("print", str(self.data))
        return self.data[print_exp.end():]

    def handle_num_args(self):
        l_bracket = re.search('\(', str(self.data))
        r_bracket = re.search('\)', str(self.data))
        args_string = self.data[l_bracket.start() + 1:r_bracket.end() - 1]
        args = []
        for x in args_string.split(','):
            args.append(x.strip)
        return len(args)

    def handle_function(self, sand_box):
        colons = re.search(":", str(self.data))
        def_exp = re.search("def", str(self.data))
        if def_exp is None:
            return eval(compile(self.data, '<string>', 'eval'), sand_box)
        else:
            num_of_args = self.handle_num_args()
            if num_of_args > 1:
                func_name = self.data[def_exp.end() + 1:colons.start() - (2 * num_of_args + 1)]
            else:
                func_name = self.data[def_exp.end() + 1:colons.start() - num_of_args - 1]
            exec self.data in sand_box
            if callable(sand_box[func_name]):
                print_search = re.search('print', self.data)
                if print_search is None:
                    if num_of_args > 1:
                        return "This Function Has Arguments Please Call The Function " + str(
                            sand_box[func_name].__name__)
                    else:
                        return sand_box[func_name]()
                else:
                    return self.handle_print()
            else:
                return self.handle_print()

    def handle_class(self, sand_box):
        class_word_remove = re.search("class", str(self.data))
        colons = re.search(":", str(self.data))
        class_name = self.data[class_word_remove.end() + 1:colons.start() - 2]
        atrr_dict = self.handle_class_inner_attr(str(self.data)[colons.end():])
        meth_dict = self.handle_class_inner_func(str(self.data)[colons.end():], sand_box)
        class_dict = atrr_dict.copy()
        if meth_dict is not None:
            class_dict.update(meth_dict)
        dyn_class = type(class_name, (object,), class_dict)
        sand_box[class_name] = dyn_class
        globals()[class_name] = None
        locals()[class_name] = None
        return sand_box[class_name]

    def handle_class_inner_attr(self, min_str):
        atrr_dict = {}
        init_func = re.search('__init__', min_str)
        if init_func is not None:
            fin_of_init_func = re.search(':', min_str)
            min_str = min_str[fin_of_init_func.end():]
        def_exp = re.search("def", min_str)
        if def_exp is not None:
            min_str = min_str[:def_exp.start()]
        for atr in min_str.split():
            if re.search("def", atr) is None:
                if re.search('self.', atr):
                    atrr_dict.update({atr.split('=')[0].replace('self.', ''): atr.split('=')[1]})
                else:
                    atrr_dict.update({atr.split('=')[0]: atr.split('=')[1]})
        return atrr_dict

    def handle_class_inner_func(self, min_str, sand_box):
        func_dict = {}
        def_exp = re.search("def", min_str)
        if def_exp is not None:
            min_str = min_str[def_exp.start():]
            for atr in min_str.split("def"):
                if atr is not '':
                    l_brackets = re.search("\(", atr)
                    self.data = "def" + str(atr)
                    if re.search('\n', self.data) is not None:
                        self.data = string.replace(self.data, '\n', '')
                    exec self.data in sand_box
                    func_name = atr[1:l_brackets.start()]
                    func_dict.update({func_name: sand_box[func_name]})
            return func_dict

    def handle_class_calls(self, sand_box):
        equal_sign = re.search('=', self.data)
        dot_sign = re.search('\.', self.data)
        left_bracket = re.search('\(', self.data)
        if equal_sign is not None:
            if re.search('\{', self.data) is not None and re.search(
                    '\}', self.data) is not None:
                exec self.data in sand_box
                return sand_box[self.data[0:equal_sign.start()]]
            elif self.data[equal_sign.end() + 1:left_bracket.start()] in sand_box.keys():
                exec self.data in sand_box
                return sand_box[self.data[:equal_sign.start() - 1]]
            else:
                return "illegal expression"
        elif dot_sign is not None:
            if self.data[:dot_sign.start()] in sand_box.keys():
                if hasattr(sand_box[self.data[:dot_sign.start()]], self.data[dot_sign.end():]):
                    return getattr(sand_box[self.data[:dot_sign.start()]], self.data[dot_sign.end():])
                elif left_bracket is not None and hasattr(sand_box[self.data[:dot_sign.start()]],
                                                          self.data[dot_sign.end():left_bracket.start()]):
                    return sand_box[self.data[dot_sign.end():left_bracket.start()]]()
                else:
                    return "The Object has No such attribute or function " + self.data[dot_sign.end():]
            else:
                return "illegal expression"

    def process_req(self, sand_box):
        if re.search('\n', self.data) is not None:
            self.data = string.replace(self.data, '\n', '')
        if re.search('import', self.data) is not None:
            return "you are trying to import a module, access is denied!"
        elif re.search("class", str(self.data)) is not None or isinstance(sand_box.get(str(self.data)),
                                                                          types.ClassType):
            return self.handle_class(sand_box)
        elif re.search("def", str(self.data)) is not None or isinstance(sand_box.get(str(str(self.data).split('(')[0])),
                                                                        types.FunctionType):
            return self.handle_function(sand_box)
        elif re.search("print", str(self.data)) is not None:
            return self.handle_print()
        elif re.search('=', self.data) is not None or re.search('\.', self.data) is not None:
            return self.handle_class_calls(sand_box)
        else:
            return self.handle_math_string_exp(sand_box)
