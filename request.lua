while(true)
do
local timer_id = os.startTimer(150)
local event, id
repeat
    event, id = os.pullEvent("timer")
until id == timer_id
--print("Timer with ID " .. id .. " was fired")
username = disk.getLabel("bottom")
print(username)
local request = http.get("http://localhost:8080",  { ["User"] = username})
if request.getResponseCode() == 200 then
    print("Mining erfolgreich")
end

if request.getResponseCode() == 204 then
    print("All coins have been mined")
end

if request.getResponseCode() == 203 then
    print("not a registered User please contact Intro if you believe this is a mistake")
end
  
end