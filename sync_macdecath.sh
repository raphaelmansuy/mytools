#!/bin/bash

# Remote source directory
REMOTE_USER="RAPHAEL"
REMOTE_HOST="192.168.1.5"
REMOTE_DIR="/Users/RAPHAEL/.m2/"

# Local destination directory
LOCAL_DIR="$HOME/.m2/"

# Trace remote and local paths
echo "Remote: ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}"
echo "Local: ${LOCAL_DIR}"

# Starting synchronization
echo "Starting synchronization: ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR} => ${LOCAL_DIR}"

# More trace before starting rsync process
echo "Initiating rsync with detailed progress..."

# Synchronize the directories using rsync with progress details (changed flag)
rsync -av --delete --progress "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}" "${LOCAL_DIR}"

echo "rsync completed with detailed progress"

# Print a message indicating the synchronization is complete
echo "Synchronization of ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR} to ${LOCAL_DIR} is complete."

# New variables for .ivy2 synchronization
REMOTE_DIR_IVY="/Users/RAPHAEL/.ivy2/"
LOCAL_DIR_IVY="$HOME/.ivy2/"

# Trace remote and local paths for .ivy2
echo "Remote .ivy2: ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR_IVY}"
echo "Local .ivy2: ${LOCAL_DIR_IVY}"

echo "Starting synchronization: ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR_IVY} => ${LOCAL_DIR_IVY}"

# Initiate rsync for .ivy2 with progress details
rsync -av --delete --progress "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR_IVY}" "${LOCAL_DIR_IVY}"

echo "Synchronization of .ivy2 is complete."
