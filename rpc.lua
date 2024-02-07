local rpc_server_port = 1974
-- usage:
-- LoadScript("custom/rpc.lua")
-- this doesnt work for now
-- TheSim:QueryServer("0.0.0.0:rpc_server_port/api/rotwoodrpc", nil, "POST", GetRPCData())

function GetDiscordRPCData()
    local payload = {}
    payload["ingame"] = InGamePlay()
    payload["localgame"] = TheNet:IsGameTypeLocal()
    payload["playercount"] = #AllPlayers

    -- largeimagetext used for room name by default, you can change it if you want
    if (TheWorld) then
        payload["largeimagetext"] = TheWorld.prefab
    else
        payload["largeimagetext"] = ""
    end

    -- primarytext used for biome name + frenzy level by default
    if (TheDungeon) and (TheDungeon:GetDungeonMap()) and (TheDungeon:GetDungeonMap().data) and (TheDungeon:GetDungeonMap().data.location_id) then
        local biome_name = TheDungeon:GetDungeonMap():GetBiomeLocation().pretty.name
        local frenzy_level = TheDungeon.progression.components.ascensionmanager:GetSelectedAscension(TheDungeon:GetDungeonMap().data.location_id)

        -- dont show frenzy level for Camp
        if (biome_name == "Camp") then
            payload["primarytext"] = biome_name.." [Fr."..frenzy_level.."]"
        else
            payload["primarytext"] = biome_name
    else
        payload["primarytext"] = ""
    end

    return json.encode(payload)
end
