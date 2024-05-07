from oscartnetdaemon.components.touchosc.file_processor import TouchOSCFileProcessor


def process_file(filename):
    tosc_file_processor = TouchOSCFileProcessor()
    tosc_file_processor.read_tosc(filepath=filename + ".tosc")
    tosc_file_processor.write_xml(filepath=filename + ".xml")


if __name__ == '__main__':
    process_file("template-widgets")
    process_file("test-widgets")
