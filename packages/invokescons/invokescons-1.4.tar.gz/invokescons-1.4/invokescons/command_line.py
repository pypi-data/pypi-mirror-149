import sys
import shlex
import subprocess
import SCons.Script

def main():
    arguments = sys.argv
    command = []
    if (len(arguments) > 1):
        arguments = arguments[1:]
        for i in range(len(arguments)):
            argument = arguments[i]
            arguments[i] = "arguments.append(\""+shlex.quote(argument)+"\")"
        if (len(arguments) > 1):
            arguments = "; ".join(arguments)
        else:
            arguments = arguments[0]
        command.append(sys.executable)
        command.append("-c")
        command.append("import sys; import SCons.Script; arguments = []; "+arguments+"; sys.argv += arguments; print(str(sys.argv)); SCons.Script.main()")
        print(str(command))
        result = subprocess.check_output(command, stderr=subprocess.STDOUT)
        print(result.decode())
    else:
        SCons.Script.main()
    return 0
