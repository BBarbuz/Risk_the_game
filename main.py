import player
import territories
import random
import os


def is_alive(gam):
    count = 0
    for j in terr_objects:
        if j.get_terr_own() == gam.get_player_id():
            count += 1
    if count == 0:
        return False
    else:
        return True


def show_terr():
    print('')
    os.system('cat ./territores_names_num | column -c 100')


def player_terr(gam):
    for j in terr_objects:
        if j.get_terr_own() == gam.get_player_id():
            print(f'{j.id_terr}\t', f'{j.name_terr}\t\t', j.force, end='')
            if j.force == 1:
                print(' jednostka')
            elif j.force == 0 or j.force >= 5:
                print(' jednostek')
            else:
                print(' jednostki')


def free_terr():
    for j in terr_objects:
        if j.get_terr_own() == -1:
            print(f'{j.id_terr}\t', j.name_terr)


def attack(gam, to_where, units):
    defender_units = terr_objects[to_where].force
    defender_name = gamer[terr_objects[to_where].terr_own].get_player_name()
    attacker_name = gam.get_player_name()
    print(f'\n------{terr_objects[to_where].name_terr}------')
    print(f'\n{attacker_name} vs. {defender_name}')
    print(f'\t{units} vs. {defender_units}', ' '*5, end='\r')
    os.system('sleep 1')

    while units > 0 and defender_units > 0:
        if random.randrange(0, 2) == 0:
            defender_units -= 1
        else:
            units -= 1

        print(f'\t{units} vs. {defender_units}', ' '*5, end='\r')
        os.system('sleep 1')

    if units > defender_units:
        print(f'\n{attacker_name} wygrałeś i zająłeś {terr_objects[to_where].name_terr}, masz tam {units} jednostek')
        terr_objects[to_where].terr_own = gam.get_player_id()
        terr_objects[to_where].force = units
    else:
        print(f'\n{attacker_name} przegrałeś i {terr_objects[to_where].name_terr} nadal należy do {defender_name} '
              f'posiada tam {defender_units} jednostek')
        terr_objects[to_where].force = defender_units


def dislocation(gam):
    show_terr()
    print('\n---Przemieszczanie wojsk / atak---')
    print('\nTwoje terytoria: ')
    player_terr(gam)

    to_where = -1
    units = 20
    od = 'n'
    while od == 'n' or od == 'N':
        units = 0
        from_where = input('\nSkąd chcesz przejść: ')
        from_where_check = from_where.strip().split(' ')

        to_where = int(input('\nGdzie idziesz: '))
        print(terr_objects[to_where].terr_own)
        if terr_objects[to_where].terr_own == -1:
            print(f'Wybierasz {terr_objects[to_where].name_terr}, terytorium jest neutralne')

            od = input('Potwierdzasz przemieszczenie? (T/N): ')
            if not (od == 'n' or od == 'N'):
                for where in from_where_check:
                    where = int(where)
                    units += dislocation_force_getter(where)

        elif terr_objects[to_where].terr_own == gam.get_player_id():
            print(f'Wybierasz {terr_objects[to_where].name_terr}, twoje terytorium')

            od = input('Potwierdzasz przemieszczenie? (T/N): ')
            if not (od == 'n' or od == 'N'):
                for where in from_where_check:
                    where = int(where)
                    units += dislocation_force_getter(where)

        else:
            print(f'Wybierasz {terr_objects[to_where].name_terr}, '
                  f'terytorium jest zajęte przez gracza {gamer[terr_objects[to_where].terr_own].get_player_name()}')
            print(f'Posiada na nim {terr_objects[to_where].force} jednostek')

            od = input('Potwierdzasz wojnę? (T/N): ')

            if not (od == 'n' or od == 'N'):
                for where in from_where_check:
                    where = int(where)
                    units += dislocation_force_getter(where)

    if terr_objects[to_where].terr_own == -1:   # neutral territory
        terr_objects[to_where].force = units
        terr_objects[to_where].terr_own = gam.get_player_id()

    elif terr_objects[to_where].terr_own == gam.get_player_id():    # gamer territory, force relocation
        terr_objects[to_where].force = units

    else:
        attack(gam, to_where, units)

    print(terr_objects[to_where].terr_own)


def dislocation_force_getter(fr_where):
    units = 20
    while units > terr_objects[fr_where].force:
        units = int(input(f'\nIle jednostek chcesz użyć z {terr_objects[fr_where].name_terr}'
                          f' (dostępnych {terr_objects[fr_where].force}): '))

    terr_objects[fr_where].force -= units
    if terr_objects[fr_where].force == 0:
        terr_objects[fr_where].terr_own = -1

    return units


def recruitment(gam):
    if gam.recruit == 1:
        print('\nNie możesz się rekruować! Poczekaj jedną kolejkę.')
        move(gam)
    else:
        recruit_force = random.randrange(1, 6+1)
        print(f'Zrekrutowałeś {recruit_force} jednostek, gdzie chcesz je ulokowac?')
        print('Twoje terytoria: ')
        player_terr(gam)
        choice = int(input('Wybór: '))
        terr_objects[choice].set_force(recruit_force)   # this function adding forces
        print(f'Twoje jednostki na {terr_names[choice]}: {terr_objects[choice].force}')

        if gam.get_player_recruit() == 2:
            gam.recruit = 0


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

    if gam.recruit < 2:
        gam.recruit += 1


os.system('clear')
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
    gamer.append(player.Players(i, name, 1, 2))
    print('')

print('Losowanie kolejki...\n')
os.system('sleep 2')
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
os.system('sleep 2')
show_terr()

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
os.system('clear')

"""

Main loop for this game. After setting beginning stuffs all game is inside this loop.

"""
print('')
while True:
    print('\n', '-' * 8, f'Runda {game_round}', '-' * 8)
    for i in range(0, players_count):
        if is_alive(gamer[i]) is True:
            print('\n', '-' * 25)
            move(gamer[i])

            print('\nTwoje terytoria: ')
            player_terr(gamer[i])
            input('\n\t<Kliknij Enter aby iść dalej>')
            os.system('clear')

    game_round += 1
