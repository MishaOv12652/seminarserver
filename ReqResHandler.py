import re
import subprocess


class ReqRes(object):
    dict = {
        'print': 'print',
        'function': 'def',
        'class': 'class',
        'MathExp': 'eval'
    }

    def __init__(self, data):
        self.data = data

    def handleMathExpr(self, req_data):
        result = eval(str(req_data))
        return str(result)

    def handlePrint(self, req_data):
        printS = re.search("print", str(req_data))
        return req_data[:printS.start()] + req_data[printS.end():]

    def handleFunction(self, req_data):
        colons = re.search(":", str(req_data))
        defex = re.search("def", str(req_data))
        funcName = req_data[defex.end() + 1:colons.start()]
        exec req_data
        exec funcName

    def handleClass(self, req_data):
        return "class"

    def process_req(self, req_data):
        if re.search("class", str(req_data)) is not None:
            return self.handleClass(str(req_data))
        elif re.search("def", str(req_data)) is not None:
            return self.handleFunction(str(req_data))
        elif re.search("print", str(req_data)) is not None:
            return self.handlePrint(str(req_data))
        else:
            return self.handleMathExpr(str(req_data))


# def main():
#     print(ReqRes("Misha").process_req("2+2"))
    # ReqResString = ReqRes('"misha"')
    # ReqResMath = ReqRes('5+5')
    # ReqResFun = ReqRes('def Misha(): print("Misha Function")')
    # ReqResPrint = ReqRes('print("Michael")')
    #
    # print(ReqResString.handleMathExpr('"misha"'))
    #
    # print(ReqResMath.handleMathExpr('5+5'))
    #
    # ReqResFun.handleFunction('def Misha(): print("Misha Function")')
    # print(ReqResFun.handleFunction('def MishaMath(): return (2+2)'))
    #
    # print(ReqResPrint.handlePrint('print("Michael")'))
    #
    # print(ReqResMath.handleMathExpr('25*4'))


# if __name__ == '__main__':
#     main()
