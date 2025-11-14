import os, re, sys
import csv
from lxml import etree, html

"""
This function is full of vibes.
"""
def generate_svg_spritesheet(file_list, output_file="sprite.svg"):
    NS = {'svg': 'http://www.w3.org/2000/svg'}
    root = etree.Element(f"{{{NS['svg']}}}svg", nsmap=NS, style="display:none;")
    defs = etree.SubElement(root, f"{{{NS['svg']}}}defs")

    print(f"Processing {len(file_list)} SVGs...")

    for filepath, file_id in file_list:
        symbol_id = file_id
        try:
            tree = etree.parse(filepath); svg_element = tree.getroot()
            if svg_element.tag != f"{{{NS['svg']}}}svg":
                print(f"Skipping {filepath}: Root is not an SVG element.")
                continue

            symbol = etree.Element(f"{{{NS['svg']}}}symbol", id=symbol_id)
            view_box = svg_element.get('viewBox');
            if view_box: symbol.set('viewBox', view_box)
            symbol.extend(svg_element); defs.append(symbol)

            print(f"| Added: {symbol_id} (Source: {filepath}, ViewBox: {view_box})")

        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    tree = etree.ElementTree(root)
    tree.write(output_file, pretty_print=False, xml_declaration=False, encoding='utf-8')
    print(f"\n✅ Spritesheet created at: {output_file}")


SVG_INPUT_TSV = sys.argv[1]
SVG_OUTPUT_FILE = sys.argv[2]

def get_file_list(tsv):
    files = []
    with open(tsv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            source = f'{row['folder']}/{row['source_name']}.svg' if row['source_name'] else f'{row['folder']}/{row['filename']}.svg'
            files.append([source, row['filename']])
    return files

generate_svg_spritesheet(get_file_list(SVG_INPUT_TSV), SVG_OUTPUT_FILE)
