FROM nvcr.io/nvidia/l4t-pytorch:r32.5.0-pth1.7-py3

#
# build OpenCV
#

RUN apt update \
    && apt install -y --no-install-recommends \
           cmake \
           libavcodec-dev \
           libavformat-dev \
           libavresample-dev \
           libavutil-dev \
           libswscale-dev \
           libgstreamer1.0-dev \
           libgstreamer-plugins-base1.0-dev \
           libgtk2.0-dev \
           unzip \
    && rm -rf /var/lib/apt/lists/* \
    && apt clean
    
RUN wget https://github.com/opencv/opencv/archive/4.5.3.zip \
    && unzip 4.5.3.zip \
    && cd opencv-4.5.3 \
    && mkdir build \
    && cd build \
    && cmake -D WITH_TBB=ON -D BUILD_TBB=ON .. \
    && make -j$(nproc) \
    && make install \
    && cd ../../ \
    && rm -r opencv-4.5.3 \
    && rm 4.5.3.zip

#
# Install Python Library
#

RUN apt update \
    && apt install -y --no-install-recommends \
           nano \
           python3-tk \
    && rm -rf /var/lib/apt/lists/* \
    && apt clean
        
RUN python3 -m pip install -U pip setuptools \
    && python3 -m pip install --no-cache-dir traitlets
    
RUN git clone --branch=master --depth=1 https://github.com/NVIDIA-AI-IOT/jetcam \
    && cd jetcam \
    && python3 setup.py install \
    && cd ../ \
    && rm -rf jetcam

