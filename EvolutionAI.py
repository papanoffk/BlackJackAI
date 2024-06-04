# параметры - карта дилера, сумма карт.

import neat

from BlackJack import BlackJack
from math import sqrt


generation = -1

class Player():
    def __init__(self, money: int = 100):
        self.money = money
        self.in_game = True

def run(genomes, config):

    # Init NEAT
    nets = []
    ge = []
    players = []

    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)

        # Init my cars
        players.append(Player())

    # Init BlackJack
    game = BlackJack(20)
    game.start(len(players), 10)

    def get_data(game: BlackJack, index: int):
        dealer_card = game.dealer.cards[0]
        match dealer_card[0:2]:
            case '2-':
                dealer_card = 2
            case '3-':
                dealer_card = 3
            case '4-':
                dealer_card = 4
            case '5-':
                dealer_card = 5
            case '6-':
                dealer_card = 6
            case '7-':
                dealer_card = 7
            case '8-':
                dealer_card = 8
            case '9-':
                dealer_card = 9
            case '10':
                dealer_card = 10
            case 'j-':
                dealer_card = 10
            case 'q-':
                dealer_card = 10
            case 'k-':
                dealer_card = 10
            case 'a-':
                dealer_card = 11

        player_points = game.players_hands[index].my_points()

        return dealer_card, player_points


    global generation
    generation += 1

    while True:
        print('GENERATION: ', generation)

        # Input my data and get result from network
        for index, player in enumerate(players):
            if player.in_game:
                output = nets[index].activate(get_data(game, index))
                if output[0] >= 0.5:
                    game.draw_turn(index)
                else:
                    game.pass_turn(index)

        remain_players = 0
        # Update fitness
        for index, player in enumerate(players):
            if game.games[index] and player.in_game:
                remain_players += 1
                ge[index].fitness += 1 / sqrt(21-game.players_hands[index].my_points()) + 1

        if game.dealer_turn():
            player_in_games = 0
            for index, k in enumerate(game.end_game()):
                ge[index].fitness += k * 10
                players[index].money += k * game.money
                if players[index].money > 0:
                    player_in_games += 1
                else:
                    players[index].in_game = False
            if player_in_games > 0:
                game.start(len(players), 20)




if __name__ == '__main__':
    # Set configuration file
    config_path = "config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Create core evolution algorithm class
    p = neat.Population(config)

    # Add reporter for fancy statistical result
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run NEAT
    p.run(run, 1000)