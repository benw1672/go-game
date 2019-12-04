# Import nonlocal dependencies.
import json, jsonpickle, sys, typing, socket, os, math, random
from functools import partial
from importlib import util
from collections import defaultdict

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

    # Start up server, listening on the port specified in the config file.
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((IP, PORT))

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

    # Instantiate the necessary number of default players.
    for i in range(num_default_players):
        players.append(DEFAULT_PLAYER_MODULE.make_player())
    
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
    cheating_players = []
    for i, player in enumerate(players):
        try:
            name = player.register()
            player_to_name[player] = name
        except RuntimeError:
            replace_cheating_player(players, i, cheating_players, player_to_name)

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
        elif game_result.loser_was_cheating:
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


def replace_cheating_player(players, cheating_player_index, cheating_players, player_to_name):
    #create replacement default player
    replacement_default_player = DEFAULT_PLAYER_MODULE.make_player()
    name = replacement_default_player.register()
    player_to_name[replacement_default_player] = name
    #add player to cheating players
    cheating_players.append(players[cheating_player_index])
    #replace cheating player with default player
    players[cheating_player_index] = replacement_default_player


def play_league_tournament(players):
    """
    1.
    """
    player_to_name = {}
    cheating_players = []

    for i, player in enumerate(players):
        try:
            name = player.register()
            player_to_name[player] = name
        except RuntimeError:
            replace_cheating_player(players, i, cheating_players, player_to_name)

    score_board = [[LOSE]*len(players) for _ in range(len(players))]

    for i in range(len(players)-1):
        for j in range(i+1, len(players)):
            game_result = referee.play_a_game(players[i], players[j])
            [print(row) for row in score_board]
            print()
            if game_result.game_was_draw:
                winner, loser = toss_coin(heads_player=players[i], tails_player=players[j])
                if winner == players[i]:
                    score_board[i][j] = WIN
                else:
                    score_board[j][i] = WIN
            elif game_result.loser_was_cheating:
                if game_result.loser == players[i]:
                    winner_index = j
                    cheater_index = i
                else:
                    winner_index = i
                    cheater_index = j
                for other_player_index in range(len(players)):
                    # only give back point if the other player hasn't been replaced
                    if (other_player_index != cheater_index
                            and score_board[cheater_index][other_player_index] == WIN
                            and players[other_player_index] not in cheating_players):
                        score_board[cheater_index][other_player_index] = LOSE
                        score_board[other_player_index][cheater_index] = WIN
                replace_cheating_player(players, cheater_index, cheating_players, player_to_name)
                #give winner the point
                score_board[winner_index][cheater_index] = WIN
            else:
                if game_result.winner == players[i]:
                    score_board[i][j] = WIN
                else:
                    score_board[j][i] = WIN

    rankings = []
    score_to_players = defaultdict(list)
    for i, player in enumerate(players):
        score = sum(score_board[i])
        score_to_players[score].append(player)

    rankings.append(cheating_players)
    for score in sorted(score_to_players.keys()):
        rankings.append(score_to_players[score])

    return pretty_format_rankings(rankings, player_to_name)


def get_tournament_parameters():
    if sys.argv[1] == "--league" and sys.argv[2].isdigit():
        mode = LEAGUE
        num_remote_players = int(sys.argv[2])
    elif sys.argv[1] == "--cup" and sys.argv[2].isdigit():
        mode = CUP
        num_remote_players = int(sys.argv[2])
    else:
        raise ValueError("Incorrect command-line arguments.")
    num_default_players = nearest_power_of_two(num_remote_players) - num_remote_players
    return mode, num_remote_players, num_default_players


def close_client(clientsocket):
    try:
        clientsocket.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    clientsocket.close()


def nearest_power_of_two(n):
    if n == 1:
        return 2
    else:
        return 2**math.ceil(math.log2(n))


if __name__ == "__main__":
    main()