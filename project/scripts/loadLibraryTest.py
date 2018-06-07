import sys, os, argparse, ctypes, glob, unittest

commandLine = None

class DefinitionSet:
    pathFormat = "bin.{0}"
    fileNamePattern = "*.so"
# class DefinitionSet

class TestSet(unittest.TestCase):
    
    class TestResult:
        def __init__(self, library, exception = None):
            self.library = library
            self.exception = exception

    def _parseCommandLine(self):
        parser = argparse.ArgumentParser(description='Load Library Test')
        parser.add_argument('-t', '--type', type=str, default='Debug', choices=['Debug', 'Release'],
            metavar = ("--type Debug|Release"),
            help='Debug/Release; build type, if not specified, default is Debug')
        self.commandLine = parser.parse_args()
    
    #class
    def testBoostFileVersion(self):
        allExceptions = []
        currentPath = os.path.dirname(os.path.realpath(__file__))
        currentPath = os.path.dirname(currentPath)
        path = DefinitionSet.pathFormat.format(commandLine.type)
        binPath = os.path.join(currentPath, path)
        pattern = os.path.join(binPath, DefinitionSet.fileNamePattern)
        iterator = glob.glob(pattern)
        for file in iterator:
            try:
                ctypes.cdll.LoadLibrary(file)
                allExceptions.append(self.TestResult(file))
            except:
                allExceptions.append(self.TestResult(file, sys.exc_info()))
        exceptionCount = self._reportExceptions(allExceptions)
        self.assertEqual(exceptionCount, 0)
    # testBoostFileVersion

    def _reportExceptions(self, result):
        exceptionCount = 0
        for item in result:
            print("=============== Testing: {0}".format(item.library))
            if item.exception:
                exceptionCount += 1
                for ee in item.exception: print(ee)
        return exceptionCount

#class TestSet

if __name__ == '__main__':  
    parser = argparse.ArgumentParser(description='Load Library Test')
    parser.add_argument('-t', '--type', type=str, default='Debug', choices=['Debug', 'Release'],
        metavar = ("--type Debug|Release"),
        help='Debug/Release; build type, if not specified, default is Debug')
    commandLine = parser.parse_args()
    while len(sys.argv) > 1:
        sys.argv.pop()
    unittest.main()
