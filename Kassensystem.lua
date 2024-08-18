local args = {...}
local monitor = peripheral.find("monitor")
monitor.setCursorPos(1,1)
monitor.setTextColor(colors.white)
local kunde = args[1]

local amount = args[2]


local file = fs.open("disk/ID", "r")
local seller = file.readAll()



local request = http.get("http://localhost:8080", {["User"]=seller, ["Kunde"]=kunde, ["Amount"]=amount})
print(request.getResponseCode())


if request.getResponseCode() == 200 then
    print(kunde .. " hat fuer " .. amount .. "PRK eingekauft")
    monitor.setTextScale(0.5)
    monitor.write("Viel Dank")
    monitor.setCursorPos(1,2)
    monitor.write("fuer ihren Einkauf")
    sleep(5)
    monitor.clear()
end

if request.getResponseCode() == 204 then
    print (kunde .. " hat nicht genug Geld")
    monitor.setTextScale(1.5)
    monitor.setTextColor(colors.red)
    monitor.write("BROKE BOI")
    monitor.setCursorPos(1,2)
    monitor.write("DETECTED")
    sleep(5)
    monitor.clear()
end