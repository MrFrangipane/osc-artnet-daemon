import io
import zlib
from xml.etree import ElementTree


class TouchOSCFileProcessor:

    def __init__(self, tosc_filepath: str = None, xml_filepath: str = None):
        self._tosc_filepath = tosc_filepath
        self._xml_filepath = xml_filepath
        self._xml_content: str = ""

    def read_tosc(self, filepath: str = None):
        if filepath is None:
            filepath = self._tosc_filepath

        if filepath is None:
            raise ValueError('No TouchOSC filepath provided')

        compressed_data = open(filepath, 'rb').read()
        decompressed_data = zlib.decompress(compressed_data).decode()

        root = ElementTree.fromstring(decompressed_data)
        tree = ElementTree.ElementTree(root)
        ElementTree.indent(tree, space="\t", level=0)

        with io.BytesIO() as in_memory_file:
            tree.write(in_memory_file, xml_declaration=True, encoding='UTF-8')
            self._xml_content = in_memory_file.getvalue().decode()

    def write_tosc(self, filepath: str = None):
        if filepath is None:
            filepath = self._tosc_filepath

        if filepath is None:
            raise ValueError('No TouchOSC filepath provided')

        compressed = zlib.compress(self._xml_content.encode())
        with open(filepath, 'wb+') as tosc_file:
            tosc_file.write(compressed)

    def write_xml(self, filepath: str = None):
        if filepath is None:
            filepath = self._xml_filepath

        if filepath is None:
            raise ValueError('No XML filepath provided')

        with open(filepath, 'w') as xml_file:
            xml_file.write(self._xml_content)
