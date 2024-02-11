import re
import argparse


def parse_file(fid, oid, corner):
    data = {}

    file_data = fid.readlines()

    resistance_start = re.compile(r'Metal (\d+) RESOVER 0')
    capacitance_start = re.compile(r'Metal (\d+) OVER 0')
    l_num = 0
    while l_num < len(file_data):
        line = file_data[l_num]
        resistance_group = resistance_start.search(line)

        if resistance_group:
            res_data = data.setdefault(int(resistance_group.group(1)), {})
            res = float(file_data[l_num + 2].split()[-1])

            res_data['res'] = res * 1000

        capacitance_group = capacitance_start.search(line)

        if capacitance_group:
            cap_data = data.setdefault(int(capacitance_group.group(1)), {})
            cap = float(file_data[l_num + 2].split()[1])
            cap_f = float(file_data[l_num + 2].split()[2])

            cap_data['cap'] = cap + cap_f * 2

        l_num = l_num + 1

    mapping = {
        1: "Metal1",
        2: "Metal2",
        3: "Metal3",
        4: "Metal4",
        5: "Metal5",
        6: "MetalTop",
    }

    oid.write('# Metal layers\n')
    for metal, m_data in data.items():
        oid.write(f"set_layer_rc {{{{ corner }}}} -layer {mapping[metal]} "
                  f"-capacitance {m_data['cap']} -resistance {m_data['res']}")
        oid.write('\n')

    vias = {
        1: {"name": "Via1",
            "res": {"typ": 4.5,
                    "wst": 16.845,
                    "bst": 4.23}},
        2: {"name": "Via2",
            "res": {"typ": 4.5,
                    "wst": 16.845,
                    "bst": 4.23}},
        3: {"name": "Via3",
            "res": {"typ": 4.5,
                    "wst": 16.845,
                    "bst": 4.23}},
        4: {"name": "Via4",
            "res": {"typ": 4.5,
                    "wst": 16.845,
                    "bst": 4.23}},
        5: {"name": "Via5",
            "res": {"typ": 4.5,
                    "wst": 16.845,
                    "bst": 4.23}},
        6: None,
    }
    for via in vias.keys():
        if via >= len(data):
            vias[via] = None

    oid.write('# Vias\n')
    for metal in data.keys():
        via = vias[metal]
        if not via:
            continue
        oid.write(f"set_layer_rc {{{{ corner }}}} -via {via['name']} "
                  f"-resistance {via['res'][corner]}")
        oid.write('\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--rcx', type=str, required=True)

    args = parser.parse_args()

    tcl = args.rcx.replace('.rules', '.tcl')
    corner = args.rcx.replace('.rules', '').split('_')[-1]

    with open(args.rcx, 'r') as fid:
        with open(tcl, 'w') as oid:
            oid.write(f'# From: {args.rcx}\n')
            parse_file(fid, oid, corner)
