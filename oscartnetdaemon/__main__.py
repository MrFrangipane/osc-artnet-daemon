from oscartnetdaemon import OSCArtnetDaemonAPI

daemon = OSCArtnetDaemonAPI()
daemon.configure_from_command_line()
daemon.run_forever()
