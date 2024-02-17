import valorant

KEY = "<RGAPI-KEY>"

def display_match_ranks(match):
    for team in match.teams:
        print(f"{team.teamId} Team's Ranks: ")
        players = match.players.get_all(teamId=team.teamId)
        for player in players:
            print(f"\t{player.gameName} - {player.rank}")

client = valorant.Client(KEY)

uname = input("Enter your Valorant Username: ")
utag = input("Enter your Valorant Tag (eg. #1234)")
account = client.get_user_by_name(uname+"#"+utag)

if account is None:
    print("User not found :c")
    exit(1)

match = account.matchlist().history.find(queueId="competitive")

if match is None:
    print("No recent Ranked match :c")
    exit(1)
else:
    match = match.get()

display_match_ranks(match)