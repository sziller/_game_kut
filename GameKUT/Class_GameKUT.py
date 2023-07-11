#!/usr/bin/python
# -*- coding: ascii  -*-

"""
Homage to an age old board game.
Remake is a turn based strategy game run in a browser. Players 2-6.
Data can be input by changing necessary yaml files.
As of now, game is in Hungarian.

Gameboard is a collaection of Nodes (Ports) and of edge- or rangebased field-strings (Sea-routes) connecting an
arbitrary combination of the (Ports).

Each player has his/her own session every turn, consisting of:
- LOOP moving all of player's ships (those allowed to move in actual turn):
    - events
    - stacking cards
    - arriving ships reward
    - unloading cards, apply effects
- buying new ships
    - buy ship
    - buy insurance
- LOOP for ships in ports:
    - sell cargo
    - buy cargo
    - buy insurance

PLAYERs own SHIPs: Ship object are either children of the bank or of a Player, once bought.
SHIPs may have certain number of CARGOs: Cargos are children of ShIPS.
to be continued...
"""

import yaml
import os
import random


def yaml_read_in(filename: str, fullpath=None):
    """=== Function name: yaml_read_in =================================================================================
    Script reads data from yaml file, and returns it as is.
    :param filename: the filename to be used (including extension!)
    :param fullpath: if given, used as prefix in front of the filename
    :return: read-in data (the type it is stored in yaml)
    ============================================================================================== by Sziller ==="""
    if not fullpath:
        fullfilename = filename
    else:
        fullfilename = fullpath + filename
    data = open(fullfilename, "r")
    answer = yaml.load(data)
    data.close()
    return answer


def objlist_reorg_by(objectlist: list, arg: str = ""):
    """=== Function name: objlist_reorg_by =============================================================================
    Function reorders an existing list, NOT affecting the original list object though!
    You can insert it into an Object az a method, and use it to alter the original instance.
    It is a simplified version for mostly numerical or string usecases.
    :param objectlist: list - of objects
    :param arg: string - the name of the argument based by which the reordering hapens
    :return list - a new list in the new order.
    ============================================================================================== by Sziller ==="""
    arglist = sorted([getattr(_, arg) for _ in objectlist])  # not too sophisticated ordering, based on Pythons built-in
    reorged_list = []
    for argument in arglist:
        for obj in objectlist:
            if argument == getattr(obj, arg):
                reorged_list.append(obj)
                objectlist.remove(obj)
                break
    objectlist = None  # not necessary.
    return reorged_list

# get rid of globals!
SHIPS = yaml_read_in(filename="../gamedata/hajok.yaml")
RND_EVENTS = yaml_read_in(filename="../gamedata/kartyak.yaml")
CARGOS = yaml_read_in(filename="../gamedata/szallitolevelek.yaml")

# As long as data isn't outsourced into external yaml's, we simply use Globals. Change for Alpha!

PORTS = {'London': False,
         'Belem': False,
         'Boston': False,
         'Bombay': False,
         'Elefantcsontpart': False,
         'Hongkong': False}
EDGES = {'London-Boston': 14,
         'London-Elefantcsontpart': 23,
         'London-Bombay': 25,
         'Boston-Belem': 9,
         'Belem-Elefantcsontpart': 16,
         'Elefantcsontpart-Bombay': 34,
         'Bombay-Hongkong': 17}
RND = {'London-Boston': [4, 11],
       'London-Elefantcsontpart': [3, 7, 10, 13, 19],
       'London-Bombay': [3, 8, 14, 20, 25],
       'Boston-Belem': [3, 5, 8],
       'Belem-Elefantcsontpart': [2, 5, 8, 12, 15],
       'Elefantcsontpart-Bombay': [2, 5, 11, 16, 20, 26, 31],
       'Bombay-Hongkong': [3, 6, 10, 15]
       }

EVENT = {'London-Boston': {5: {'act': 'loss_ship', 'cond': False, 'value': None, 'txt': 'A hajo elsulyed a viharban', 'cp': False},
                           8: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                           13: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None}},
       'London-Elefantcsontpart': {9: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                                   12: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                                   16: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None}},
       'London-Bombay': {7: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                         13: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                         15: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                         19: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None}},
       'Boston-Belem': {2: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                        4: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                        7: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None}},
       'Belem-Elefantcsontpart': {4: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                                  7: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                                  10: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                                  13: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None}},
       'Elefantcsontpart-Bombay': {4: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                                   6: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                                   9: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                                   13: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                                   18: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                                   24: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                                   28: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                                   32: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None}},
       'Bombay-Hongkong': {5: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                           7: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                           13: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None},
                           16: {'act': None, 'cond': None, 'value': None, 'txt': 'placeholder', 'cp': None}}
       }


class KiAzUrATengeren:
    """=== Class name: KiAzUrATengeren =================================================================================
    Game developed for mobile and browser use.
    This is a turn based multiplayer game. The rules allow to let players execute their actions parallel, as there is
    almost no interaction between players.
    Some race conditions may arise in the buying turns, which can later be settled via auctions.
    Have fun!
    ============================================================================================== by Sziller ==="""
    def __init__(self, player_names: list):
        if not player_names: player_names = ['Jackyl', 'Hide']  # Default two player cast

        self.playername_list: list          = player_names
        self.player_objects: list           = []
        # ..............................................
        self.portinfo: dict                 = {}
        self.board: object                  = None
        # ..............................................
        self.shipdata: dict                 = SHIPS
        self.ship_objects_bank: list        = []
        # ..............................................
        self.cargolist: list                = CARGOS
        self.cargo_objects_available: list  = []
        # ..............................................
        self.rndeventlist: list             = RND_EVENTS
        self.rndevent_objects: list         = []
        # ..............................................
        self.bank_balance: int              = 0
        # ..............................................
        
        self.in_game: bool          = False
        self.actual_round: callable = None

    def display_info_player(self):
        """=== Method name: display_info_player ========================================================================
        Prints player info to display
        :var self.player_objects:
        ========================================================================================== by Sziller ==="""
        print(Player.return_header())
        for _ in self.player_objects:
            print(_.return_playerinfo())

    @ staticmethod
    def display_info_cargo_bank(cargo_objects_available: list):
        print(Cargo.return_header())
        for _ in cargo_objects_available:
            print(_.return_cargoinfo())

    def display_info_bank(self):
        print(self.return_header())
        print(self.return_bankinfo())

    @ staticmethod
    def display_info_ships_bank(ship_objects: list):
        print('{}'.format(Ship.return_header(operational=False)))
        for _ in ship_objects:
            print(_.return_shipinfo(operational=False))

    def create_players(self):
        self.player_objects = [Player(name=name, static_mapinfo=self.board.edgeinfo) for name in self.playername_list]

    def msg_create_players_done(self):
        for _ in self.player_objects:
            print("created player - {}: {}".format(_.player_seq_nr, _.name))

    def create_ships(self):
        self.ship_objects_bank = [Ship.from_hun_dict(name, data) for name, data in self.shipdata.items()]
        self.ship_objects_bank = objlist_reorg_by(objectlist=self.ship_objects_bank, arg="nr")

    def msg_create_ships_done(self):
        for _ in self.ship_objects_bank:
            print("created ship   - {}".format(_.name))

    def create_cargos(self):
        self.cargo_objects_available = [Cargo.from_hun_dict(data) for data in self.cargolist]

    def msg_create_cargos_done(self):
        for _ in self.cargo_objects_available:
            print("created cargo  - {}: {} - {}".format(_.good, _.source, _.destination))

    def initial_credit(self, amount: int):
        """=== Method name: initial_credit =============================================================================
        Crediting each players account by a fixed amount. Usually at game start.
        :var self.player_objects: list - list of player objects
        :var self.bank_balance: integer - banks balance sheet
        :param amount: integer - the amount evrey player starts out with
        ========================================================================================== by Sziller ==="""
        for playerobj in self.player_objects:
            playerobj.tx_with_bank(amount)
            playerobj.session_settlement()
            bank_balance_change = playerobj.balance_change_actual_session
            self.bank_balance -= bank_balance_change

    def return_bankinfo(self):
        to_return = "|{:>3}| {:^25} |{:>5}|{:>10}|" \
            .format(0, 'bank', len(self.ship_objects_bank), self.bank_balance)
        return to_return

    @staticmethod
    def return_header():
        return "|{:>3}| {:^25} |{:>5}|{:>10}|".format('nr', 'name', 'ships', 'cash')

    def start(self):
        """=== Method name: start ======================================================================================
        Method starts and encompasses the entire Game.
        The actual Method to launch the GAME ENGINE. This is where all actions are collected.
        Use:
        instance = KiAzUrATengeren(**)
        instance.start()
        ========================================================================================== by Sziller ==="""
        self.preparations()
        while self.in_game:
            self.actual_round = Round(player_objects=self.player_objects,
                                      ship_objects_bank=self.ship_objects_bank,
                                      cargo_objects_bank=self.cargo_objects_available)
            self.actual_round.start()
            self.bank_balance -= self.actual_round.bank_balance_change

            self.display_info_player()
            self.display_info_bank()

            self.end_of_turn()
            os.system("pause")

    def create_board(self):
        self.portinfo = {port: [cargo for cargo in self.cargo_objects_available if cargo.source == port] for port in PORTS.keys()}
        self.board = Playground(nodeinfo=self.portinfo, edgesizes=EDGES, rndinfo=RND, eventinfo=EVENT)
        self.board.generate_edgeinfo()
        self.board.set_rnd_fields()
        self.board.set_event_fields()

    def preparations(self):
        """=== Method name: preparations ===============================================================================
        All the action taking place once game has launched. This is basically Round 0.
        ========================================================================================== by Sziller ==="""
        self.in_game = True
        # Opening the game box, creating starting inventory
        self.create_ships()
        self.create_cargos()
        self.create_board()
        # inviting players listed
        self.create_players()

        # Crediting everyone with initial founds
        self.initial_credit(5000)

        # messaging
        self.msg_create_players_done()
        self.msg_create_ships_done()
        self.msg_create_cargos_done()
        # ...................................................
        self.display_info_player()
        # ...................................................
        self.display_info_bank()
        self.display_info_ships_bank(self.ship_objects_bank)
        self.display_info_cargo_bank(self.cargo_objects_available)

    def end_of_turn(self):
        print("================\nEnd of round {:>3}\n================".format(self.actual_round.counter))

    def end_of_last_turn(self):
        self.in_game = False


class Round:
    """Class name: Round ===============================================================================================
    """
    counter: int = -1

    def __init__(self, player_objects, ship_objects_bank, cargo_objects_bank):
        Round.counter += 1
        self.player_objects = player_objects
        self.ship_objects_bank = ship_objects_bank
        self.cargo_objects_bank = cargo_objects_bank
        self.bank_balance_change = 0

    def start(self):
        """=== Method name: start ======================================================================================
        Starting a new round.
        ========================================================================================== by Sziller ==="""
        self.show_counter()
        self.circle_player_sessions()

        for _ in self.player_objects:
            _.list_shipnames()

    def show_counter(self):
        print("-----------------------\n"
              "- ROUND NUMBER: {:>5} -\n"
              "-----------------------".format(self.counter))

    def circle_player_sessions(self):
        """=== Method name: circle_player_sessions =====================================================================
        Loop through every player. This might be put later into parallel Processes, to enable smooth gameplay, instead
        of hotseat.
        :var self.bank_balance_change: bank's stash
        ========================================================================================== by Sziller ==="""
        for player in self.player_objects:
            player.ship_objects_bank = self.ship_objects_bank
            player.cargo_objects_bank = self.cargo_objects_bank
            player.session()
            self.bank_balance_change += player.balance_change_actual_session  # settlement between player and bank


class Player:
    """=== Class name: Player ==========================================================================================
    This being quite a player centric game, Players are the main Instances to deal with in this game.
    Not much is hapening where Players wouldn be involved.
    =============================================================================================== by Sziller ==="""
    counter_id: int = 0  # player count on init is increased. Class arg introduced

    def __init__(self, name, static_mapinfo):
        self.name: str  = name
        Player.counter_id += 1
        self.player_seq_nr = Player.counter_id
        self.static_mapinfo = static_mapinfo
        self.ships_owned = []
        self.cash = 0
        self.balance_change_actual_session = 0
        # ---------------------------------------------------
        self.ship_objects_bank = []
        self.cargo_objects_bank = []

    def return_playerinfo(self):
        to_return = "|{:>3}| {:>25} |{:>5}|{:>10}|" \
            .format(self.player_seq_nr,self.name,
                    len(self.ships_owned),
                    self.cash)
        return to_return

    @staticmethod
    def return_header():
        to_return = ("|{:>3}| {:^25} |{:>5}|{:>10}|"
                     .format('nr', 'name', 'ships', 'cash'))
        return to_return

    def session(self):
        self.balance_change_actual_session = 0
        # self.ship_objects_bank = ship_objects_bank
        # self.cargo_objects_bank = cargo_objects_bank

        '''
        - loop moving ships:
            - events
            - stacking cards
            - arriving ships reward
            - unloading cards, apply effects
        - buying new ships
            - buy ship
            - buy insurance
        - loop for ships in ports:
            - sell cargo
            - buy cargo
            - buy insurance
        '''

        print("--------------------------------------------------------------------")
        print("Player{:>2}: It is {}'s turn.".format(self.player_seq_nr, self.name))
        print(self.return_header())
        print(self.return_playerinfo())
        self.fleet_movement()
        print("Player{:>2} may buy a ship:".format(self.name))
        self.buy_ship()

        self.buy_cargo()

        self.session_settlement()

        # os.system("pause")

    def list_shipnames(self):
        print("{} owns the following ships".format(self.name))
        print(Ship.return_header())
        for _ in self.ships_owned:
            print(_.return_shipinfo())

    def fleet_movement(self):
        print("{} has the the following ships".format(self.name))
        print('{}'.format(Ship.return_header(operational=True)))
        for _ in self.ships_owned:
            print(_.return_shipinfo(operational=True))
        for shipobj in self.ships_owned:
            tossed = shipobj.dicetoss()
            shipobj.sail(static_mapinfo=self.static_mapinfo, steps=tossed)

            on_sea = bool(shipobj.direction)
            if on_sea:
                edge, field = shipobj.location
                print("---------------------------------------------")
                print(self.static_mapinfo[edge][int(field)].style)
                print("---------------------------------------------")
            else:
                print("---------------------------------------------")
                print("port")
                print("---------------------------------------------")

        for _ in self.ships_owned:
            print(_.return_shipinfo(operational=True))

    def buy_ship(self, limit: int = 2):
        """=== Method name: buy_ship ===================================================================================
        Method to acquire ships when funds available, if ships still to be sold.
        :param limit: integer - max number of ships to buy each turn
        ========================================================================================== by Sziller ==="""
        answer = False
        for counter in range(limit):
            while answer not in ['y', 'Y', 'yes', 'YES', 'Yes', 'yES', 'n', 'N', 'NO', 'No', 'nO', 'no']:
                answer = input("Do you want to buy a ship? ")
            answer = True if answer in ['y', 'Y', 'yes', 'YES', 'Yes', 'yES'] else False
            if not answer:
                break
            else:
                answer = False
                print("You may buy the following ships: ")
                valid_pick_list = [_.nr for _ in self.ship_objects_bank] + [0]
                KiAzUrATengeren.display_info_ships_bank(self.ship_objects_bank)
                select = None
                expensive = False

                while select not in valid_pick_list or expensive:
                    select = input("Pick ship by number, or 0 if you do not want one! ")
                    try:
                        select = int(select)
                    except ValueError:
                        expensive = 1
                    else:
                        if select == 0:
                            answer = "no"
                            break
                        for ship in self.ship_objects_bank:
                            if select == ship.nr:
                                if self.cash > abs(self.balance_change_actual_session - ship.buy_price):
                                    expensive = False
                                    self.ships_owned.append(ship)
                                    self.tx_with_bank(-1 * ship.buy_price)
                                    self.ship_objects_bank.remove(ship)
                                else:
                                    expensive = True
                                    print("SHIT, not enought cash!!! - ship too expensive, pick an other one...")

    def buy_cargo(self):
        """=== Method name: buy_ship ===================================================================================
        Method to acquire cargo when funds available, if cargo still to be sold for ships in ports.
        ========================================================================================== by Sziller ==="""
        for shipobj in self.ships_owned:
            if shipobj.direction == 0:
                name = shipobj.name
                anchoring = shipobj.location[0]
                print("Your ship {} is anchoring in: {}".format(name, anchoring))

                if input("want to buy cargo?"):
                    print("You may buy the following ones:")
                    print(' PICK {}'.format(Cargo.return_header()))
                    c = 0
                    for cargodata in self.cargo_objects_bank:
                        if cargodata.source == anchoring:
                            c += 1
                            print('{:>4} >{}'.format(c, cargodata.return_cargoinfo()))

                    select = int(input("pick one:"))
                    self.ships_owned.append(self.ship_objects_bank[select])
                    self.tx_with_bank(-1 * self.ship_objects_bank[select].price)
                    del(self.ship_objects_bank[select])

    def tx_with_bank(self, amount: int):
        """=== Method name: tx_with_bank ===============================================================================
        Settlement of Players founds IN-turn.
        :param amount: integer - the amount to be transfered. Mind the sign!!!
        :var self.balance_change_actual_session
        ========================================================================================== by Sziller ==="""
        self.balance_change_actual_session += amount

    def session_settlement(self):
        """=== Method name: tx_with_bank ===============================================================================
        Settlement of Players founds at session end between Player and outgoing bank account.
        :var self.balance_change_actual_session
        ========================================================================================== by Sziller ==="""
        self.cash += self.balance_change_actual_session


class Cargo:
    def __init__(self, good, buy_price, sell_price, buyback_price, source, destination, insurance, mass, hypo, nr):
        self.good = good    #
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.hypo = hypo
        self.buyback_price = buyback_price
        self.source = source    #
        self.destination = destination  #
        self.insurance = insurance
        self.mass = mass
        self.nr = nr

    @classmethod
    def from_hun_dict(cls, dictionary):
        good, buy_price, sell_price, buyback_price, source, destination, insurance, mass, hypo, nr =\
            dictionary["Rakomany"], \
            dictionary["AtveteliAr"], \
            dictionary["LeszallitasiAr"], \
            dictionary["Visszavaltas"], \
            dictionary["Berakodas"], \
            dictionary["Celkikoto"], \
            dictionary["Biztositas"], \
            dictionary["RakodasiSuly"], \
            dictionary["Zalogertek"], \
            dictionary["Nr"]
        return cls(good, buy_price, sell_price, buyback_price, source, destination, insurance, mass, hypo, nr)

    def return_cargoinfo(self):
        to_return = "| {:>16} - {:<16} | {:>13} | {:>5} | {:>5} | {:>5} | {:>5} | {:>5} | {:>5}|" \
            .format(self.source,
                    self.destination,
                    self.good,
                    self.buy_price,
                    self.sell_price,
                    self.buyback_price,
                    self.insurance,
                    self.hypo,
                    self.mass)
        return to_return

    @staticmethod
    def return_header():
        to_return = ("| {:>16} - {:<16} | {:>13} | {:>5} | {:>5} | {:>5} | {:>5} | {:>5} | {:>5}|"
                     .format('source', 'destination', 'good', 'buy', 'sell', 'bback', 'ins.', 'hypo', 'mass'))
        return to_return


class Ship:
    def __init__(self, name, nr, buy_price, insurance, insurance_value, buyback_price, hypo, capacity,
                 starting_port: tuple = ("London", 0)):
        self.name           : str   = name
        self.nr             : int   = nr
        self.buy_price      : int   = buy_price
        self.insurance      : int   = insurance
        self.insurance_value: int   = insurance_value
        self.buyback_price  : int   = buyback_price
        self.hypo           : int   = hypo
        self.capacity       : int   = capacity
        # .............................................
        self.location       : tuple = starting_port
        self.direction      : int   = 0  # 0: in port, 1: on edge corresponding to--, -1: on edge against edge-order
        self.nr_of_rounds_to_skip   = 0
        self.speed          : int   = 6
        self.cargo_objects : list  = []

    def return_cargo_weight(self):
        return sum([_.mass for _ in self.cargo_objects])


    @classmethod
    def from_hun_dict(cls, name, dictionary):
        nr, buy_price, insurance, insurance_value, buyback_price, hypo, capacity =\
            dictionary["Nr"],\
            dictionary["UjonnaniAra"],\
            dictionary["Biztositas"],\
            dictionary["BiztositasiErtek"],\
            dictionary["Visszavaltas"],\
            dictionary["Zalogertek"],\
            dictionary["HasznosTeherbirasa"]
        return cls(name, nr, buy_price, insurance, insurance_value, buyback_price, hypo, capacity)

    def return_shipinfo(self, operational: bool = False):
        if operational:
            to_return = "| {:<15} | {:>4} / {:>4} |{:>5} |{:>27}:{:>2}"\
                .format(self.name, self.return_cargo_weight(), self.capacity, self.nr_of_rounds_to_skip, *self.location)
        else:
            to_return = "| {:<15} |{:>5} |{:>5} |{:>5} |{:>5} |{:>5} |{:>5} |{:>5} |" \
                .format(self.name, self.nr, self.capacity, self.buy_price, self.insurance, self.insurance_value,
                    self.buyback_price, self.hypo)
        return to_return

    @staticmethod
    def return_header(operational: bool = False):
        if operational:
            to_return = "| {:^15} | {:>4} / {:>4} |{:^6}|{:>30}".format('name', 'load', 'cap.', 'skip', 'current location')
        else:
            to_return = ("| {:^15} |{:^6}|{:^6}|{:^6}|{:^6}|{:^6}|{:^6}|{:^6}|"
                         .format('name', 'nr', 'cap.', 'price', 'ins.', 'insv.', 'buyb.', 'hypo'))
        return to_return

    def dicetoss(self):
        if self.nr_of_rounds_to_skip > 0:
            self.nr_of_rounds_to_skip -= 1
            print("{} skips this turn.".format(self.name))
            os.system("pause")
            return 0
        else:
            toss = random.randint(1, 6)
            print("{} tossed: {}".format(self.name, toss))
            inp = (input("kimaradas: "))
            try:
                self.nr_of_rounds_to_skip = int(inp)
            except ValueError:
                self.nr_of_rounds_to_skip = 0
            return toss

    def sail(self, static_mapinfo: dict, steps: int):
        """=== Method name: sail =======================================================================================
        Ship movement on board
        :param static_mapinfo:
        :param steps:
        :return:
        ========================================================================================== by Sziller ==="""
        if self.direction == 0:  # ship is in port and must choose future path
            self.pick_edge(static_mapinfo=static_mapinfo)

        print("ITT:")
        print(self.location)

        edge, coord = self.location
        coord += steps * self.direction

        if 0 < coord <= len(static_mapinfo[edge]):
            self.location = (edge, coord)
        else:
            print("in port")
            self.location = {1: (edge.split(sep="-")[1], 0), -1: (edge.split(sep="-")[0], 0)}[self.direction]
            self.direction = 0
        print("you are now at: {}".format(self.location))

    def pick_edge(self, static_mapinfo):
        list_of_possible_endpoints = []
        list_of_possible_edges = []
        list_of_directions = []
        list_of_coords = []
        for edge, fields in static_mapinfo.items():
            endpoints = edge.split(sep="-")
            if self.location[0] in endpoints:
                list_of_possible_edges.append(edge)
                if self.location[0] == endpoints[0]:
                    direction = 1
                    coordinate = 0
                    list_of_possible_endpoints.append(endpoints[1])
                else:
                    direction = -1
                    coordinate = len(fields) + 1
                    list_of_possible_endpoints.append(endpoints[0])
                list_of_coords.append(coordinate)
                list_of_directions.append(direction)

        print("from: {}".format(self.location))
        print("possible_endpoints: {}".format(list_of_possible_endpoints))
        print("their directions: {}".format(list_of_directions))

        szam = int(input('merre? adj egy szamot: '))

        destination = list_of_possible_endpoints[szam]
        self.direction = list_of_directions[szam]

        current_edge = list_of_possible_edges[szam]
        current_coord = list_of_coords[szam]
        self.location = (current_edge, current_coord)
        print("heading to {}".format(destination))
        print("on the path this is {}".format({1: "forward", -1: "backwards"}[self.direction]))
        print("you are at: {}".format(self.location))


class Playground:
    def __init__(self, nodeinfo:dict, edgesizes: dict, rndinfo: dict, eventinfo: dict = {}):
        self.nodeinfo = nodeinfo
        self.edgesizes = edgesizes
        self.edgeinfo = {}
        self.rndinfo = rndinfo
        self.eventinfo = eventinfo

    def generate_edgeinfo(self):
        for edge, length in self.edgesizes.items():
            self.edgeinfo[edge] =\
                [Field(coord="{}.{}".format(edge, _), is_port=False, style="---") for _ in range(1, length+1)]

    def set_rnd_fields(self):
        for edgeid, fieldlist in self.edgeinfo.items():
            for number in self.rndinfo[edgeid]:
                fieldlist[number-1].is_rnd = True
                fieldlist[number - 1].style = 'rnd'

    def set_event_fields(self):
        for edgeid, fieldlist in self.edgeinfo.items():
            for number, event in self.eventinfo[edgeid].items():
                fieldlist[number - 1].event = Event(event)
                fieldlist[number - 1].style = 'evt'

    def setup_portinfo(self, cargoobj_list):
        """=== Method name: setup_portinfo"""


class Field:
    def __init__(self, coord, is_port, style):
        self.coord = coord
        self.style = style
        self.is_port = is_port
        self.is_rnd = False
        self.event = False


class Event:
    def __init__(self, dictionary: dict):
        self.act = dictionary['act']
        self.cond = dictionary['cond']
        self.cp = dictionary['cp']
        self.txt = dictionary['txt']
        self.value = dictionary['value']

    def display_text(self):
        print(self.txt)

"""

def register():
    counter = 0
    ports = ['London', 'Belem', 'Boston', 'Bombay', 'Elefantcsontpart', 'Hongkong']
    for port_in in ports:
        for port_out in ports:
            for level in CARGOS:
                if level['Berakodas'] == port_in and level["Celkikoto"] == port_out:
                    print("{:>17}:{:<17}Nr:{:>3}".format(level['Berakodas'], level["Celkikoto"], level['Nr']))
"""


if __name__ == "__main__":

    # pl = Playground(nodeinfo=PORTS, edgesizes=EDGES, rndinfo=RND, eventinfo=EVENT)
    # pl.generate_edgeinfo()
    # pl.set_rnd_fields()
    # pl.set_event_fields()
    # print(pl.edgeinfo)
    # for k, v in pl.edgeinfo.items():
    #     print("{}:".format(k))
    #     for _ in v:
    #         print("{:>20}".format(_.style))
    #
    # hajo = Ship.from_hun_dict(name="Ariel", dictionary={"UjonnaniAra": 2600,
    #                                                     "Biztositas": 550,
    #                                                     "BiztositasiErtek": 1700,
    #                                                     "Nr": 4,
    #                                                     "HasznosTeherbirasa": 800,
    #                                                     "Visszavaltas": 2300,
    #                                                     "Zalogertek": 1900})
    #
    # hajo.location = "Elefantcsontpart"
    #
    # print(hajo.return_header(operational=True))
    # print(hajo.return_shipinfo(operational=True))
    # while True:
    #     toss = int(input("dicetoss: "))
    #     hajo.sail(static_mapinfo=pl.edgeinfo, steps=toss)

    game = KiAzUrATengeren(player_names=['Lillus', 'Floci', 'Adel'])
    game.start()
