import os, subprocess, shutil, argparse, multiprocessing, time

class DefinitionSet:
    buildDirectoryFormat = "build.{0}"
    outputDirectoryFormat = "bin.{0}"
    cmakeFormat = 'cmake -DCMAKE_BUILD_TYPE={0} {1} "{2}"'
    cmakeCompiler = "-DCMAKE_C_COMPILER=icc  -DCMAKE_CXX_COMPILER=icpc"
    cmakeNonDefaultCompiler = "icc"
    cmakeIncludeTests = " -Dinclude_tests:boolean=true"
    makeFormat = "make -j {0}" # number of cores
    cmakeCacheFileName = "CMakeCache.txt"

class Builder:
    def build(self):
        self._parseCommandLine()
        self._prepare()
        if not self.buildOnly: 
            if self.commandLine.clean_only:
                return
            compiler = ""
            if self.commandLine.compiler == DefinitionSet.cmakeNonDefaultCompiler:
                  compiler = DefinitionSet.cmakeCompiler
            cmakeCommand = DefinitionSet.cmakeFormat.format(self.commandLine.target, compiler, self.rootDirectory)
            if self.commandLine.include_tests:
                cmakeCommand = cmakeCommand + DefinitionSet.cmakeIncludeTests
            process = subprocess.Popen(cmakeCommand, cwd = self.buildDirectory, shell = True)
            cmakeReturn = process.wait()
            if cmakeReturn != 0:
                exit(cmakeReturn)
        # if not build-only
        makeReturn = self._make()
        if makeReturn != 0:
            exit(makeReturn)
        return 0
    def _detectCmakeCache(self):
        cmakeCacheFileName = os.path.join(self.buildDirectory, DefinitionSet.cmakeCacheFileName)
        return os.path.exists(self.buildDirectory) and os.path.exists(cmakeCacheFileName)
    def _prepare(self):
        scriptDirectory = os.path.dirname(os.path.realpath(__file__))
        self.rootDirectory = os.path.dirname(scriptDirectory)
        self.outputDirectory = os.path.join(
            self.rootDirectory,
            DefinitionSet.outputDirectoryFormat.format(self.commandLine.target)) 
        self.buildDirectory = os.path.join(
            self.rootDirectory,
            DefinitionSet.buildDirectoryFormat.format(self.commandLine.target))
        self.buildOnly = self.buildOnly and self._detectCmakeCache() 
        if self.buildOnly:
            return
        if self.commandLine.clean_build or self.commandLine.clean_only:
            if os.path.exists(self.outputDirectory):
                shutil.rmtree(self.outputDirectory)
            if os.path.exists(self.buildDirectory):
                shutil.rmtree(self.buildDirectory)
            if self.commandLine.clean_only:
                return
        if not os.path.exists(self.buildDirectory):
            os.makedirs(self.buildDirectory)
    def _make(self):
        coreCount = multiprocessing.cpu_count() // 2
        if coreCount < 1:
            coreCount < 1
        process = subprocess.Popen(
            DefinitionSet.makeFormat.format(coreCount),
            cwd = self.buildDirectory,
            shell = True)        
        return process.wait()
    def _parseCommandLine(self):
        parser = argparse.ArgumentParser(description='Build')
        parser.add_argument('-c', '--compiler', type=str, default='gcc', choices=['gcc', 'icc'],
            metavar = ("--compiler gcc|icc"),
            help='gcc|clang|icc; specify compiler to use')
        parser.add_argument('-t', '--target', type = str, default = 'Debug', choices = ['Debug', 'Release'],
            metavar = ("--target Debug|Release"),
            help='Debug|Release; builds debug configuration if not specified')
        parser.add_argument('-cb', '--clean-build', action='store_true',
            default=False, 
            help='True|False; make a clean build if true')
        parser.add_argument('-co', '--clean-only', action = 'store_true', default = False, 
            help='true/false; cleans all build directories and does not perform build')
        parser.add_argument('-it', '--include-tests', action = 'store_true', default = False, 
            help='True|False; include tests into cmake targets if true')
        self.commandLine = parser.parse_args()
        self.buildOnly = not (self.commandLine.clean_build or self.commandLine.clean_only)        
# class Builder

if __name__ == '__main__':
    startTime = time.time()    
    exitCode =  Builder().build()
    if exitCode != 0:
        print("Build error: {0}".format(exitCode))
    elapsedTime = time.time() - startTime
    print(time.strftime("Build time: %H:%M:%S", time.gmtime(elapsedTime)))