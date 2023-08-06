import requests

class ValorantAPI():
    def __init__(self, region="eu"):
        self.api_url = "https://api.henrikdev.xyz/valorant"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        self.region = region

    def get_account_data(self, user, id, version="v1"):
        r = requests.get(self.api_url + f"/{version}/account/{user}/{id}", headers=self.headers)
        if r.status_code != 200:
            return "There was an error processing your request!"

        stats = r.json()["data"]

        puuid = stats["puuid"]
        account_level = stats["account_level"]
        small_card = stats["card"]["small"]
        big_card = stats["card"]["large"]
        wide_card = stats["card"]["wide"]
        last_update = stats["last_update"]

        return {"puuid": puuid, "account_level": account_level, "cards": [small_card, big_card, wide_card], "last_update": last_update}
        
    def get_mmr_data(self, user, id, version="v1"):
        r = requests.get(self.api_url + f"/{version}/mmr/{self.region}/{user}/{id}", headers=self.headers)
        if r.status_code != 200:
            return "There was an error processing your request!"

        stats = r.json()["data"]

        current_tier = stats["currenttier"]
        current_tier_patched = stats["currenttierpatched"]
        ranking_in_tier = stats["ranking_in_tier"]
        mmr_change_to_last_game = stats["mmr_change_to_last_game"]
        elo = stats["elo"]
        
        return {"current_tier": current_tier, "current_tier_patched": current_tier_patched, "ranking_in_tier": ranking_in_tier, "mmr_change_to_last_game": mmr_change_to_last_game, "elo": elo}

    def get_mmr_history(self, user, id, version="v1"):
        data = {}

        r = requests.get(self.api_url + f"/{version}/mmr-history/{self.region}/{user}/{id}", headers=self.headers)
        if r.status_code != 200:
            return "There was an error processing your request!"

        stats = r.json()["data"]

        for data_point in stats:
            current_tier = data_point["currenttier"]
            current_tier_patched = data_point["currenttierpatched"]
            ranking_in_tier = data_point["ranking_in_tier"]
            mmr_change_to_last_game = data_point["mmr_change_to_last_game"]
            date_raw = data_point["date_raw"]
            data.update( {date_raw:{"current_tier": current_tier, "current_tier_patched": current_tier_patched, "ranking_in_tier": ranking_in_tier, "mmr_change_to_last_game": mmr_change_to_last_game}} )

        return data

    def get_match_history(self, user, id, version="v3"):
        data = {}
        r = requests.get(self.api_url + f"/{version}/matches/{self.region}/{user}/{id}", headers=self.headers)
        if r.status_code != 200:
            return "There was an error processing your request!"

        stats = r.json()["data"]

        for data_point in stats:
            meta = data_point["metadata"]
            players = data_point["players"]["all_players"]
            teams = data_point["teams"]
            kills = data_point["kills"]

            team = ""
            for player in players:
                if player["name"] == user and player["tag"] == id:
                    team = player["team"]
                    break
                
            if teams["red"]["has_won"] == True and team == "Red":
                won = True
            elif teams["blue"]["has_won"] == True and team == "Blue":
                won = True
            else:
                won = False

            kill_counter = 0
            for kill in kills:
                if kill["killer_display_name"] == f"{user}#{id}":
                    kill_counter += 1


            map = meta["map"]
            game_length = meta["game_length"]
            game_start = meta["game_start"]
            rounds_played = meta["rounds_played"]
            mode = meta["mode"]
            cluster = meta["cluster"]
            
            data.update({game_start: {"won": won,"map": map, "kills": kill_counter, "game_length": game_length, "rounds_played": rounds_played, "mode": mode, "cluster" :cluster}})
        
        return data

class Player(ValorantAPI):
    def __init__(self, user, id, region="eu"):
        self.user = user
        self.id = id
        self.api_url = "https://api.henrikdev.xyz/valorant"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        self.region = region

    def account_data(self, version="v1"):
        return self.get_account_data(self.user, self.id, version)

    def mmr_data(self, version="v1"):
        return self.get_mmr_data(self.user, self.id, version)

    def mmr_history(self, version="v1"):
        return self.get_mmr_history(self.user, self.id, version)

    def match_history(self, version="v3"):
        return self.get_match_history(self.user, self.id, version)