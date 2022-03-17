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
    os.system('cat ./territores_in_game_num | column ')


def player_terr_list(gam):
    terr_list = []
    for j in terr_objects:
        if j.get_terr_own() == gam.get_player_id():
            terr_list.append(j.id_terr)
    return terr_list


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


def player_terr_counter(gam):
    counter = 0
    for j in terr_objects:
        if j.get_terr_own() == gam.get_player_id():
            counter += 1
    return counter


def player_level(terr_count):
    if terr_count < 5:
        return 0
    elif 5 < terr_count < 8:
        return 1
    elif 8 < terr_count < 12:
        return 2
    else:
        return 3


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
        print(f'\n\n{attacker_name} wygrałeś i zająłeś {terr_objects[to_where].name_terr}, masz tam {units} jednostek')
        terr_objects[to_where].terr_own = gam.get_player_id()
        terr_objects[to_where].force = units
    else:
        print(f'\n\n{attacker_name} przegrałeś i {terr_objects[to_where].name_terr} nadal należy do {defender_name} '
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

        while True:

            from_where = input('\nSkąd chcesz przejść: ')
            from_where_check = from_where.strip().split(' ')

            if recruit_helper(gam, from_where_check) is True:
                break

        while True:
            try:
                to_where = int(input('\nGdzie idziesz: '))
                print('')
                if not 0 <= to_where <= len(terr_objects)-1:
                    print(f'Podaj liczbę z przedzału (0 - {len(terr_objects)-1})')
                    continue
                break

            except ValueError:
                print('Wprowadzona liczba musi być liczbą całkowiką')
                print('')

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
        terr_objects[to_where].force += units

    else:
        attack(gam, to_where, units)


def dislocation_force_getter(fr_where):
    while True:
        try:
            units = int(input(f'\nIle jednostek chcesz użyć z {terr_objects[fr_where].name_terr}'
                              f' (dostępnych {terr_objects[fr_where].force}): '))
            print('')
            if 0 <= units <= terr_objects[fr_where].force:
                break
            print(f'Podaj liczbę z przedzału (0 - {terr_objects[fr_where].force})')
        except ValueError:
            print('Wprowadzona liczba musi być liczbą całkowiką')
            print('')

    terr_objects[fr_where].force -= units
    if terr_objects[fr_where].force == 0:
        terr_objects[fr_where].terr_own = -1

    return units


def recruitment(gam):
    if gam.recruit == 1:
        print('\nNie możesz się rekruować! Poczekaj jedną kolejkę.')
        print('')
        move(gam)
    else:
        recruit_force = random.randrange(1, 6+1 + int(gam.get_player_level()))
        print(f'Zrekrutowałeś {recruit_force} jednostek, gdzie chcesz je ulokowac?')
        print('Twoje terytoria: ')
        player_terr(gam)

        while True:

            choice = input('Wybór: ')
            choice = choice.strip().split(' ')

            if recruit_helper(gam, choice) is True:
                break

        if len(choice) > 1:
            for c in choice:
                c = int(c)

                while True:
                    try:
                        unit = int(input(f'\nIle jednostek chcesz ulokować w '
                                         f'{terr_names[c]} (dostępne {recruit_force}): '))
                        print('')
                        if 0 <= unit <= recruit_force:
                            break
                        print(f'Podaj liczbę z przedzału (0 - {recruit_force})')
                    except ValueError:
                        print('Wprowadzona liczba musi być liczbą całkowiką')
                        print('')

                terr_objects[c].set_force(unit)   # this function adding forces
                recruit_force -= unit
        else:
            terr_objects[int(choice[0])].set_force(recruit_force)

        if gam.get_player_recruit() == 2:
            gam.recruit = 0


def recruit_helper(gam, choice):
    answer = True
    try:
        for ch in choice:
            if answer is False:
                break
            for t in player_terr_list(gam):
                if int(ch) is int(t):
                    answer = True
                    break
                elif int(ch) is not int(t):
                    answer = False

        if answer is False:
            if len(choice) is 1:
                print('Wprowadzone terytorium nie należy do ciebie')
            else:
                print('Wprowadzone terytoria nie należą do ciebie')

    except ValueError:
        print('Wprowadzona liczba musi być liczbą całkowiką')
        print('')
        answer = False

    return answer


def move(gam):                # During working on the main loop this is main menu
    gam.view_player()

    print('1. Rekrutacja')
    print('2. Przemieszczanie wojsk / atak')
    print('3. Nic (utrata kolejki)')

    while True:
        try:
            choice = int(input(f'{gam.get_player_name()} wybierz numer:  '))
            print('')
            if 1 <= choice <= 3:
                break
            print('Podaj liczbę z przedzału (1 - 3)')
        except ValueError:
            print('Wprowadzona liczba musi być liczbą całkowiką')
            print('')

    if choice == 1:
        recruitment(gam)
    elif choice == 2:
        dislocation(gam)
    else:
        pass

    if gam.recruit < 2:
        gam.recruit += 1


def building_map_helper(choice):
    answer = True
    try:
        for co in choice:
            if not 1 <= int(co) <= 6:
                answer = False
                print('Podaj liczbę z przedzału (1 - 6)')
    except ValueError:
        print('Wprowadzona liczba musi być liczbą całkowiką')
        print('')
        answer = False
    return answer


os.system('clear')
print('-' * 24)
print('     RISK THE GAME       ')
print('-' * 24, '\n')

players_count = -1
while True:
    try:
        players_count = int(input('Ilu bedzie graczy: '))
        print('')
        if 1 < players_count <= 42:
            break
        print('Podaj liczbę z przedzału (2 - 42)')
    except ValueError:
        print('Wprowadzona liczba musi być liczbą całkowiką')
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
# random.shuffle(gamer)


# showing all players
for i in range(0, players_count):
    print(f'{gamer[i].get_player_name()} jest {i+1} w kolejce gry')

"""

Building own map using only selected continents or play on whole world

"""
print('\n', '-' * 10, 'Wybór mapy', '-' * 10)
print('1.Mapa całego śwata\n2.Mapa własna')
while True:
    try:
        map_type = int(input('\nWybór: '))
        print('')
        if 1 <= map_type <= 2:
            break
        print('Podaj liczbę z przedzału (1 - 2)')
    except ValueError:
        print('Wprowadzona liczba musi być liczbą całkowiką')
        print('')

if map_type == 1:
    with open('territores_files/territores_World', 'r') as r_terr:
        with open('territores_in_game', 'w') as w_terr:
            for line in r_terr:
                w_terr.write(line)
else:
    print('\n', '-' * 6, 'Stwórz własną mapę gry!', '-' * 6)
    print('Kontynenty możesz łączyć wpisując po spacji ich numery\n')
    print('1.North America\n2.South America\n3.Europe\n4.Africa\n5.Asia\n6.Australia')

    while True:
        continents = input('\nWybór: ')
        continents = continents.strip().split(' ')

        if building_map_helper(continents) is True:
            break

    with open('territores_in_game', 'w') as w_terr:
        for continent in continents:
            continent = int(continent)
            for file in os.listdir('territores_files'):
                if file.startswith(f'{continent}') is True:
                    with open(f'territores_files/{file}', 'r') as r_terr:
                        for line in r_terr:
                            w_terr.write(line)
            w_terr.write('\n')

with open('territores_in_game', 'r') as r_terr:
    with open('territores_in_game_num', 'w') as w_terr:
        number = 0
        for line in r_terr:
            w_terr.write(str(number) + '. ' + line)
            number += 1

"""

Upload name of each territory from territories_names file.
Create terr_names list with these names.

"""
terr_names = []
with open('territores_in_game', 'r') as f_terr:   # upload terr_names from file
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

    while True:
        try:
            num = int(input(f'{gamer[i].get_player_name()} wybierz pierwsze terytorium: '))
            print('')
            if not 0 <= num <= len(terr_objects)-1:
                print(f'Podaj liczbę z przedzału (0 - {len(terr_objects)-1})')
                continue
            elif not terr_objects[num].terr_own == -1:
                print('Terytorium należy już do innego gracza!')
                continue

            break

        except ValueError:
            print('Wprowadzona liczba musi być liczbą całkowiką')
            print('')

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
            gamer[i].set_player_level(player_level(player_terr_counter(gamer[i])))
            print('\n', '-' * 25)
            move(gamer[i])

            print('\nTwoje terytoria: ')
            player_terr(gamer[i])
            input('\n\t<Kliknij Enter aby iść dalej>')
            os.system('clear')

    game_round += 1
