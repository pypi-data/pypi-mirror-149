import subprocess as sp
import shlex


def parse(f):
    def deco(cmd, *args, **kwargs):
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)
        return f(cmd, *args, **kwargs)

    return deco


@parse
def fpipe(cmd, cwd=None):
    p = sp.Popen(cmd, stdout=sp.DEVNULL, stdin=sp.DEVNULL, cwd=cwd)

    return p


@parse
def pipe(cmd, n_lines=0, return_idx=0, cwd=None):
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, cwd=cwd)
    if n_lines:
        lines = [p.stdout.readline() for _ in range(n_lines)]
        p.terminate()
        return lines[return_idx].decode().rstrip()

    lines = p.stdout.readlines()
    p.terminate()
    return [line.decode().rstrip() for line in lines]


@parse
def call(cmd):
    sp.check_call(cmd)
