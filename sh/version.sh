#
# Copyright (c) 2021 Takeshi Yamazaki
# This software is released under the MIT License, see LICENSE.
#

version_str=$(head -n 1 /etc/nv_tegra_release)

if [ -z "${version_str}" ]; then
    version_str=$(dpkg-query --showformat='${Version}' --show nvidia-l4t-core)
    arr1=(${version_str//-/ })
    arr2=(${arr1[0]/./ })
    RELEASE=${arr2[0]}
    REVISION=${arr2[1]}
else
    RELEASE=$(echo $version_str | cut -f 2 -d ' ' | grep -Po '(?<=R)[^;]+')
    REVISION=$(echo $version_str | cut -f 2 -d ',' | grep -Po '(?<=REVISION: )[^;]+')
fi

REVISION_MAJOR=${REVISION:0:1}
REVISION_MINOR=${REVISION:2:1}

VERSION="${RELEASE}.${REVISION}"

echo "L4T BSP Version:  L4T R${VERSION}"