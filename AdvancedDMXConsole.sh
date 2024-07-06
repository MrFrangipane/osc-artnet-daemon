export PYTHONPATH=${PYTHONPATH}:~/AdvancedDMXConsole/osc-artnet-daemon
export PYTHONPATH=${PYTHONPATH}:~/AdvancedDMXConsole/osc-artnet-daemon/examples/advanced-dmx-console
cd ~/AdvancedDMXConsole/osc-artnet-daemon/examples/advanced-dmx-console || exit

~/AdvancedDMXConsole/virtualenv/bin/python -m advanceddmxconsole \
  -m configuration/midi-devices.yml configuration/midi-pages.yml configuration/midi-layer-groups.yml \
  -o configuration/osc.yml \
  -a configuration/artnet-variables.yml configuration/artnet-fixtures.yml \
  -n 192.168.20.12 \
  -u 1
