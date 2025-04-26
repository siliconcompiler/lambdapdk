#!/usr/bin/env bash

set -e

# Get directory of script
src_path=$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)

work_dir=`mktemp -d`

pushd $work_dir

mkdir -p $src_path/lef $src_path/nldm $src_path/verilog

git clone https://github.com/gadfort/FakeRAM2.0.git
pushd FakeRAM2.0
git checkout cb17ef7a2af3328c445ed60bcb39a034dec9e261

python3 run.py $src_path/fakeram7.cfg --output_dir $work_dir/results

cp $work_dir/results/*/*.lef $src_path/lef
cp $work_dir/results/*/*.lib $src_path/nldm
cp $work_dir/results/*/*.v $src_path/verilog

popd
popd
