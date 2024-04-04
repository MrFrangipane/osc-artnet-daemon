--- ROOT --
function onReceiveOSC(message, connections)
    if message[1] == '/device_name' then
        local device_name = message[2][1].value
        device_name_control = root:findByName('DEVICE_NAME_CONTROL', true)
        device_name_control.values['text'] = device_name

        local device_name_tab = root:findByName('DEVICE_NAME_TAB', true)
        device_name_tab.name = device_name
    end

    if message[1] == '/device_address' then
        local device_address = message[2][1].value
        device_name_control.values['text'] = device_name_control.values['text'] .. " (" .. device_address .. ")"
    end
end
