from random import randint, choices
import time
from datetime import date, timedelta
from collections import Counter

TIME_NAMES = [
    'Botafogo', 'Bragantino', 'Palmeiras', 'Flamengo', 'Athletico-PR',
    'Grêmio', 'Atlético-MG', 'Fluminense', 'Fortaleza', 'São Paulo',
    'Internacional', 'Ceará', 'Corinthians', 'Santos', 'Vasco', 'Bahia',
    'Atlético-GO', 'América-MG', 'Sport', 'Cuiabá']

POS = [
    "Goleiro", "Zagueiro Esquerdo", "Zagueiro Direito", "Lateral Direito",
    "Lateral Esquerdo", "Volante", "Meia Esquerda", "Meia Direita",
    "Ponta Esquerda", "Ponta Direita", "Atacante"]

peso_de_gols = [2, 3, 5, 8, 4, 6, 15, 4, 20, 25, 30]

with open('nomes.txt', 'r', encoding='utf8') as f:
  NAMES = f.read().splitlines()

class Pessoa():

  def __init__(self, nome, idade):
    self.nome = nome
    self.idade = idade

class Tecnico(Pessoa):

  def __init__(self, nome, idade, time_nome, carreira):
    super().__init__(nome, idade)
    self.time_nome = time_nome
    self.carreira = carreira

class Jogador(Pessoa):

  def __init__(self, nome, idade, posicao, n_camisa, gols):
    super().__init__(nome, idade)
    self.posicao = posicao
    self._num_camisa = n_camisa
    self.gols = gols

  def add_gols(self, gols):
    self.gols += gols

class Time():

  def __init__(self, time_nome, estadio):
    self.time_nome = time_nome
    self.estadio = estadio
    self.tecnico = ''
    self.jogadores = []
    self.pontos = 0

    self._add_jogador()
    self._add_tecnico()

  def _add_jogador(self):
    for i in range(11):
        
      j_name = choices(NAMES)
      #garantir que não vai ter nome diferente (NOVO)
      while j_name[0] in [j.nome[0] for j in self.jogadores]:
        j_name = choices(NAMES)
        
      self.jogadores.append(
          Jogador(j_name, randint(16, 38), POS[i], i + 1, 0))

  def _add_tecnico(self):
    old_time = TIME_NAMES[randint(0, len(TIME_NAMES) - 1)]

    while old_time == self.time_nome:
      old_time = TIME_NAMES[randint(0, len(TIME_NAMES) - 1)]

    self.tecnico = Tecnico(choices(NAMES), randint(30, 65), self.time_nome,
                           'Tecnico ja passou por ' + old_time)

  def _add_pontos(self, p):
    self.pontos += p

class Rodada():

  def __init__(self, times_obj):
  
    self._jogos = {}
    self.times = times_obj

    self.add_confrontos()

  def add_confrontos(self):

    jogos = {i: [] for i in range(1, 39)}

    for i in range(1, 39):
      
      for j in range(10):
        
        if i < 20:
          jogos[i].append([self.times[j], self.times[-1-j]])
        else:
          jogos[i].append([self.times[-1-j], self.times[j]])
          
      self.times.insert(1, self.times.pop())
    
    self._jogos = jogos

  def get_confrontos(self, n):
    
    confrontos = []
    jogadores_casa = []
    jogadores_fora = []
    quant_gols_casa = {}
    
    for i in range(10):
      gols = (randint(0, 5), randint(0, 5))  # (dentro_casa, fora_casa)

      if gols[0] == gols[1]:
          
        vencedor = 'empate'
        # Empate (NOVO, antes tinha outro if pra isso)
        self._jogos[n][i][0]._add_pontos(1)
        self._jogos[n][i][1]._add_pontos(1)
        
      else:
        vencedor = gols.index(max(gols))

      if vencedor != 'empate': # pontuação normal para vencedor
        self._jogos[n][i][vencedor]._add_pontos(3)

      #Time dentro de casa
      if gols[0] != 0:
          
        jogadores_casa = choices(self._jogos[n][i][0].jogadores, weights=peso_de_gols, k=gols[0])

        quant_gols_casa = Counter(jogadores_casa)
        
        for jogador in self._jogos[n][i][0].jogadores:

          for obj_jogador in quant_gols_casa:
            if jogador.nome[0] == obj_jogador.nome[0]:
              jogador.add_gols(quant_gols_casa[obj_jogador])

      #Time fora de casa
      if gols[1] != 0:
        jogadores_fora = choices(self._jogos[n][i][1].jogadores, weights=peso_de_gols, k=gols[1])

        quant_gols_fora = Counter(jogadores_fora)
        for jogador in self._jogos[n][i][1].jogadores:

          for obj_jogador in quant_gols_fora:
            if jogador.nome[0] == obj_jogador.nome[0]:
              jogador.add_gols(quant_gols_fora[obj_jogador])

      data =  date.today() + (n * timedelta(7))

      confrontos.append(
          Confronto(
              self._jogos[n][i][0].estadio, self._jogos[n][i][0],
              self._jogos[n][i][1],
              f'Resultado: {self._jogos[n][i][vencedor].time_nome} vencedor'
              if vencedor != 'empate' else vencedor, data,
              f'{self._jogos[n][i][0].time_nome} {gols[0]} X {gols[1]} {self._jogos[n][i][1].time_nome}'
          ))

    return confrontos


class Confronto():

  def __init__(self, estadio, time1, time2, resultado, data, placar):
    self.estadio = estadio
    self.data = data
    self.time1 = time1
    self.time2 = time2
    self.resultado = resultado
    self.placar = placar

class Brasileirao():

  def __init__(self):
      
    self.__times = []
    
    self.__rodadas = {}
    self.n_rodada = 0
    
    self.__confrontos = {}
    self._classificacao = {}
    
    self._jogadoresQntGols = {}

    self._add_times()
    self._add_rodada()

  def _add_times(self):
    for i in range(20):
      self.__times.append(Time(TIME_NAMES[i], TIME_NAMES[i] + ' Arena'))

  def _add_rodada(self):
    self.__rodadas = Rodada(self.__times)


  def get_times(self):
    for time in self.__times:
      
      print(f'Time: {time.time_nome} - Estadio: {time.estadio}')
      
      print(f'\tTecnico: {time.tecnico.nome[0]} - Carreira: {time.tecnico.carreira}')
      
      for jogador in time.jogadores:
        print(
            f'\tJogador: {jogador.nome[0]} - Camisa: {jogador._num_camisa} - Posicao: {jogador.posicao} - Gols: {jogador.gols}'
        )
      print('\n')

  def gerar_rodadas(self, n_rodada):

    self.__confrontos[n_rodada] = self.__rodadas.get_confrontos(n_rodada)
    self.n_rodada = len(self.__confrontos)

  def get_rodadas(self, n_rodada):
        print(f'Rodada {n_rodada}')
        for i in self.__confrontos[n_rodada]:
            print(f'{i.data} {i.placar}')
        
  def get_artilheiros(self):
    
    aux_jogadores_gols = []
    
    for time in self.__times:
    
      for jogador in time.jogadores:
     
        try:
          self._jogadoresQntGols[time.time_nome].update({jogador.nome[0]: (jogador.gols, time.time_nome)})
        except:
          self._jogadoresQntGols[time.time_nome] = {jogador.nome[0]: (jogador.gols, time.time_nome)}
    
    for time in self._jogadoresQntGols:
      
      self._jogadoresQntGols[time] = sorted(self._jogadoresQntGols[time].items(), key=lambda x: x[1], reverse=True)
      aux_jogadores_gols = aux_jogadores_gols + self._jogadoresQntGols[time]
      aux_jogadores_gols = sorted(aux_jogadores_gols, key=lambda x: x[1], reverse=True)
      
    pos = 1
    
    for i in aux_jogadores_gols:  
    
      if pos > 5:
        break
      
      print(f'{pos}º {i[0]} - {i[1][0]} gols - {i[1][1]}')
      pos += 1  
    
  def get_classificacao(self):
    
    for time in self.__times:
      try:        
          self._classificacao[time.pontos].append(time.time_nome)
      except:
          self._classificacao[time.pontos] = [time.time_nome]

    pos = 1

    for i in sorted(self._classificacao, reverse=True):
      for time in self._classificacao[i]:
          print(f'{pos}ª {time} - {i}')
          pos += 1
          
    self._classificacao = {}

def menu(r):
  
  print('-=-=-=-=-=-Campeonato Brasileiro-=-=-=-=-=-')
  print('Ver times: 1')
  
  if r >= 39:
    print(f'Ver rodada {38}: 2')
  else:
    print(f'Ver rodada {r}: 2')
    
  print('Ver artilheiros: 3')
  print('Ver classificação: 4')
  print('Ver um rodada específica: 5')
  print('Qual rodada estamos: 6')
  print('Reiniciar: 7')
  print('Sair: 8')
  print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
  
def choice(input_choice, rodada):
  
  global brasileirao
  
  if input_choice == '1':
    brasileirao.get_times()
    
  elif input_choice == '2':
    
    if rodada >= 39:
      print('As rodadas acabaram, se deseja reiniciar o campeonato digite 5')
      rodada = 38
      
    #ANIMAÇÃO DOS 3 PONTINHOSSSSS
  
    # symbols = ['', '', '.', '.', '..', '..', '...', '...']
    # i = 0
    # a = 0
    
    # while a < 15:
      
    #   i = (i + 1) % len(symbols)
    #   print('\r\033[KOs times estão jogando%s' % symbols[i], flush=True, end='')
      
    #   time.sleep(0.2)
    #   a += 1
    # print('\n')
    
    brasileirao.gerar_rodadas(rodada)
    brasileirao.get_rodadas(rodada)
    rodada += 1
  
  elif input_choice == '3':
    
    print('\n')
    brasileirao.get_artilheiros()
    print('\n')
    
  elif input_choice == '4':
    
    print('\n')
    brasileirao.get_classificacao()
    print('\n')

  elif input_choice == '5':
    input_rodada = int(input('Digite o número da rodada: '))
    
    if input_rodada > 38 or (rodada == 1 and input_rodada > 1):
      print('Rodada inválida')
      
    else:
      brasileirao.get_rodadas(input_rodada)
    
  elif input_choice == '6':
    print(f'Rodada {rodada}')
    
  elif input_choice == '7':
    rodada = 1
    brasileirao = Brasileirao()
    
  else:
    print('Opção inválida')
  
  return rodada

if __name__ == '__main__':
  
  rodada = 1
  brasileirao = Brasileirao()
  input_choice = 0
  
  while True:
    
    menu(rodada)
    input_choice = input('Escolha uma opção: ')
    
    if input_choice == '8':
      print('Programa encerrado')
      break
    
    rodada = choice(input_choice, rodada)
    
