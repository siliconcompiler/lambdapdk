#!/usr/bin/env bash

set -e

# Get directory of script
src_path=$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)

work_dir=`mktemp -d`

pushd $work_dir

git clone https://github.com/gadfort/bsg_fakeram.git
pushd bsg_fakeram
git checkout nangate45

make tools

make run CONFIG=$src_path/fakeram45.cfg

mkdir -p $src_path/lef $src_path/nldm $src_path/verilog

cp results/*/*.lef $src_path/lef
cp results/*/*.lib $src_path/nldm
cp results/*/*.v $src_path/verilog

popd
popd
