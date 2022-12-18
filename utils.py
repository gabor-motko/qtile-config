import subprocess

# Execute a shell command and return its results as a tuple of (stdout: array, stderr: array, exitcode).
def exec(cmd):
    proc = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    return (
        [item.decode() for item in stdout.split(b"\n")],
        [item.decode() for item in stderr.split(b"\n")],
        proc.returncode
    )
