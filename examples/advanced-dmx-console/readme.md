# Advanced DMX Console

A DMX Artnet console, based on Behringer's XTouch

Three layers
- Fixtures: list of registered fixtures
- DMX: list of DMX channels for selected fixture
- Programs: list of programs (all fixtures values saved into each program)

Command line

````
python -m advanceddmxconsole -m configuration/midi.yml -o configuration/osc.yml -a configuration/artnet.yml   
````
