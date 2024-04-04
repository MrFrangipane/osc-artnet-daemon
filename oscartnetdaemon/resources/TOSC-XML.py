from xml.etree import ElementTree
import zlib


def to_xml(filename_in, filename_out):
    compressed_data = open(filename_in, 'rb').read()
    decompressed_data = zlib.decompress(compressed_data).decode()

    root = ElementTree.fromstring(decompressed_data)
    tree = ElementTree.ElementTree(root)
    ElementTree.indent(tree, space="\t", level=0)
    tree.write(filename_out, xml_declaration=True, encoding='UTF-8')

    with open(filename_out, 'r') as file:
        content = file.read()

    for hostname in ["Frangitronik", "FrangiPad"]:
        content = content.replace(f"<default>{hostname}</default>", "<default>&lt;DEVICE_NAME&gt;</default>")
        content = content.replace(f"<value>{hostname}</value>", "<value>DEVICE_NAME_TAB</value>")

    with open(filename_out, 'w') as file:
        file.write(content)


def to_tosc(filename_in, filename_out):
    tree = ElementTree.parse(filename_in)
    ElementTree.indent(tree, space="", level=0)
    xml_string = ElementTree.tostring(tree.getroot(), xml_declaration=True, encoding='UTF-8')
    # xml_string = xml_string.replace(b'\n', b'') # FIXME : script newlines !
    compressed = zlib.compress(xml_string)
    open(filename_out, 'wb+').write(compressed)


if __name__ == '__main__':
    to_xml("touch-osc.tosc", "touch-osc.xml")
    to_tosc("touch-osc.xml", "touch-osc.tosc")
