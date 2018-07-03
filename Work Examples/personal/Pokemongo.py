import json, requests,time
import winsound

z0s = 0

def load(pos):
    global z0s
    ignore = ['Caterpie','Drowzee','Golduck','Goldeen','Jynx','Oddish',
              'Pidgey','Pidgeotto','Rattata','Seel','Spearow','Weedle',
              'Zubat','Venonat','Nidoran M','Magikarp','Raticate','Seadra',
              'Psyduck','Poliwhirl','Slowpoke','Staryu','Tentacool','Hypno',
              'Golbat','Gastly','Fearow','Horsea','Tentacruel','Shellder',
              'Seaking','Bellsprout','Krabby','Magnemite','Poliwag',
              'Cloyster','Pinsir','Haunter','Nidoran F','Paras','Magmar',
              'Starmie','Kakuna','Kingler','Mankey','Ponyta','Dratini',
              'Hitmonchan','Abra','Eevee','Metapod','Squirtle','Sandshrew',
              'Cubone','Geodude','Beedrill','Clefairy','Koffing','Exeggcute',
              'Jigglypuff','Ekans','Rhyhorn','Pidgeot','Vulpix',
              'Scyther','Electabuzz','Grimer','Hitmonlee','Slowbro','Wartortle',
              'Parasect','Omanyte','Voltorb','Butterfree','Weepinbell','Gengar',
              'Nidorina','Nidorino','Meowth','Machop','Kabuto','Blastoise',
              'Porygon', 'Gloom','Gyarados','Dewgong','Lickitung','Growlithe',
              'Graveler','Venomoth','Magneton','Dragonair','Diglett','Bulbasaur',
              'Charmander','Poliwrath','Lapras','Doduo','Weezing','Kadabra',
              'Vaporeon','Snorlax']
    resp = requests.get(url='http://skiplagged.com/api/pokemon.php?bounds='+pos)
    try:
        data = json.loads(resp.text)
    except ValueError:
        print('value error')
        return 0
    if not isinstance(data, dict):
        #print('http://skiplagged.com/api/pokemon.php?bounds='+pos)
        print('no return value')
        return 0
    elif 'pokemons' not in data.keys():
        print('no return field')
        return 0
    p = data['pokemons']
    d = {}
    s = []
    if len(p) == 0:
        z0s += 1
    else:
        z0s = 0
    for i in p:
        name = str(i['pokemon_name'])
        c = [i['latitude'],i['longitude'],i['expires']]
        #print(name)
        if name not in ignore:
            if name in s:
                d[name]['pos'].append(c)
            else:
                d[name] = {}
                d[name]['pos'] = c
                s.append(name)
    return d

idx = []

def calc_pos(s,a,b,c,d):
    global idx
    d = load(str(s[0]+a)+','+str(s[1]+b)+','+str(s[0]+c)+','+str(s[1]+d))
    if d == 0:
        return
    k = sorted(d.keys())
    a = []
    t = time.time()
    st = time.strftime("%H:%M:%S", time.gmtime(t))
    for i in k:
        ti = d[i]['pos'][2]
        ss = int(ti - t)
        ss3 = str(ti) + ',' + i
        if ss3 not in idx:
            if ss > 120:
                ss2 = str(int(ss/60)) + 'm' + str(ss%60) + 's'
                a.append('[' + st + '] ' + i + ': ' + str(d[i]['pos'][:2]) + ', ' + ss2 + ', ' + str(ti))
                winsound.Beep(2400,1000)
            idx.append(ss3)
    if len(idx) > 10:
        for i in idx:
            if int(i.split(',')[0]) < t:
                i = 0
        idx = filter(lambda a: a != 2, idx)
        #' '.join([''] * (len(i) + 3))
    #f = open('pokemon.txt','w')
    #f.write('\n'.join(a))
    if len(a) > 0:
        print('\n'.join(a))
    time.sleep(4)

def scan():
    s = [51.523203, -0.196767]
    a = 0.02
    na = -0.02
    a2 = 0.031
    n = 4
    for i in range(n):
        calc_pos(s,na*1,a2*(i),na*0,a2*(i+1))
        calc_pos(s,na*2,a2*(i),na*1,a2*(i+1))
        calc_pos(s,na*3,a2*(i),na*2,a2*(i+1))
        calc_pos(s,na*4,a2*(i),na*3,a2*(i+1))
    
    ppp = """
    calc_pos(s,a,na*2,a*2,na)
    calc_pos(s,a,na,a*2,a)
    calc_pos(s,a,a,a*2,a*2)
    calc_pos(s,na,na,a,a)
    calc_pos(s,na,a,a,na)
    calc_pos(s,na,a,a,na*2)
    calc_pos(s,na*2,na*2,na,na)
    calc_pos(s,na*2,na,na,a)
    calc_pos(s,na*2,a,na,a*2)"""
print(time.strftime("%H:%M:%S", time.gmtime(time.time())))
while True:
    scan()
    if z0s > 3:
        z0s = 0
        time.sleep(90)
