import requests

from mod_state import ModState

class ModAPI:
    def __init__(self, cf_key=None):
        self.cf_base = "https://api.curseforge.com/v1"
        self.mr_base = "https://api.modrinth.com/v2"
        self.user_agent = "VersionLink/1.0 (wyattk1093@gmail.com)"
        
        # Toggle CurseForge based on key presence
        self.cf_key = cf_key
        self.cf_enabled = True if cf_key else False
        self.cf_headers = {"x-api-key": cf_key} if self.cf_enabled else {}

    def get_modrinth_data(self, slug, state):
        headers = {"User-Agent": self.user_agent}
        res = requests.get(f"{self.mr_base}/project/{slug}/version", headers=headers)
        if res.status_code != 200:
            return state

        for ver in res.json():
            for g_ver in ver['game_versions']:
                for loader in ver['loaders']:
                    state.add_version(g_ver, loader.lower())
        return state

    def get_curseforge_data(self, mod_id, state):
        if not self.cf_enabled:
            return state
        # We fetch the files for the specific Mod ID
        res = requests.get(f"{self.cf_base}/mods/{mod_id}/files", headers=self.cf_headers)
        if res.status_code != 200:
            return state

        # CF uses integers for "Game Version Types"
        # 1 = Minecraft Version, 4 = Forge, 5 = Quilt, 6 = Fabric
        loader_map = {1: "forge", 2: "cauldron", 3: "liteloader", 4: "forge", 5: "quilt", 6: "fabric"}

        for file in res.json()['data']:
            # Extract Minecraft versions
            mc_versions = [gv for gv in file['gameVersions'] if "." in gv]
            
            # Extract loaders by checking against known ID types or names
            # In CF API, loaders often appear as strings like "Fabric" in the gameVersions list
            loaders = []
            for gv in file['gameVersions']:
                gv_lower = gv.lower()
                if gv_lower in ["forge", "fabric", "quilt", "neoforge"]:
                    loaders.append(gv_lower)

            for v in mc_versions:
                for l in loaders:
                    state.add_version(v, l)
        return state

    def fetch_mod(self, platform, identifier):
        from mod_state import ModState
        state = ModState(identifier)
        if platform == "modrinth":
            return self.get_modrinth_data(identifier, state)
        elif platform == "curseforge":
            return self.get_curseforge_data(identifier, state)
        return state