import requests

API_KEY = "RGAPI-b9d55bc9-983a-4dbc-8a2d-d85a6b33a293"

def get_summoner_puuid(gameName,tagLine):
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={API_KEY}"
    # print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['puuid']
    return None
def get_summoner_rank(puuid):
    url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={API_KEY}"
    # print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        summoner_id = data['id']
        summoner_lvl = data['summonerLevel']
        # print(summoner_id)
        url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={API_KEY}"
        # print(url)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for league_entry in data:
                if league_entry['queueType'] == 'RANKED_SOLO_5x5':
                    return  [league_entry['summonerName'],league_entry['tier'],league_entry['rank'],league_entry['leaguePoints'],summoner_lvl]
    return None
def get_summoner_matches(puuid,start=0,count=10):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}&api_key={API_KEY}"
    # print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    return None
def get_players_by_game(game):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{game}?api_key={API_KEY}"
    # print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        players = []
        for participant in data['info']['participants']:
            players.append(participant['puuid'])
        return players
    return None
def rank_to_int(rank):
    """
    IN : rank -> [summonerName, tier, rank, leaguePoints]
    OUT : int -> 1 (Iron IV) to 31 (Challenger)
    """
    if rank[2] == "I":tier=4
    elif rank[2] == "II":tier=3
    elif rank[2] == "III":tier=2
    elif rank[2] == "IV":tier=1
    if rank[1] == "IRON":
        return tier
    elif rank[1] == "BRONZE":
        return 4+tier
    elif rank[1] == "SILVER":
        return 8+tier
    elif rank[1] == "GOLD":
        return 12+tier
    elif rank[1] == "PLATINUM":
        return 16+tier
    elif rank[1] == "EMERALD":
        return 20+tier
    elif rank[1] == "DIAMOND":
        return 24+tier
    elif rank[1] == "MASTER":
        return 29
    elif rank[1] == "GRANDMASTER":
        return 30
    elif rank[1] == "CHALLENGER":
        return 31
    return 0
def get_ranks_by_game(game):
    """
    IN : game -> matchId
    OUT : game_ranks -> [(rank,lvl),(rank,lvl),...] (list of player's ranks)
    """
    players = get_players_by_game(game)
    game_ranks = []
    for puuid in players:
        rank = get_summoner_rank(puuid)
        if rank != None:
            game_ranks.append((rank_to_int(rank),rank[4],puuid))
    return game_ranks
def display_match_ranks(matches, puuid=None):
    """
    Create a single matplotlib graph to display the players' ranks in every game in matches.
    The x-axis represents the level, and the y-axis represents the rank.
    The graph is limited to the range of levels 1 to 700 and ranks 1 to 31.

    If puuid is not None, the graph will display the puuid's player's dot in red.
    """
    import matplotlib.pyplot as plt
    x = []
    y = []
    n = 1
    for game in matches:
        print(f"Game: {game} ({n}/{len(matches)})")
        game_ranks = get_ranks_by_game(game)
        x += [rank[1] for rank in game_ranks if rank[2] != puuid]
        y += [rank[0] for rank in game_ranks if rank[2] != puuid]
        n += 1
    if puuid is not None:
        puuid_rank = get_summoner_rank(puuid)
        print(puuid_rank)
        if puuid_rank is not None:
            plt.scatter(puuid_rank[4], rank_to_int(puuid_rank), color='red')
            print(f"Your rank: {puuid_rank[1]} {puuid_rank[2]} ({puuid_rank[3]} lp)")
    plt.scatter(x, y)
    plt.xlabel('Level')
    plt.ylabel('Rank')
    plt.title('Players Ranks')
    plt.axis(xmin=1, xmax=700, ymin=1, ymax=31)
    plt.hlines([4.5,8.5,12.5,16.5,20.5,24.5,28.5,29.5,30.5,31.5], 1, 700, colors='grey', linestyles='dotted')
    plt.show()

gameName = "mat2dius"
tagLine = "EUW"
puuid = get_summoner_puuid(gameName,tagLine)
rank = get_summoner_rank(puuid)
if rank is not None or rank != []:
    print(f"{rank[0]}'s rank: {rank[1]} {rank[2]} ({rank[3]} lp)")
else:
    print("Summoner not found or an error occurred.")
print("\nRecent matches: ")
matches = get_summoner_matches(puuid,count=50)
# print(matches)
display_match_ranks(matches,puuid)

