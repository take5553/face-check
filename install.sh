# Check L4T version
source sh/version.sh

## Check current directory
dir_path=$(pwd)

if [ ${RELEASE} -eq 32 ]; then
    if [ ${REVISION_MAJOR} -eq 6 ]; then
        TAG="jp6.0"
    elif [ ${REVISION_MAJOR} -eq 5 ]; then
        TAG="jp5.0"
    fi
fi

## Make run.sh
TEXT=`cat << EOF
sudo docker run \\\\
    --runtime nvidia \\\\
    --rm \\\\
    --net host \\\\
    --env DISPLAY=\\${DISPLAY} \\\\
    --env PULSE_SERVER=unix:/run/user/\\${UID}/pulse/native \\\\
    --volume /tmp/.X11-unix:/tmp/.X11-unix \\\\
    --volume ~/.Xauthority:/root/.Xauthority \\\\
    --volume ${dir_path}/src:/face-check/src \\\\
    --volume ${dir_path}/data:/face-check/data \\\\
    --volume /tmp/argus_socket:/tmp/argus_socket \\\\
    --volume /run/user/\\${UID}/pulse/native:/run/user/\\${UID}/pulse/native \\\\
    --device /dev/video0 \\\\
    --workdir /face-check/src \\\\
    take5553/face-check:${TAG} python3 main.py
EOF
`

echo "${TEXT}" > run.sh
chmod +x run.sh
mkdir data