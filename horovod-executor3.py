import sys
import subprocess
import shutil
import os


try:
    os.mkdir("/root/.ssh", 0o600)
    shutil.copyfile("/tmp/generated/executor.init", "/root/.ssh/id_rsa")
    os.chmod("/root/.ssh/id_rsa", 0o400)

    # python_script = sys.argv[2]
    # trainingset = sys.argv[3]
    # training_metrics = sys.argv[4]
    # net_weights = sys.argv[5]

    for idx, arg in enumerate(sys.argv):
        print(f"{idx} -> {arg}")
    exit()
    
    horovod_command = sys.argv[1].split(" ")
    horovod_command.insert(1, "--hostfile")
    horovod_command.insert(2, "/tmp/generated/executor.config")
    horovod_command.extend(["python", python_script, trainingset, training_metrics, net_weights])

    horovod_command = " ".join(horovod_command)
    print("horovod_command:", horovod_command)

    process = subprocess.run(horovod_command, shell=True)
except Exception as err:
    print(err)