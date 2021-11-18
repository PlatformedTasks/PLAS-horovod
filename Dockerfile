FROM horovod/horovod:master

COPY . /horovod/examples
COPY hostfile /tmp/generated/hostfile
