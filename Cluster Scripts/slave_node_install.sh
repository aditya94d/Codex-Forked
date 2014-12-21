#!/bin/bash


sudo apt-get install openssh-client
sudo apt-get install openssh-server
sudo apt-get install nfs-common
sudo apt-get install nfs-kernel-server
sudo apt-get install mpich2

sudo -s <<EOF
cat sshd_config_setup > /etc/ssh/sshd_config
EOF
sudo -s <<EOF
 echo "master:/home/mpiuser /home/mpiuser nfs" >> /etc/fstab
EOF