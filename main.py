from random import randint, choices
from random import shuffle
from time import sleep

TIME_NAMES = ['Botafogo','Bragantino', 'Palmeiras', 'Flamengo', 'Athletico-PR', 'Grêmio', 'Atlético-MG', 'Fluminense', 'Fortaleza', 'São Paulo', 'Internacional', 'Ceará', 'Corinthians', 'Santos', 'Vasco', 'Bahia', 'Atlético-GO', 'América-MG', 'Sport', 'Cuiabá']
POS = ["Goleiro", "Zagueiro Esquerdo", "Zagueiro Direito", "Lateral Direito", "Lateral Esquerdo", "Volante", "Meia Esquerda", "Meia Direita", "Ponta Esquerda", "Ponta Direita", "Atacante"]

with open('nomes.txt', 'r', encoding='utf8') as f:
    NAMES = f.read().splitlines()

class Pessoa():
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

class Jogador(Pessoa):
    def __init__(self, nome, idade, posicao, numero, gols):
        super().__init__(nome, idade)
        self.posicao = posicao
        self.numero = numero
        self.gols = gols

    def add_gols(self, gols):
        self.gols = gols

        
class Tecnico(Pessoa):
    def __init__(self, nome, idade, time, carreira):
        super().__init__(nome, idade)
        self.time = time
        self.carreira = carreira

class Time():
    def __init__(self, time):
        
        self.time = time
        self.jogadores = []
        self.tecnico = ''
        self.estadio = ''

        self.add_estadio()
        self.add_jogador()
        self.add_tecnico()

    def add_jogador(self):

        for i in range(11):
            self.jogadores.append(Jogador(choices(NAMES), randint(16, 38), POS[i], i + 1, 0))       
    
    def add_tecnico(self):

        old_time = TIME_NAMES[randint(0, len(TIME_NAMES) - 1)]

        while old_time == self.time:
            old_time = TIME_NAMES[randint(0, len(TIME_NAMES) - 1)]

        self.tecnico = Tecnico(choices(NAMES), randint(30, 65), self.time, 'Tecnico ja passou por ' + old_time)

    def add_estadio(self):
        self.estadio = self.time + ' Arena'

class Confronto():
    def __init__(self, times):

        self.times = times
        self.placar = [0, 0]
        self.resultado = ''
        self.estadio = ''
        self.data = ''
        self.confrontos = self.create_rodadas()

    def create_rodadas(self):
        
        times_dentro = self.times[:10]
        times_fora = self.times[10:]

        print(len(times_dentro), len(times_fora))

        confrontos = {
            '1': [],
            '2': [],
            '3': [],
            '4': [],
            '5': [],
            '6': [],
            '7': [],
            '8': [],
            '9': [],
            '10': [],
            '11': [],
            '12': [],
            '13': [],
            '14': [],
            '15': [],
            '16': [],
            '17': [],
            '18': [],
            '19': [],
            '20': [],
            '21': [],
            '22': [],
            '23': [],
            '24': [],
            '25': [],
            '26': [],
            '27': [],
            '28': [],
            '29': [],
            '30': [],
            '31': [],
            '32': [],
            '33': [],
            '34': [],
            '35': [],
            '36': [],
            '37': [],
            '38': [],
        }

        for i in range(1, 39):

            for j in range(10):

                if i < 20:
                    confrontos[str(i)].append([times_dentro[j].time, times_fora[j].time])

                else:
                    confrontos[str(i)].append([times_fora[j].time, times_dentro[j].time])
                    
            times_dentro.insert(1, times_fora.pop())
            times_fora.insert(0, times_dentro.pop())

        return confrontos

            
class Rodada():
    def __init__(self, TIMES):
        self.times = TIMES
        self.rodada = 'rodada'
        self.jogos = {}
        self.add_jogos()

    def add_jogos(self):
        self.jogos = Confronto(self.times)
        print(self.jogos.confrontos)

class Brasileirao():

    def __init__(self):

        self.times = []
        self.rodadas = []
        self.rodada_atual = 0

        self.add_time()
        self.add_rodada()

    def get_rodada(self, i):

        return self.rodadas
    
    def add_rodada(self):
        
           
        self.rodadas.append(Rodada(self.times))


    def add_time(self):

        for i in range(20):
            self.times.append(Time(TIME_NAMES[i]))

        print('Times adicionados com sucesso!')

    def get_times(self):
        for i in range(len(self.times)):
            print(f'time: {self.times[i].time}')
            for j in range(len(self.times[i].jogadores)):
                print(self.times[i].jogadores[j].nome, self.times[i].jogadores[j].posicao, self.times[i].jogadores[j].numero, self.times[i].jogadores[j].idade,self.times[i].jogadores[j].gols)


campeonato = Brasileirao()
campeonato.get_rodada(0)
