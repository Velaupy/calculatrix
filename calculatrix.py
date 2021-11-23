import string,decimal

decimal.getcontext().clear_traps()

Deci = decimal.Decimal

ismain = __name__ == "__main__"

numbers = list(string.digits)
symbols = ["+","-","*","/","%","."]

filter = {
    "()" : "",
    ")(" : "",
    #"//0" : "",
    #"/0" : "",
    #"%0" : "",
}

for num in numbers:
    filter[")" + num] = num
    filter[num + "("] = num
    for symbol in symbols:
        if symbol != ".":
            filter[symbol + "0" + num] = symbol + num
            filter[symbol + "." + num] = symbol + "0." + num

for symbol in symbols:
    filter["(" + symbol + ")"] = symbol
    filter[symbol + ")"] = ")"
    if symbol != "-":
        filter["(" + symbol] = "("
    if symbol == ".":
        filter[")" + symbol + "("] = symbol
        filter[")" + symbol] = symbol
        filter[symbol + "("] = symbol
    for symbol2 in symbols:
        if (symbol == "*" and symbol2 == "*") or (symbol == "/" and symbol2 == "/"):
            continue
        filter[symbol + symbol2] = symbol
        filter[symbol2 + symbol] = symbol2

def math(orgarg : str):
    orgarg = str(orgarg)
    pr = 0
    arg = orgarg
    if arg and any(char for char in arg if char.isdigit()):
        def removewastefromarg():
            nonlocal arg
            arg = arg.replace("×","*")
            arg = arg.replace("÷","/")
            arg = arg.replace(":","/")
            arg = arg.replace("^","**")
            arg = "".join([var for var in arg if var in (numbers + symbols + ["(",")"])])
        removewastefromarg()
        lastarg = ""
        while True:
            #print()
            #print("arg currently: " + arg)
            lastarg = arg
            removewastefromarg()
            def removeindex(index : int):
                nonlocal arg
                arg = arg[:index] + " " + arg[index+1:]
            if arg[0] == "0":
                for index,char in enumerate(arg):
                    if char == "0" and arg[index+1].isdigit():
                        removeindex(index)
                    else:
                        break
            while arg[0] in symbols:
                if arg[0] == "." and arg[1].isdigit():
                    arg = "0" + arg
                for symbol in symbols:
                    arg = arg.removeprefix(symbol)
            while arg[-1] in symbols:
                for symbol in symbols:
                    arg = arg.removesuffix(symbol)
            for var in filter:
                while var in arg:
                    arg = arg.replace(var,filter.get(var))
            parenthese_starts = []
            filtered_parentheses_ends = []
            for index,char in enumerate(arg):
                if char == "(":
                    parenthese_starts.append(index)
                end = len(arg)-1
                if char in symbols:
                    if char == ".":
                        for index2 in range(index+1,end):
                            char2 = arg[index2]
                            if char2 == char:
                                removeindex(index2)
                            elif not char2.isdigit():
                                break
                    if index != end and (char == "*" or char == "/") and arg[index+1] == char:
                        start = index+2
                        for index2 in range(start,end):
                            if arg[index2] == char:
                                removeindex(index2)
                            else:
                                break
                if index != end and char == "0" and arg[index+1].isdigit() and (not arg[index-1].isdigit() and arg[index-1] != "."):
                    removeindex(index)
            parenthese_starts.sort()
            if (not parenthese_starts):
                arg = arg.replace(")","")
            else:
                #print("parentheses starts: " + str(parenthese_starts))
                for parenthese_start in reversed(parenthese_starts):
                    #print("current parenthese start: " + str(parenthese_start))
                    parenthese_end = arg.index(")",parenthese_start) if arg.find(")",parenthese_start) != -1 else None
                    if not parenthese_end:
                        #print("no parenthese end found at all")
                        removeindex(parenthese_start)
                        continue
                    while parenthese_end in filtered_parentheses_ends:
                        parenthese_end = arg.index(")",parenthese_end+1) if arg.find(")",parenthese_end+1) != -1 else None
                        if not parenthese_end:
                            #print("no parenthese end found (loop)")
                            removeindex(parenthese_start)
                            break
                    if parenthese_end:
                        filtered_parentheses_ends.append(parenthese_end)
                #print("filtered parentheses ends: " + str(filtered_parentheses_ends))
                for index,char in enumerate(arg):
                    if char == ")" and not index in filtered_parentheses_ends:
                        removeindex(index)
            removewastefromarg()
            if lastarg == arg:
                break

        while True:
            nondecifound = False
            for index,char in enumerate(arg):
                if char.isdigit():
                    #print()
                    end = len(arg)-1
                    #print(f"arg: {arg}")
                    #print(f"({char}) index: {str(index)}")
                    #print()
                    #print("arg[:index]: " + arg[:index])
                    if not arg[:index].endswith("Deci("):
                        #print("doesn't end with Deci(")
                        previndex = index-1
                        if previndex != -1 and (arg[previndex].isdigit() or arg[previndex] == "."):
                            continue
                        nondecifound = True
                        #print("index to end: " + arg[index:])
                        #print()
                        if index != end:
                            for index2 in range(index,end+1):
                                #print("index2: " + str(index2))
                                #print("end: " + str(end))

                                #print("char2 isn't a number: " + str(not arg[index2].isdigit()))
                                #print("index2 == end: " + str(index2 == end))
                                if not arg[index2].isdigit() and arg[index2] != ".":
                                    arg = arg[:index] + "Deci(" + arg[index:index2] + ")" + arg[index2:]
                                    break
                                if index2 == end:
                                    arg = arg[:index] + "Deci(" + arg[index:len(arg)] + ")"
                        else:
                            arg = arg[:index] + "Deci(" + arg[end] + ")"
                        break
                    #else:
                        #print("ends with Deci(")
            if not nondecifound:
                break
        pr = str(eval(arg))
    if ismain:
        print()
        print(f"given result: {orgarg}")
        print()
        print(f"filtered result: {arg}")
        print()
        print(f"calculated end result: {pr}")
        print()
        print("-" * 100)
    else:
        return pr

"""
import random

lst : list = None

while True:
    lst = list(string.printable * random.randint(1,10))
    random.shuffle(lst)
    st = "".join(lst)
    math(st)
"""

while ismain:
    math(input("enter math: "))
