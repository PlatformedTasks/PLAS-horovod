import sys
import subprocess
import shutil
import os


try:
    os.mkdir("/root/.ssh", 0o600)
    shutil.copyfile("/tmp/generated/executor.init", "/root/.ssh/id_rsa")
    os.chmod("/root/.ssh/id_rsa", 0o400)
    
    with open("/tmp/generated/executor.config") as f:
        lines = f.readlines()
        
    for line in lines:
        host = line.split(" ")[0]
        subprocess.run(["scp", sys.argv[2], f"{host}:/tmp/{sys.argv[2].split('/')[-1]}"])
    
    shutil.copyfile(f"{sys.argv[2]}", f"/tmp/{sys.argv[2].split('/')[-1]}")

    horovod_command = sys.argv[1].split(" ")
    horovod_command.insert(1, "--hostfile")
    horovod_command.insert(2, "/tmp/generated/executor.config")
    horovod_command.extend(["python", f"/tmp/{sys.argv[2].split('/')[-1]}"])

    print("horovod_command:", horovod_command)
    
    process = subprocess.run(horovod_command)
except Exception as err:
    print(err)
