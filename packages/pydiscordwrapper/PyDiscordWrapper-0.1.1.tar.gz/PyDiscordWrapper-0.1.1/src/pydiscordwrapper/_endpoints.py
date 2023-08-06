from ._urls import API_BASE_URL

CURRENT_USER = API_BASE_URL + "/users/@me"
CURRENT_USER_GUILDS = API_BASE_URL + "/users/@me/guilds"

GUILD = API_BASE_URL + "/guilds/{guild_id}"
GUILD_CHANNELS = GUILD + "/channels"
GUILD_MEMBERS = GUILD + "/members"
GUILD_ROLES = GUILD + "/roles"
