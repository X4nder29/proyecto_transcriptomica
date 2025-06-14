#!/usr/bin/env python3
"""
gen_qrc.py

Genera un .qrc a partir de una carpeta:
  - --folder: carpeta base que quieres incluir
  - --prefix: prefijo para <qresource>
  - --output: (opcional) ruta de salida; si no se especifica, imprime por stdout
"""

import os
import argparse
import xml.etree.ElementTree as ET
from xml.dom import minidom


def build_qrc(folder: str, prefix: str) -> ET.ElementTree:
    # Raíz RCC
    rcc = ET.Element("RCC", version="1.0")
    # Nodo qresource con prefix
    qres = ET.SubElement(rcc, "qresource", prefix=prefix)

    # Recorre todos los ficheros en folder
    for root, _, files in os.walk(folder):
        for fname in sorted(files):
            full_path = os.path.join(root, fname)
            # ruta relativa dentro de folder, usando forward slashes
            rel_path = os.path.relpath(full_path, folder).replace(os.sep, "/")
            # alias = nombre de fichero
            alias = fname
            file_el = ET.SubElement(qres, "file", alias=alias)
            file_el.text = rel_path

    return ET.ElementTree(rcc)


def prettify(tree: ET.ElementTree) -> str:
    """Devuelve el XML con indentación y DOCTYPE"""
    # Serializa a string
    rough = ET.tostring(tree.getroot(), "utf-8")
    reparsed = minidom.parseString(rough)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    # Inserta DOCTYPE justo después de la declaración XML
    lines = pretty_xml.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("<?xml"):
            lines.insert(i + 1, "<!DOCTYPE RCC>")
            break
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Genera un .qrc desde una carpeta.")
    parser.add_argument(
        "--folder",
        "-f",
        required=True,
        help="Carpeta base cuyo contenido podrá cargarse como recurso",
    )
    parser.add_argument(
        "--prefix",
        "-p",
        required=True,
        help="Prefijo para el tag <qresource> (por ejemplo '/styles')",
    )
    parser.add_argument(
        "--output", "-o", help="Ruta de salida del .qrc (default: stdout)"
    )
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        parser.error(f"'{args.folder}' no es una carpeta válida.")

    tree = build_qrc(args.folder, args.prefix)
    xml_str = prettify(tree)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(xml_str)
        print(f"Generado {args.output}")
    else:
        print(xml_str)


if __name__ == "__main__":
    main()
