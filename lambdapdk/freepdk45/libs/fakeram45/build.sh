#!/usr/bin/env bash

set -e

# Get directory of script
src_path=$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)

work_dir=`mktemp -d`

pushd $work_dir

mkdir -p $src_path/lef $src_path/nldm $src_path/verilog

git clone https://github.com/gadfort/FakeRAM2.0.git
pushd FakeRAM2.0
git checkout 40a7a4beb7c2018c4c4fe62b0cdd955c0d1150e5

python3 run.py $src_path/fakeram45.cfg --output_dir $work_dir/results

cp results/*/*.lef $src_path/lef
cp results/*/*.lib $src_path/nldm
cp results/*/*.v $src_path/verilog

popd
popd
