-- usage:
-- LoadScript("custom/rpc.lua")
-- SendRPCData(GetRPCData())
function SendDiscordRPCData(jsondata)
    -- this doesnt work for now
    TheSim:QueryServer(
        "0.0.0.0:1974/api/rotwoodrpc",
        nil,
        "POST",
        jsondata
    )
end

function GetDiscordRPCData()
    local payload = {}
    payload["ingame"] = InGamePlay()
    payload["localgame"] = TheNet:IsGameTypeLocal()
    payload["playercount"] = #AllPlayers
    if (TheWorld) then
        payload["room"] = TheWorld.prefab
    else
        payload["room"] = ""
    end
    if (TheDungeon) then
        payload["biome"] = TheDungeon:GetDungeonMap():GetBiomeLocation().pretty.name
    else
        payload["biome"] = ""
    end

    local payload_json = json.encode(payload)

    return payload_json
end
