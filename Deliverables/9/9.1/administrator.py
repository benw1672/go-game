# Import nonlocal dependencies.
import json, jsonpickle, sys, typing, socket, os, math, random
from functools import partial
from importlib import util

# Import local dependencies.
from constants import *
import utils
from players.remote_proxy_player import RemoteProxyPlayer
from players.state_proxy_player import StateProxyPlayer
from players.strategies import PrioritizeCaptureStrategy
from game_state import BlackIllegalMove, WhiteIllegalMove, LegalEnd
from game_result import GameResult
import referee


def main():
    # Read from command line to see which tournament type will be played.
    mode, num_remote_players, num_default_players = get_tournament_parameters()

    # Get config.
    config = load_config()

    # Start up server, listening on the port specified in the config file.
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((config["IP"], config["port"]))

    # Accept only one connection for now.
    serversocket.listen(num_remote_players)
    num_connections = 0
    clientsockets = []
    while num_connections < num_remote_players:
        conn, _ = serversocket.accept()
        clientsockets.append(conn)
        num_connections += 1

    # Instantiate representative of the remote player.
    players = []
    for clientsocket in clientsockets:
        remote_player = StateProxyPlayer(RemoteProxyPlayer(clientsocket))
        players.append(remote_player)

    # Load default player.
    spec = util.spec_from_file_location('players.default_player', config["default-player"])
    default_player_mod = util.module_from_spec(spec)
    spec.loader.exec_module(default_player_mod)

    # Instantiate the necessary number of default players.
    for i in range(num_default_players):
        players.append(default_player_mod.make_player())
    
    # Play the tournament.
    if mode == CUP:
        final_rankings = play_cup_tournament(players)
    elif mode == LEAGUE:
        final_rankings = play_league_tournament(players)
    print("\n".join(final_rankings))

    # Graceful shutdown.
    for conn in clientsockets:
        close_client(conn)
    serversocket.close()


def play_cup_tournament(players):
    # Ask each player to register.
    player_to_name = {}
    for player in players:
        name = player.register()
        player_to_name[player] = name
    final_rankings = play_cup_tournament_helper(players, rankings=[[]])
    return pretty_format_rankings(final_rankings, player_to_name)


def pretty_format_rankings(rankings, player_to_name):
    result = []
    rank = 1
    while rankings:
        players = rankings.pop()
        for player in players:
            result.append("{}. {}".format(rank, player_to_name[player]))
        rank += len(players)
    return result


def play_cup_tournament_helper(players, rankings):
    """
    rankings:
    16 players
    [
        [cheating_players]
        [p1, ..., p8], <- 13th (round 1 losers)
        [p9, ..., p12], <- 5th place (round 2 losers)
        [p13, p14], <- 3rd place (round 3 losers)
        [p15], <- 2nd place (finals loser)
        [p16] <- 1st place (winner)
    ]
    """
    if len(players) == 1:
        rankings.append(players)
        return rankings
    winners = []
    fair_losers = []
    for i in range(0, len(players), 2):
        player1, player2 = players[i], players[i+1]
        game_result = referee.play_a_game(player1, player2)
        if game_result.game_was_draw:
            winner, loser = toss_coin(heads_player=player1, tails_player=player2)
            winners.append(winner)
            fair_losers.append(loser)
        if game_result.loser_was_cheating:
            winners.append(game_result.winner)
            rankings[0].append(game_result.loser)
        else:
            winners.append(game_result.winner)
            fair_losers.append(game_result.loser)
    rankings.append(fair_losers)
    return play_cup_tournament_helper(winners, rankings)
    

def toss_coin(heads_player, tails_player):
    if random.randint(0, 1) == 0:
        return heads_player, tails_player
    else:
        return tails_player, heads_player


def play_league_tournament(players):
    pass


def get_tournament_parameters():
    if (len(sys.argv) == 3):
        if sys.argv[1] == "-league" and sys.argv[2].isdigit():
            mode = LEAGUE
            num_remote_players = int(sys.argv[2])
        elif sys.argv[1] == "-cup" and sys.argv[2].isdigit():
            mode = CUP
            num_remote_players = int(sys.argv[2])
        else:
            raise ValueError("Incorrect command-line arguments.")
    else:
        raise ValueError("Incorrect command-line arguments.")
    num_default_players = nearest_power_of_two(num_remote_players) - num_remote_players
    return mode, num_remote_players, num_default_players


def load_config():
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir, 'go.config')) as fd:
        config = json.load(fd)
    return config


def close_client(clientsocket):
    try:
        clientsocket.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    clientsocket.close()


def nearest_power_of_two(n):
    return 2**math.ceil(math.log2(n))


if __name__ == "__main__":
    main()