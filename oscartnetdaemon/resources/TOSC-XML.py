from xml.etree import ElementTree
import zlib


def to_xml(filename_in, filename_out):
    compressed_data = open(filename_in, 'rb').read()
    decompressed_data = zlib.decompress(compressed_data).decode()

    root = ElementTree.fromstring(decompressed_data)
    tree = ElementTree.ElementTree(root)
    ElementTree.indent(tree, space="\t", level=0)
    tree.write(filename_out, xml_declaration=True, encoding='UTF-8')
    # TODO replace: <default>Frangitronik</default> (hostname)


def to_tosc(filename_in, filename_out):
    tree = ElementTree.parse(filename_in)
    ElementTree.indent(tree, space="", level=0)
    xml_string = ElementTree.tostring(tree.getroot(), xml_declaration=True, encoding='UTF-8')
    xml_string = xml_string.replace(b'\n', b'')
    compressed = zlib.compress(xml_string)
    open(filename_out, 'wb+').write(compressed)


if __name__ == '__main__':
    to_xml("touch-osc.tosc", "touch-osc.xml")
    # to_tosc("touch-osc.xml", "touch-osc.tosc")
