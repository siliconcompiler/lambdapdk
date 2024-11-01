import json
import os

from jinja2 import Environment, FileSystemLoader
import xml.etree.ElementTree as ET
import xml.dom.minidom

template_dir = os.path.join(os.path.dirname(__file__), 'base', 'templates')
jinja2_env = Environment(loader=FileSystemLoader(template_dir))


LICENSE = '''Copyright 2024 ZeroASIC Corp

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


def __get_gds_type_name(gds_type):
    if gds_type == 0:
        return ""
    if gds_type == 10:
        return "pin"
    if gds_type == 20:
        return "text"
    if gds_type == 30:
        return "fill"

    raise ValueError(str(gds_type))


def make_metal_layer(
        name,
        gds_mapping,
        direction,
        min_width,
        min_spacing,
        resistance_per_um,
        capacitance_per_um,
        max_width=None):

    layer = {
        "name": name,
        "type": "ROUTING",
        "direction": direction,
        "gds": gds_mapping,
        "width": {
            "min": min_width
        },
        "spacing": {
            "min": min_spacing
        },
        "parasitic": {
            "resistance": resistance_per_um,
            "capacitance": capacitance_per_um
        }
    }

    if max_width:
        layer["width"]["max"] = max_width

    return layer


def make_cut_layer(
        name,
        gds_mapping,
        width,
        min_spacing,
        enclosure_bot,
        enclosure_top,
        resistance_per_cut):

    layer = {
        "name": name,
        "type": "CUT",
        "gds": gds_mapping,
        "width": {
            "min": width
        },
        "spacing": {
            "min": min_spacing
        },
        "enclosure": {
            "bottom": enclosure_bot,
            "top": enclosure_top
        },
        "parasitic": {
            "resistance": resistance_per_cut
        }
    }

    return layer


def build_tech(layer_count, name=None, width=None):
    if not isinstance(width, (tuple, list)):
        width = layer_count * [width]

    layers = []
    gds_layer = 1
    for n in range(layer_count):
        layeridx = n + 1

        metal_name = f"metal{layeridx}"
        max_width = 5.0
        if layeridx == layer_count:
            metal_name = "topmetal"
            gds_layer = 100
            max_width = None

        layers.append(
            make_metal_layer(
                metal_name,
                {
                    "number": gds_layer,
                    "types": {
                        "NET": 0,
                        "SPNET": 0,
                        "PIN": 10,
                        "LEFPIN": 10,
                        "FILL": 30
                    },
                    "name": {
                        "PIN": 20,
                        "SPNET": 20,
                        "TEXT": 20
                    }
                },
                "HORIZONTAL" if layeridx % 2 == 1 else "VERTICAL",
                min_width=width[n],
                min_spacing=width[n],
                resistance_per_um=1.5000e-03,
                capacitance_per_um=1.0000E-01,
                max_width=max_width
            ))

        if layeridx != layer_count:
            layers.append(
                make_cut_layer(
                    f"via{layeridx}",
                    {
                        "number": gds_layer + 1,
                        "types": {
                            "NET": 0,
                            "SPNET": 0,
                            "PIN": 10,
                            "LEFPIN": 10,
                            "FILL": 30
                        },
                        "name": {
                            "PIN": 20,
                            "SPNET": 20,
                            "TEXT": 20
                        }
                    },
                    width[n] / 2,
                    width[n] / 2,
                    width[n] / 2,
                    width[n] / 2,
                    resistance_per_cut=10e-3
                ))
        gds_layer += 2

    if not name:
        name = f"{layer_count}ML"

    tech = {
        "name": name,
        "grid": 0.005,
        "layers": layers,
        "outline": (0, 0)
    }

    return tech


def build_layermap(tech, path):
    layermap = []
    for layer in tech["layers"]:
        name = layer["name"]
        gds_number = layer["gds"]["number"]

        for map_type, gds_type in layer["gds"]["types"].items():
            layermap.append((
                name,
                map_type,
                str(gds_number),
                str(gds_type)
            ))

        for map_type, gds_type in layer["gds"]["name"].items():
            layermap.append((
                "NAME",
                f"{name}/{map_type}",
                str(gds_number),
                str(gds_type)
            ))

    layermap.append((
        "DIEAREA",
        "ALL",
        str(tech["outline"][0]),
        str(tech["outline"][1])
    ))

    os.makedirs(path, exist_ok=True)
    with open(f'{path}/{tech["name"]}.layermap', 'w') as f:
        f.write(
            jinja2_env.get_template('layermap.j2').render(
                license=LICENSE,
                layers=layermap
            )
        )
        f.write('\n')


def build_openroad_pex(tech, path):
    corners = {
        "maximum": 0.3,
        "typical": 0.0,
        "minimum": -0.3
    }

    for corner, adjustment in corners.items():
        metals = []
        vias = []
        for layer in tech["layers"]:
            name = layer["name"]

            if layer["type"] == "ROUTING":
                metals.append((
                    name,
                    layer["parasitic"]["resistance"]*(1+adjustment),
                    layer["parasitic"]["capacitance"]*(1+adjustment)
                ))
            else:
                vias.append((
                    name,
                    layer["parasitic"]["resistance"]*(1+adjustment)
                ))

        os.makedirs(path, exist_ok=True)
        with open(f'{path}/{tech["name"]}.{corner}.tcl', 'w') as f:
            f.write(
                jinja2_env.get_template('pex.tcl.j2').render(
                    license=LICENSE,
                    metals=metals,
                    vias=vias
                )
            )
            f.write('\n')


def build_klayout_drc(tech, path):
    layers = []

    for n, layer in enumerate(tech["layers"]):
        layer_nm = {
            "name": layer["name"],
            "type": layer["type"],
            "width": {
                "min": int(layer["width"]["min"] * 1000)
            },
            "spacing": {
                "min": int(layer["spacing"]["min"] * 1000)
            }
        }

        if "max" in layer["width"]:
            layer_nm["width"]["max"] = int(layer["width"]["max"] * 1000)

        if layer["type"] == "CUT":
            layer_nm["enclosure"] = {
                "bottom": (
                    tech["layers"][n - 1]["name"],
                    int(layer["enclosure"]["bottom"] * 1000)
                ),
                "top": (
                    tech["layers"][n + 1]["name"],
                    int(layer["enclosure"]["top"] * 1000)
                )
            }

        gds_types = sorted(set(layer["gds"]["types"].values()))
        layer_nm["gds"] = [
            (layer["gds"]["number"], gds_type) for gds_type in gds_types
        ]

        layers.append(layer_nm)

    os.makedirs(path, exist_ok=True)
    with open(f'{path}/{tech["name"]}.drc', 'w') as f:
        f.write(
            jinja2_env.get_template('drc.j2').render(
                license=LICENSE,
                grid=int(tech["grid"] * 1000),
                layers=layers,
                outline={"number": tech["outline"][0], "type": tech["outline"][1]}
            )
        )
        f.write('\n')


def build_klayout_layer_properties(tech, path):
    colors = [
        "#ffc280",
        "#ff9d9d",
        "#ff80a8",
        "#c080ff",
        "#9580ff",
        "#8086ff",
        "#80a8ff",
        "#ff0000",
        "#ff0080",
        "#ff00ff",
        "#8000ff",
        "#91ff00",
        "#008000",
        "#508000",
        "#808000",
        "#805000"
    ]
    patterns = [
        "I5",
        "I9"
    ]

    layeridx = 0

    def make_layer(name, gds):
        prop = ET.Element("properties")

        color = colors[layeridx % len(colors)]
        pattern = patterns[layeridx % len(patterns)]

        for tag, value in [
                ("frame-color", color),
                ("frame-brightness", "0"),
                ("fill-color", color),
                ("fill-brightness", "0"),
                ("dither-pattern", pattern),
                ("line-style", None),
                ("value", "true"),
                ("visible", "true"),
                ("transparent", "false"),
                ("width", "1"),
                ("marked", "false"),
                ("xfill", "false"),
                ("animation", "0"),
                ("name", name),
                ("source", f"{name} {gds[0]}/{gds[1]}@1")
                ]:
            el = ET.Element(tag)

            if value is not None:
                el.text = value
            prop.append(el)

        return prop

    props = ET.Element("layer-properties")
    props.append(make_layer("outline", (tech["outline"][0], tech["outline"][1])))
    layeridx += 1
    for layer in tech["layers"]:
        gds_types = sorted(set([*layer["gds"]["types"].values(), *layer["gds"]["name"].values()]))
        for gds_type in gds_types:
            name = layer["name"]
            gds_name = __get_gds_type_name(gds_type)
            if gds_type:
                name += "." + gds_name
            props.append(make_layer(name, (layer["gds"]["number"], gds_type)))

            layeridx += 1

    props.insert(0, ET.Comment(f"\n{LICENSE}"))

    os.makedirs(path, exist_ok=True)
    with open(f'{path}/{tech["name"]}.lyp', 'w') as f:
        f.write(
            xml.dom.minidom.parseString(
                ET.tostring(props)).toprettyxml(indent="  "))


def build_lef(tech, path):
    vias = []
    for n, layer in enumerate(tech["layers"]):
        if layer["type"] == "ROUTING":
            continue
        bottom_layer = tech["layers"][n - 1]
        top_layer = tech["layers"][n + 1]

        name = layer["name"].upper() + "_1"

        cut_egde = layer["width"]["min"]
        cut = (-cut_egde / 2, -cut_egde / 2, cut_egde / 2, cut_egde / 2)
        bot = (cut[0] - layer["enclosure"]['bottom'], cut[1] - layer["enclosure"]['bottom'],
               cut[2] + layer["enclosure"]['bottom'], cut[3] + layer["enclosure"]['bottom'])
        top = (cut[0] - layer["enclosure"]['top'], cut[1] - layer["enclosure"]['top'],
               cut[2] + layer["enclosure"]['top'], cut[3] + layer["enclosure"]['top'])

        vias.append({
            "name": name,
            "layers": [
                (layer["name"], [f"{v:.3f}" for v in cut]),
                (bottom_layer["name"], [f"{v:.3f}" for v in bot]),
                (top_layer["name"], [f"{v:.3f}" for v in top])
            ]})

    os.makedirs(path, exist_ok=True)
    with open(f'{path}/{tech["name"]}.lef', 'w') as f:
        f.write(
            jinja2_env.get_template('lef.j2').render(
                license=LICENSE,
                grid=tech["grid"],
                layers=tech["layers"],
                vias=vias
            )
        )


def build_openroad_fill(tech, path):
    fill = {"layers": {}}

    for layer in tech["layers"]:
        if layer["type"] == "CUT":
            continue

        max_spacing = 5 * layer["spacing"]["min"]

        max_width = 10 * layer["width"]["min"]
        if "max" in layer["width"]:
            max_width = layer["width"]["max"]

        shapes = []
        for ratio in (1.0, 0.75, 0.5, 0.25, 0.0):
            width = layer["width"]["min"] + ratio * (max_width - layer["width"]["min"])
            width = tech["grid"] * round(width / tech["grid"])

            shapes.append(width)

        fill["layers"][layer["name"]] = {
            "name": layer["name"],
            "layer": layer["gds"]["number"],
            "datatype": layer["gds"]["types"]["NET"],
            "space_to_outline": max_spacing,
            "non-opc": {
                "datatype": layer["gds"]["types"]["FILL"],
                "width": shapes,
                "height": shapes,
                "space_to_fill": layer["spacing"]["min"],
                "space_to_non_fill": max_spacing
            }
        }

    os.makedirs(path, exist_ok=True)
    with open(f'{path}/{tech["name"]}.fill.json', 'w') as f:
        json.dump(fill, f, indent=2)


def build_readme(stackups):
    from lambdapdk import interposer

    for stackup in stackups:
        metals = []
        for layer in stackup["tech"]["layers"]:
            if layer["type"] == "ROUTING":
                metals.append((
                    layer["name"],
                    f'{int(layer["width"]["min"] * 1000)}nm',
                    f'{int(layer["spacing"]["min"] * 1000)}nm'
                ))
        stackup["metalstack"] = reversed(metals)

    with open('README.md', 'w') as f:
        f.write(
            jinja2_env.get_template('README.md.j2').render(
                desc=interposer.setup.__doc__,
                license=LICENSE,
                stackups=stackups
            )
        )


if __name__ == "__main__":
    def tapered_metal(layer_count):
        mid = int(layer_count // 2)
        widths = mid * [0.4]
        if layer_count % 2 != 0:
            widths += [0.8]
        widths += mid * [2.0]
        return widths

    tech_specs = {
        "0400": 0.4,
        "0800": 0.8,
        "2000": 2.0,
        "0400_2000": tapered_metal
    }

    stackups = []

    for name, width in tech_specs.items():
        for layer_count in range(3, 6):
            tech_name = f"{layer_count}ML_{name}"

            widths = width
            if not isinstance(widths, (int, float, list, tuple)):
                widths = widths(layer_count)

            tech = build_tech(layer_count, name=tech_name, width=widths)
            stackups.append({
                "name": tech_name,
                "tech": tech
            })

            build_lef(tech, 'base/apr')
            build_layermap(tech, 'base/apr')
            build_klayout_layer_properties(tech, 'base/setup/klayout')
            build_klayout_drc(tech, 'base/setup/klayout')
            build_openroad_pex(tech, 'base/pex/openroad')
            build_openroad_fill(tech, 'base/dfm/openroad')

    build_readme(stackups)
