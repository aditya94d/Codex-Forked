#!/bin/bash

sudo -s <<EOF
cat sshd_config_setup > /etc/ssh/sshd_config
EOF
