#!/usr/bin/env bash

set -e

# Get directory of script
src_path=$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)

work_dir=`mktemp -d`

pushd $work_dir

git clone https://github.com/gadfort/FakeRAM2.0.git
pushd FakeRAM2.0
git checkout c0ed59820551c1587472162691e3b81220b35009

python3 run.py $src_path/fakeram7.cfg

mkdir -p $src_path/lef $src_path/nldm $src_path/verilog

cp results/*/*.lef $src_path/lef
cp results/*/*.lib $src_path/nldm
cp results/*/*.v $src_path/verilog

popd
popd
