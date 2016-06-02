#!/bin/sh
svc=${1:-unknown}
cat <<EOF |mail -i root
Subject: $svc Failed at [$HOSTNAME]
EOF
