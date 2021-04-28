import subprocess
import shlex


class ProcessException(Exception):

    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


def execute(command: str) -> str:
    process = subprocess.Popen(shlex.split(command),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               encoding="utf8",
                               universal_newlines=True)
    try:
        stdout, stderr = process.communicate()
    except UnicodeDecodeError as e:
        raise ProcessException(e.reason)

    if process.returncode:
        raise ProcessException(stderr)

    return stdout
