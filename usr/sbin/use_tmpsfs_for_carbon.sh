#!/bin/sh
# This script is ment to allow running carbon from tmpfs
# instead of the flash to reduce wear
# another process will priodcly copy the files for the flash
# every 30 min
set -x
GRAPHITE_DIR="/var/lib/graphite"
GRAPHITE_TMP_DIR="${GRAPHITE_DIR}.ephemeral"
GRAPHITE_STOR_DIR="${GRAPHITE_DIR}.permanent"
SIZE="150m"

systemctl is-active carbon-cache.service && systemctl stop carbon-cache.service
if [ ! -d "$GRAPHITE_TMP_DIR" ] ;then
    mkdir ${GRAPHITE_TMP_DIR}
    mount -t tmpfs -o size=${SIZE} tmpfs ${GRAPHITE_TMP_DIR}
fi
if [ ! -d "$GRAPHITE_STOR_DIR" -a -d "$GRAPHITE_DIR" ] ;then
  mv ${GRAPHITE_DIR} ${GRAPHITE_STOR_DIR}
fi

[ -d "$GRAPHITE_DIR" ] || ln -s ${GRAPHITE_TMP_DIR} ${GRAPHITE_DIR}
echo 0 > /proc/sys/vm/swappiness
rsync --archive  ${GRAPHITE_STOR_DIR}/ ${GRAPHITE_TMP_DIR} || exit 1
#systemctl start carbon-cache.service
