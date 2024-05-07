from oscartnetdaemon.components.touchosc.file_processor import TouchOSCFileProcessor


if __name__ == '__main__':
    filename = "test-widgets"
    tosc_file_processor = TouchOSCFileProcessor()
    tosc_file_processor.read_tosc(filepath=filename + ".tosc")
    tosc_file_processor.write_xml(filepath=filename + ".xml")
