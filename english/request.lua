while true do
    local timer_id = os.startTimer(150)
    local event, id
    repeat
        event, id = os.pullEvent("timer")
    until id == timer_id
    --print("Timer with ID " .. id .. " was fired")
    username = disk.getLabel("bottom")
    print(username)
    local request = http.get("http://localhost:8080", { ["User"] = username })

    if request.getResponseCode() == 200 then
        print("Mining successful")
    end

    if request.getResponseCode() == 204 then
        print("All coins have been mined")
    end

    if request.getResponseCode() == 203 then
        print("Not a registered user. Please contact support if you believe this is a mistake.")
    end

end
