local args = {...}
local monitor = peripheral.find("monitor")
monitor.setCursorPos(1,1)
monitor.setTextColor(colors.white)
local customer = args[1]
local amount = args[2]

local file = fs.open("disk/ID", "r")
local seller = file.readAll()

local request = http.get("http://localhost:8080", {["User"]=seller, ["Customer"]=customer, ["Amount"]=amount})
print(request.getResponseCode())

if request.getResponseCode() == 200 then
    print(customer .. " has purchased " .. amount .. " PRK")
    monitor.setTextScale(0.5)
    monitor.write("Thank you very much")
    monitor.setCursorPos(1,2)
    monitor.write("for your purchase")
    sleep(5)
    monitor.clear()
end

if request.getResponseCode() == 204 then
    print(customer .. " doesn't have enough money")
    monitor.setTextScale(1.5)
    monitor.setTextColor(colors.red)
    monitor.write("BROKE BOI")
    monitor.setCursorPos(1,2)
    monitor.write("DETECTED")
    sleep(5)
    monitor.clear()
end
