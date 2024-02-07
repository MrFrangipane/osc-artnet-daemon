--- ROOT --
function onReceiveOSC(message, connections)
    if message[1] == '/device_name' then
        local device_name = message[2][1].value
        root:findByName('DEVICE_NAME', true).values['text'] = device_name

        local faders = self:findAllByType(ControlType.FADER, true)
        if #faders > 0 then
            faders[1].parent.name = device_name
        end
    end
end
