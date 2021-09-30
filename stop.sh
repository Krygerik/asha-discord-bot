#!/bin/bash

for KILLPID in `ps ax | grep 'main' | awk ''{print $1;}''`; do
kill -9 $KILLPID;
done