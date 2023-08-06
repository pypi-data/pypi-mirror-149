# -*- coding: utf-8 -*-
import os, sys, configparser
from simple_file_user import read, rewrite
from importlib import import_module, invalidate_caches
from . import testRunner

class CLIArgument:
    possibleActions = ("storeValue", "storeTrue", "storeFalse")

    def __init__(self, name: str, description: str, type_: type, choices: list, action: str, default, required, nargs) -> None:
        if not isinstance(name, str):
            raise ValueError("Name argument must be str type.")
        else:
            self.name = name

        if not name.startswith("--") and required:
            raise ValueError("Required argument is not possible for positional argument.")
        else:
            self.required = required

        if description is None:
            self.description = ""
        else:
            self.description = description

        if nargs == "+":
            self.nargs = float("inf")
        elif isinstance(nargs, int):
            self.nargs = nargs
        else: 
            raise Exception("Invalid value for nargs.")
        
        if type_ is None:
            self.type = str
        elif not isinstance(type_, type):
            raise ValueError("Type argument must be type.")
        else:
            self.type = type_

        self.choices = choices

        if action is None:
            self.action = "storeValue"
        elif not action in CLIArgument.possibleActions:
            raise ValueError("Unknown action value.")
        else:
            self.action = action

        self.default = default

        self.value = None

    def setValue(self, value: str = None):
        if self.action == "storeValue":
            if value is None:
                value = self.default
            elif not isinstance(value, self.type):
                value = self.type(value)
            else:
                value = value

            if not self.choices is None:
                if not value in self.choices:
                    raise ValueError("Invalid argument's value.")

        elif self.action == "storeTrue":
            value = True

        elif self.action == "storeFalse":
            value = False


        if self.value is None and self.nargs > 1:
            self.value = [value]

        elif self.value is None and self.nargs == 1:
            self.value = value

        else:
            self.value.append(value)


class ArgumentParser:
    def __init__(self, name: str = None, description: str = None) -> None:
        if name is None:
            self.name = os.path.split(sys.argv[0])[1]
        elif not isinstance(name, str):
            raise TypeError("Name argument must be string.")
        else:
            self.name = name

        if description is None:
            self.description = ""
        elif not isinstance(description, str):
            raise TypeError("Description argument must be string.")
        else:
            self.description = description

        self.arguments = [[]]

    def addArgument(self, name: str, description: str = None, type_: type = str, choices: list = None, action: str = None, group: int = 0, default = None, required: bool = False, nargs=1) -> None:
        self.arguments[group].append(CLIArgument(name, description, type_, choices, action, default, required, nargs))

    def createGroup(self):
        self.arguments.append([])

    def parseArgs(self, args: str = None) -> dict:
        if args is None:
            args = sys.argv[1:]
        
        if "-h" in args or "--help" in args:
            self.__typeHelp()
            sys.exit(0)

        # if "-ch" in args:
        #     self.arguments = [self.arguments[args.index("-ch")+1]]
        # elif "--chooseGroup" in args:
        #     self.arguments = [self.arguments[args.index("--chooseGroup")+1]]

        for positionals, optionals in map(self.__findArgsNames, self.arguments):
            setOptionalValue = False
            setPositionalValue = False
            lastArg = None

            valuedPositionals = {}
            valuedOptionals = {}
            optionalIndex = 0
            positionalIndex = 0
            unknownPositional = None
            unknownOptional = None
            for arg in args:
                if setPositionalValue:
                    valuedPositionals[lastArg.name].setValue(arg)
                    setPositionalValue = lastArg.nargs
                    valuedPositionals[lastArg.name].nargs -= 1
                    setPositionalValue = bool(lastArg.nargs)

                elif setOptionalValue:
                    valuedOptionals[lastArg.name].setValue(arg)
                    valuedOptionals[lastArg.name].nargs -= 1

                elif arg.startswith("-"):
                    optionalsNames = [optional.name for optional in optionals]
                    if arg in optionalsNames:
                        valuedOptionals[arg] = optionals[optionalsNames.index(arg)]
                        if optionals[optionalsNames.index(arg)].action == "storeValue":
                            setOptionalValue = True
                        optionalIndex += 1
                        lastArg = optionals[optionalsNames.index(arg)]
                    else:
                        unknownOptional = "--" + arg
                        break
                        
                else:
                    try:
                        valuedPositionals[positionals[positionalIndex].name] = positionals[positionalIndex]
                    except IndexError:
                        break
                    try:
                        valuedPositionals[positionals[positionalIndex].name].setValue(arg)
                    except Exception as error:
                        self.__exception(error)
                    unknownPositional = None
                    lastArg = positionals[positionalIndex]
                    lastArg.nargs -= 1
                    setPositionalValue = bool(lastArg.nargs)
                    positionalIndex += 1


            if setOptionalValue:
                valuedOptionals[lastArg.name].setValue()

            if not unknownOptional is None:
                continue
            
            if len(valuedPositionals) == len(positionals):
                for argument in optionals:
                    if argument.required:
                        if not argument.name in valuedOptionals:
                            self.__exception("Required optional argument doesn't given.")

                args = {arg.name: None for argGroup in self.arguments for arg in argGroup}
                args.update({name: arg.value for name, arg in {**valuedPositionals, **valuedOptionals}.items()})
                return args
        
        else:
            if not unknownOptional is None:
                self.__exception(f"Unknown optional argument: {unknownOptional}")
            elif not unknownPositional is None:
                self.__exception(f"Unknown positional argument: {unknownPositional}")
            else:
                self.__exception("Invalid positionals arguments.")



    def __typeHelp(self) -> None:
        self.__printUsage()
        help = ""
        for index, argumentGroup in enumerate(self.arguments):
            help += f"    group {index}\n"
            for argument in argumentGroup:
                help += f"    {argument.name}: {argument.description}"
                if not argument.default is None:
                    help += f" Default: {argument.default}"
                if not argument.choices is None:
                    help += f" Choices: {', '.join(argument.choices)}"
                
                help += "\n"
            help += "\n"
        
        print(help)

    def __findArgsNames(self, args: list):
        positionals = []
        optionals = []
        for argument in args:
            if argument.name.startswith("-") or argument.name.startswith("--"):
                optionals.append(argument)
            else:
                positionals.append(argument)
        return positionals, optionals

    def __exception(self, massage) -> None:
        self.__printUsage()
        print("Error:", massage)
        sys.exit(1)

    def __printUsage(self) -> None:
        usage = "usage: [-h, --help] "
        for argumentGroup in self.arguments:
            usage += "( "
            for argument in argumentGroup:
                if argument.name.startswith("-"):
                    usage += f"[{argument.name}]"
                else:
                    usage += argument.name
                usage += " "
            usage += ")"

        print(usage)

class CLI:
    possibleTests = ["runtime", "memory"]

    def __init__(self) -> None:
        argparser = ArgumentParser("tester", description="Program for testing python modules.")
        argparser.addArgument("module", type_=str, description="Given module for testing.")
        argparser.addArgument("iters", type_=int, description="How many times module will be tested.")
        argparser.addArgument("tests", choices=CLI.possibleTests, description="Tests those measurer should do with given module.", nargs="+")
        argparser.createGroup()
        argparser.addArgument("--config", type_=str, group=1, description="Takes all setup configuration from configuration file.", default="config.cfg", required=True)
        arguments = argparser.parseArgs()

        if not arguments["--config"] is None:
            configParser = configparser.ConfigParser()
            if not os.access(os.path.abspath(arguments["--config"]), os.F_OK):
                raise FileNotFoundError(f"File doesn't exist. Path: {os.path.abspath(arguments['--config'])}")
            configParser.read(os.path.abspath(arguments["--config"]))

            self.module = os.path.abspath(configParser["MEASURER_DATA"]["module"])
            self.iters = int(configParser["MEASURER_DATA"]["iters"])
            self.tests = configParser["MEASURER_DATA"]["tests"].split(", ")
        else:
            self.module = os.path.abspath(arguments["module"])
            self.iters = arguments["iters"]
            self.tests = arguments["tests"]

        if not os.access(self.module, os.F_OK):
            raise FileNotFoundError(f"File doesn't exists. Path: {self.module}")

    def getTests(self) -> list:
        return self.tests

    def showTable(self, table) -> None:
        buildenTable = table.build()
        print(buildenTable)

class Tester:
    def __init__(self, tests: list) -> None:
        if not isinstance(tests, list):
            tests = [tests]
        self.tests = tests
        self.testingFunctions = []

    def importScript(self, pathToScript: str) -> None:
        programFolder = os.path.split(__file__)[0]

        scriptName = os.path.split(pathToScript)[1]

        if not scriptName in os.listdir(programFolder) and scriptName.endswith(".py"):
            script = import_module(os.path.splitext(scriptName)[0])

        else:
            scriptContent = read(pathToScript)
            rewrite(os.path.join(programFolder, scriptName), scriptContent)
            invalidate_caches()
            script = import_module(os.path.splitext(scriptName))
        
        for name in dir(script):
            if isinstance(getattr(script, name), testRunner):
                self.testingFunctions.append(getattr(script, name))

    def makeTests(self, iters: int) -> None:
        self.results = {}
        for test in self.tests:
            if not self.testingFunctions == []:
                results = {}
                for function in self.testingFunctions:
                    if test == "memory":
                        result = function(test)
                    else:
                        result = [function(test) for iter in range(iters)]
                    results.update({function.name: result})
                self.results.update({test: results})
            else:
                if test == "memory":
                    self.results.update({test: {"": ""}})
                else:
                    self.results.update({test: {"": ["" for i in range(iters)]}})

    def getResults(self) -> dict:
        return self.results

class Table:
    def __init__(self, results: dict, iters: int) -> None:
        tests = ["Tests."]
        funcNames = ["Functions."]
        iters_ = [[f"Iteration {i + 1}."] for i in range(iters)]
        for test, functionNames in results.items():
            tests.append(test)
            for functionName, results_ in functionNames.items():
                funcNames.append(functionName)
                if not test == "memory":
                    for iteration, result in enumerate(results_):
                        iters_[iteration].append(str(result))


        testLen = max([len(test) for test in tests])
        namesLen = max([len(name) for name in funcNames])
        itersLens = [max([len(res) for res in iter]) for iter in iters_]
        tableLen = testLen + namesLen + sum(itersLens) + 3 + iters


        self.table = ["-" * tableLen + "\n",
        f"|%{testLen}s|%{namesLen}s|" % ("Tests.", "Functions.") + "".join([f"%{len}s|" % iters_[i][0] for i, len in enumerate(itersLens)]) + "\n"
        , "-" * tableLen + "\n"]

        for test, functionNames in results.items():
            self.table.append(f"|%{testLen}s|" % test)
            for row, functionName, results in zip(range(iters), functionNames, functionNames.values()):
                if row:
                    self.table.append(f"|{' ' * testLen}|")
                self.table.append(f"%{namesLen}s|" % functionName)
                if test == "memory":
                    self.table.append(f"%{sum(itersLens) + iters - 1}s|" % results)
                else:
                    for i, result in enumerate(results):
                        self.table.append(f"%{itersLens[i]}s|" % result)

                self.table.append("\n")
            self.table.append("-" * tableLen + "\n")



    def build(self) -> str:
        return "".join(self.table)

def main():
    cliManager = CLI()

    tester = Tester(cliManager.getTests())
    tester.importScript(cliManager.module)
    tester.makeTests(cliManager.iters)

    table = Table(tester.getResults(), cliManager.iters)

    cliManager.showTable(table)

if __name__ == "__main__":
    main()
