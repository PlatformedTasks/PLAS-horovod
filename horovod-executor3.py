import sys
import subprocess
import shutil
import os


try:
    os.mkdir("/root/.ssh", 0o600)
    shutil.copyfile("/tmp/generated/executor.init", "/root/.ssh/id_rsa")
    os.chmod("/root/.ssh/id_rsa", 0o400)

    horovod_command = sys.argv[1:]
    print("horovod_command:", horovod_command)
    process = subprocess.run(horovod_command)
except Exception as err:
    print(err)