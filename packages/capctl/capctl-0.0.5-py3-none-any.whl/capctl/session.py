import threading
import subprocess


class Session(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.output = ""
        self.err = ""
        self.ret = 0
        self.process = None

    def run(self, **kwargs):
        self.process = subprocess.Popen(self.cmd, **kwargs)
        if self.process.stdout is not None:
            self.output = self.print_console(self.process)
        err = self.process.communicate()[1]
        self.err = str(err, "utf-8") if err is not None else ""
        self.ret = self.process.returncode
        return self.output, self.err, self.ret

    def print_console(self, process):
        stdout = ""
        while True:
            nextline = str(process.stdout.readline(), "utf-8")
            if len(nextline) == 0 and process.poll() is not None:
                break
            if nextline:
                print(nextline.strip())
                stdout += nextline
        return stdout
