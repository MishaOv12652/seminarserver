import re


class ReqRes(object):

    def __init__(self, data):
        self.data = data

    def handle_math_string_exp(self):
        result = eval(str(self.data))
        print(result)
        return str(result)

    def handle_print(self):
        print_exp = re.search("print", str(self.data))
        return self.data[:print_exp.start()] + self.data[print_exp.end():]

    def handle_num_args(self):
        l_bracket = re.search('\(', str(self.data))
        r_bracket = re.search('\)', str(self.data))
        args_string = self.data[l_bracket.start() + 1:r_bracket.end() - 1]
        args = []
        for x in args_string.split(','):
            args.append(x.strip)
        return len(args)

    def handle_function(self):
        colons = re.search(":", str(self.data))
        def_exp = re.search("def", str(self.data))
        func_name = self.data[def_exp.end() + 1:colons.start()]
        exec str(self.data)
        if eval(str(func_name)) is not None:
            return eval(str(func_name))
        else:
            return self.handle_print()

    def handle_class(self):
        class_word_remove = re.search("class", str(self.data))
        colons = re.search(":", str(self.data))
        class_name = self.data[class_word_remove.end() + 1:colons.start()]
        dynamic_class = type(class_name, (), {"f_name": "Misha"})
        return dynamic_class

    def handle_class_inner_attr(self):
        return "m"

    def handle_class_inner_func(self):
        return "m"

    def process_req(self):
        if re.search("class", str(self.data)) is not None:
            return self.handle_class()
        elif re.search("def", str(self.data)) is not None:
            return self.handle_function()
        elif re.search("print", str(self.data)) is not None:
            return self.handle_print()
        else:
            return self.handle_math_string_exp()


def main():
    print (ReqRes('"Misha"').process_req())
    print (ReqRes('2+2').process_req())
    print (ReqRes('print "Hi, I am Hungry" ').process_req())
    print (ReqRes('def Hi(): print("Hi, I am Misha")').process_req())
    print (ReqRes('class Misha(object): fName = "Misha"').process_req())
    print (ReqRes('class Misha(): fName = "Misha"').process_req().f_name)
    print (ReqRes('def add(x,y,a,p): return x+y').handle_args())


if __name__ == '__main__':
    main()
