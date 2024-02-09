--- ROOT --
function onReceiveOSC(message, connections)
    if message[1] == '/device_name' then
        local device_name = message[2][1].value
        local device_name_control = root:findByName('DEVICE_NAME', true)
        device_name_control.values['text'] = device_name
        device_name_control.parent.name = device_name
    end
end
