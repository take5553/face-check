if [ ! -d data ];then
    mkdir data
fi

sudo docker run \
    --runtime nvidia \
    -d \
    --name face-check_main_0 \
    --rm \
    --env DISPLAY=$DISPLAY \
    --env PULSE_SERVER=unix:/run/user/$UID/pulse/native \
    --volume /tmp/.X11-unix:/tmp/.X11-unix \
    --volume ~/.Xauthority:/root/.Xauthority \
    --volume ~/face-check/src:/face-check/src \
    --volume ~/face-check/data:/face-check/data \
    --volume /tmp/argus_socket:/tmp/argus_socket \
    --volume /run/user/$UID/pulse/native:/run/user/$UID/pulse/native \
    --device /dev/video0 \
    --workdir /face-check/src \
    take5553/face-check:jp5.0
sudo docker exec face-check_main_0 python3 main.py
sudo docker stop face-check_main_0