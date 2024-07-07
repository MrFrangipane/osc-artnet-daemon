# OSC Artnet Daemon

**/!\ BETA VERSION**

- [OSC Artnet Fixtures](https://github.com/MrFrangipane/osc-artnet-fixtures)
- [OSC Artnet Desktop](https://github.com/MrFrangipane/osc-artnet-desktop)

## Notes

- https://github.com/rppicomidi/pico-mc-display-bridge?tab=readme-ov-file
- https://github.com/tttapa/Control-Surface
- https://github.com/rppicomidi/usb_midi_host

## TODO

- FIX LOG QUEUE
- fix "nested" recall groups issue
- fix error messages on recall empty slot
- move MIDIPagination, MIDILayerGroup, OSCRecallGroup to domain contract ?
- ~~fork mido and add timeout `midi_in.receive(timeout=0.2)~~
- find dead code with [vulture](https://github.com/jendrikseipp/vulture)
- ~~wildcards in config files for variable reference~~
- check `atexit` for proper termination
- unify inter-process communication (Queues, Managers, Dataclasses)
- unify configuration files ?
````yaml
---
variables:
  - name: Fader01
    type: fader
    caption: "Fader01"
    midi:
      value: { channel: 6, type: pitchwheel }
      display-caption: { type: sysex, bytes: [
          "00", "00", "66", "14", "12", "00", "{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}"
      ]}
      display-value: { type: sysex, bytes: [
          "00", "00", "66", "14", "12", "00", "{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}"
      ]}
    osc:
      address: /Fader01
````
not sure if this is a good idea, it might lock possibilities

## To read
- https://stackoverflow.com/questions/59402568/python-multiprocessing-queue-not-receiving-puts-from-forked-processes
