import player
import territories
import random
import os


def show_terr(terr):
    print('')
    counter = 0
    print(f'\nID\tNazwa\n')
    for j in terr:
        print(counter, '\t', j)
        counter += 1


def player_terr(gam):
    for j in terr_objects:
        if j.get_terr_own() == gam.get_player_id():
            print(f'{j.id_terr}\t', j.name_terr)


def free_terr():
    for j in terr_objects:
        if j.get_terr_own() == -1:
            print(f'{j.id_terr}\t', j.name_terr)


def attack(gam, to_where, from_where, units):
    defender_units = terr_objects[to_where].force
    defender_name = gamer[terr_objects[to_where].terr_own].get_player_name()
    attacker_name = gam.get_player_name()
    print(f'------{terr_objects[to_where].name_terr}------')
    print(f'\n{attacker_name} vs. {defender_name}')
    print(f'{units} vs. {defender_units}', end='\r')
    os.system('sleep 1')

    while units > 0 and defender_units > 0:
        if random.randrange(0, 2) == 0:
            defender_units -= 1
        else:
            units -= 1

        print(f'{units} vs. {defender_units}', end='\r')
        os.system('sleep 1')


def dislocation(gam):
    show_terr(terr_names)
    print('\n---Przemieszczanie wojsk / atak---')
    print('\nTwoje terytoria: ')
    player_terr(gam)
    from_where = int(input('\nSkąd chcesz przejść: '))

    to_where = -1
    od = 'n'
    while od == 'n' or od == 'N':
        to_where = int(input('\nGdzie idziesz: '))
        if terr_objects[to_where].terr_own == -1:
            print(f'Wybierasz {terr_objects[to_where].name_terr}, terytorium jest neutralne')
            od = input('Potwierdzasz przemieszczenie? (T/N): ')
        else:
            print(f'Wybierasz {terr_objects[to_where].name_terr}, '
                  f'terytorium jest zajęte przez gracza {gamer[terr_objects[to_where].terr_own].get_player_name()}')
            print(f'Posiada na nim {terr_objects[to_where].force} jednostek')
            od = input('Potwierdzasz wojnę? (T/N): ')

    units = 1000
    while units > terr_objects[from_where].force:
        units = int(input(f'Ile jednostek chcesz użyć, (dostępnych {terr_objects[from_where].force}): '))

    if terr_objects[to_where].terr_own == -1:
        terr_objects[to_where].force = units
        terr_objects[from_where].force -= units
        terr_objects[to_where].terr_own = gam.get_player_id()

        print('\nTwoje terytoria: ')
        player_terr(gam)

    else:
        attack(gam, to_where, from_where, units)


def recruitment(gam):
    if gam.get_player_recruit() == 0:
        print('Nie możesz się rekruować! Poczekaj jedną kolejkę.')
        move(gam)
    else:
        recruit_force = random.randrange(1, 6+1)
        print(f'Zrekrutowałeś {recruit_force} jednostek, gdzie chcesz je ulokowac?')
        print('Twoje terytoria: ')
        player_terr(gam)
        choice = int(input('Wybór: '))
        terr_objects[choice].set_force(recruit_force)
        print(f'Twoje jednostki na {terr_names[choice]}: {terr_objects[choice].force}')

        if gam.get_player_recruit() == 1:
            gam.recruit = 0
        # print('Wolne terytoria (nie koniecznie z połączeniem):')
        # free_terr(gam)


def move(gam):                # During working on the main loop this is main menu
    gam.view_player()

    print('1. Rekrutacja')
    print('2. Przemieszczanie wojsk / atak')
    print('3. Nic (utrata kolejki)')
    choice = int(input(f'{gam.get_player_name()} wybierz numer:  '))

    if choice == 1:
        recruitment(gam)
    elif choice == 2:
        dislocation(gam)
    else:
        pass

    if gam.get_player_recruit() == 0:
        gam.recruit = 1


print('-' * 24)
print('     RISK THE GAME       ')
print('-' * 24, '\n')


players_count = int(input('Ilu bedzie graczy: '))
print('')

"""

Add players / gamers with id, name, level, territories 
and recruitment ability.  

"""
gamer = []
for i in range(0, players_count):           # adding players on the beginning
    print(f'Gracz ID_{i}')
    name = input('Imie gracza: ')
    gamer.append(player.Players(i, name, 1, 1))
    print('')

print('Losowanie kolejki...\n')
# os.system('sleep 3')
random.shuffle(gamer)


# showing all players
for i in range(0, players_count):
    print(f'{gamer[i].get_player_name()} jest {i+1} w kolejce gry')

"""

Upload name of each territory from territories_names file.
Create terr_names list with these names.

"""
terr_names = []
with open('territores_names', 'r') as f_terr:   # upload terr_names from file
    for line in f_terr:
        terr_names.append(line[:-1])

print('\nGenerowanie mapy...\n')
# os.system('sleep 3')
show_terr(terr_names)

count_terr = len(terr_names)

# create array with territories
terr_objects = []
for i in range(0, count_terr):
    terr_objects.append(territories.Territories(i, terr_names[i], 0, -1))

"""

Choosing start territory for each player and giving them 5 unit each.

"""
for i in range(0, players_count):
    print('\n', '-' * 25)

    gamer[i].view_player()

    num = int(input(f'{gamer[i].get_player_name()} wybierz pierwsze terytorium: '))

    terr_objects[num].set_force(5)
    terr_objects[num].set_terr_own(gamer[i].get_player_id())


game_round = 1

"""

Main loop for this game. After setting beginning stuffs all game is inside this loop.

"""
print('')
while True:
    print('\n', '-' * 8, f'Round {game_round}', '-' * 8)
    for i in range(0, players_count):
        print('\n', '-' * 25)
        move(gamer[i])
        # os.system('clear')

    game_round += 1
    # os.system('clear')
