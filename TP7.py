import pygame
import psutil
import cpuinfo
import platform
import os
# Cores:
preto = (0, 0, 0)
branco = (255, 255, 255)
cinza = (100, 100, 100)
vermelho = (255, 0, 0)
azul = (0, 0, 255)
verde = (0, 255, 0)

# Iniciando a janela principal
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Informações de CPU")
pygame.display.init()
# Superfície para mostrar as informações:
s1 = pygame.surface.Surface((largura_tela, altura_tela))

# Para usar na fonte
pygame.font.init()
font = pygame.font.Font(None, 24)
 
# Cria relógio
clock = pygame.time.Clock()
# Contador de tempo
cont = 60

class Cpu_detalhes:
    def __init__(self):
        self.x = 0
        
    def mostra_info_cpu(self):
      s1.fill(branco)
      self.mostra_texto(s1, "Nome:", "brand", 10)
      self.mostra_texto(s1, "Arquitetura:", "arch", 30)
      self.mostra_texto(s1, "Palavra (bits):", "bits", 50)
      self.mostra_texto(s1, "Frequência (MHz):", "freq", 70)
      self.mostra_texto(s1, "Núcleos (físicos):", "nucleos", 90)
      tela.blit(s1, (0, 0))
      
    def mostra_texto(self, s1, nome, chave, pos_y):
      text = font.render(nome, True, preto)
      s1.blit(text, (10, pos_y))
      if chave == "freq":
              s = str(round(psutil.cpu_freq().current, 2))
      elif chave == "nucleos":
              s = str(psutil.cpu_count())
              s = s + " (" + str(psutil.cpu_count(logical=False)) + ")"
      else:
              s = str(info_cpu[chave])
      text = font.render(s, True, cinza)
      s1.blit(text, (160, pos_y))

    def mostra_uso_cpu(self, s, l_cpu_percent):
          s.fill(cinza)
          num_cpu = len(l_cpu_percent)
          x = y = 10
          desl = 10
          alt = s.get_height() - 2*y
          larg = (s.get_width()-2*y - (num_cpu+1)*desl)/num_cpu
          d = x + desl
          for i in l_cpu_percent:
                      pygame.draw.rect(s, vermelho, (d, y, larg, alt))
                      pygame.draw.rect(s, azul,     (d, y, larg, (1-i/100)*alt))
                      d = d + larg + desl
          # parte mais abaixo da tela e à esquerda
          tela.blit(s, (0, altura_tela/5))

class Geral_detalhes:
    def __init__(self):
        self.Sys = processos()
        self.p= Painel()
        
        self.listaCPU = list()
        self.gCPU = Grafico()
        
        self.listaMemoria = list()
        self.gMemoria = Grafico()
        
        self.listaDisc = list()
        self.gDisc = Grafico()
        
        self.dic_interfaces = psutil.net_if_addrs()
        
    def carragar(self):
        tela.fill(branco)

        pygame.draw.rect(tela, preto, ((310,50), (470, 510)), 1)

        pygame.draw.rect(tela, preto, ((39,50), (240, 150)), 1)
        CPU = self.Sys.lerCPU()
        CPU_str = "Uso de CPU:"+str("{0:.2f}".format(round(CPU,2)))+"%"
        self.p.desenha(tela,CPU_str, preto,40,205,'Arial-bold')
        self.listaCPU = self.gCPU.moverGrafico(self.listaCPU, 40, 200-CPU*1.5, CPU*1.5, vermelho)
        for q in self.listaCPU:
            q.desenha(tela)

        pygame.draw.rect(tela, preto, ((39,230), (240, 150)), 1)
        Memoria = self.Sys.lerMemoria().percent
        Memoria_str = "Uso de Memória (Total: " + str(round( self.Sys.lerMemoria().total/(1024*1024*1024),2)) + "GB):"
        self.p.desenha(tela,Memoria_str, preto,40,385,'Arial-bold')
        self.listaMemoria = self.gMemoria.moverGrafico(self.listaMemoria, 40, 380-Memoria*1.5, Memoria*1.5, azul)
        for q in self.listaMemoria:
            q.desenha(tela)

        pygame.draw.rect(tela, preto, ((39,410), (240, 150)), 1)
        Disc = self.Sys.lerDisc().percent
        Disc_str = round(self.Sys.lerDisc().total/(1024*1024*1024), 2)
        self.p.desenha(tela,"Uso de Disco: (Total: " + str(Disc_str) + "GB)", preto,40,565,'Arial-bold')
        self.listaDisc = self.gDisc.moverGrafico(self.listaCPU, 40, 560-Disc*1.5, Disc*1.5, verde)
        for q in self.listaDisc:
            q.desenha(tela)

        self.p.desenha(tela,platform.node(), preto,330,60,'Arial')
        self.p.desenha(tela,platform.platform(), preto,330,80,'Arial')
        self.p.desenha(tela,'IMFORMAÇÃO REDE:', preto,330,130,'Arial-bold')
        i=0
        for dic in self.dic_interfaces:
            self.p.desenha(tela,dic, preto,330,150+i,'Arial')
            self.p.desenha(tela,self.dic_interfaces[dic][1].address, preto,330,170+i,'Arial')
            i = i+50

    def carragarMemoria(self):
        tela.fill(branco)
        pygame.draw.rect(tela, preto, ((39,50), (240, 150)), 1)
        Memoria = self.Sys.lerMemoria().percent
        Memoria_str = "Uso de Memória (Total: " + str(round( self.Sys.lerMemoria().used/(1024*1024*1024),2)) + "GB):"
        self.p.desenha(tela,Memoria_str, preto,40,205,'Arial-bold')
        self.listaMemoria = self.gMemoria.moverGrafico(self.listaMemoria, 40, 200-Memoria*1.5, Memoria*1.5, azul)
        for q in self.listaMemoria:
            q.desenha(tela)
            
        pygame.draw.rect(tela, preto, ((310,50), (470, 510)), 1)
        self.p.desenha(tela,platform.node(), preto,330,60,'Arial')
        self.p.desenha(tela,platform.platform(), preto,330,80,'Arial')
        self.p.desenha(tela,platform.processor(), preto,330,100,'Arial')
        
        Memoria_total = "Capacidade Total de Memória: "+ str(round( self.Sys.lerMemoria().total/(1024*1024*1024),2))+ "GB"
        Memoria_livre = "Memória Livre: "+ str(round( self.Sys.lerMemoria().available/(1024*1024*1024),2))+ "GB"
        Memoria_uso = "Memória em Uso: "+ str(round( self.Sys.lerMemoria().used/(1024*1024*1024),2))+ "GB"
        
        self.p.desenha(tela,'IMFORMAÇÃO MEMÓRIA:', preto,330,130,'Arial-bold')
        self.p.desenha(tela,Memoria_total, preto,330,170,'Arial')
        self.p.desenha(tela,Memoria_livre, preto,330,210,'Arial')
        self.p.desenha(tela,Memoria_uso, preto,330,250,'Arial')

            
    def carragarDisco(self):
        tela.fill(branco)
        pygame.draw.rect(tela, preto, ((39,50), (240, 150)), 1)
        Disc = self.Sys.lerDisc().percent
        Disc_str = round(self.Sys.lerDisc().used/(1024*1024*1024), 2)
        self.p.desenha(tela,"Uso de Disco: (Total: " + str(Disc_str) + "GB)", preto,40,205,'Arial-bold')
        self.listaDisc = self.gDisc.moverGrafico(self.listaCPU, 40, 200-Disc*1.5, Disc*1.5, verde)
        for q in self.listaDisc:
            q.desenha(tela)

        pygame.draw.rect(tela, preto, ((310,50), (470, 510)), 1)
        self.p.desenha(tela,platform.node(), preto,330,60,'Arial')
        self.p.desenha(tela,platform.platform(), preto,330,80,'Arial')
        self.p.desenha(tela,platform.processor(), preto,330,100,'Arial')
        
        Disc_total = "Capacidade Total da partição de Disco: "+ str(round( self.Sys.lerDisc().total/(1024*1024*1024),2))+ "GB"
        Disc_livre = " Espaço Livre: "+ str(round( self.Sys.lerDisc().free/(1024*1024*1024),2))+ "GB"
        Disc_uso = "Espaço em Uso: "+ str(round( self.Sys.lerDisc().used/(1024*1024*1024),2))+ "GB"
        
        self.p.desenha(tela,'IMFORMAÇÃO MEMÓRIA:', preto,330,130,'Arial-bold')
        self.p.desenha(tela,Disc_total, preto,330,170,'Arial')
        self.p.desenha(tela,Disc_livre, preto,330,210,'Arial')
        self.p.desenha(tela,Disc_uso, preto,330,250,'Arial')

    
    def carragarIp(self):
        tela.fill(branco)
        pygame.draw.rect(tela, preto, ((49,50), (700, 510)), 1)
        self.p.desenha(tela,platform.node(), preto,70,60,'Arial')
        self.p.desenha(tela,platform.platform(), preto,70,80,'Arial')
        self.p.desenha(tela,platform.processor(), preto,70,100,'Arial')
        self.p.desenha(tela,'IMFORMAÇÃO REDE:', preto,70,130,'Arial-bold')
        i=0
        for dic in self.dic_interfaces:
            self.p.desenha(tela,dic, preto,70,150+i,'Arial')
            self.p.desenha(tela,self.dic_interfaces[dic][1].address, preto,70,170+i,'Arial')
            i = i+50
    
    def lerListaProcessos(self):

        listaPNomes = list()
        for proc in psutil.process_iter():
           pDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent','memory_percent'])
           listaPNomes.append(pDict)
        tela.fill(branco)
        pygame.draw.rect(tela, preto, ((49,50), (700, 510)), 1)
        self.p.desenha(tela,platform.node(), preto,70,60,'Arial')
        self.p.desenha(tela,platform.platform(), preto,70,80,'Arial')
        self.p.desenha(tela,platform.processor(), preto,70,100,'Arial')
        self.p.desenha(tela,'PROCESSOS:', preto,70,130,'Arial-bold')
        i=0
        v=0
        
        for elem in listaPNomes:
            self.p.desenha(tela,'Nome: '+str(elem['name'])+' CPU: '+str(elem['cpu_percent'])+' Memória: '+str(elem['memory_percent']), preto,70,150+i,'Arial')
            v = v+1
            i = i+50
            if v==8:
                break
    
    def lerListaArquivos(self):
        dl = os.chdir('c:')
        dl = os.listdir()
        lista = []
        for ar in dl:
            if(os.path.isfile(ar)):
                nome = 'Arquivo: '+ar
            elif(os.path.isdir(ar)):
                nome = 'Diretorio: '+ar
            else:
                nome = 'Outros: '+ar
            tamanho = os.stat(ar).st_size
            ob = (nome,tamanho)
            
        ordenado = sorted(lista, key=lambda arquivos: arquivos[1], reverse=True)
        
        tela.fill(branco)
        pygame.draw.rect(tela, preto, ((49,50), (700, 510)), 1)
        self.p.desenha(tela,platform.node(), preto,70,60,'Arial')
        self.p.desenha(tela,platform.platform(), preto,70,80,'Arial')
        self.p.desenha(tela,platform.processor(), preto,70,100,'Arial')
        self.p.desenha(tela,'ARQUIVOS e DIRETÓRIOS da PARTIÇÃO:', preto,70,130,'Arial-bold')
        i=0
        v=0
        for el in ordenado:
            self.p.desenha(tela,''+str(el[0])+' / '+str(el[1])+' Bytes', preto,70,150+i,'Arial')
            v = v+1
            i = i+50
            if v==8:
                break

class processos():
    def __init__(self):
        self.CPU = None
        self.Memoria = None
        
    def lerCPU(self):
        self.CPU = psutil.cpu_percent(interval=1)
        return self.CPU
    
    def lerMemoria(self):
        self.Memoria = psutil.virtual_memory()
        return self.Memoria
    
    def lerDisc(self):
        self.Disc = psutil.disk_usage('C:')
        return self.Disc
    
class Grafico():
    def __init__(self):
        self.grafLista = list()
        
    def moverGrafico(self, lista, x, y, altura, cor):
        self.grafLista = lista
        q = Quadrado();
        q.setSelf(x, y, 10, altura, cor)
        
        if len(self.grafLista)== 0:
            self.grafLista.append(q)
            
        elif len(self.grafLista)<20:
            self.grafLista.append(None)
            
        for i in range(len(self.grafLista)):
            self.grafLista[len(self.grafLista)-(i+1)] = self.grafLista[len(self.grafLista)-(i+2)]
    
        for i in range(len(self.grafLista)):
            self.grafLista[i].setx((x +i*12))
            
        self.grafLista[0]=q
        
        return self.grafLista
    
#Classe dos objetos Quadrado
class Quadrado():
    def __init__(self):
        self.largura = None
        self.altura = None
        self.x = None
        self.y = None
        self.cor = None
    
    def setSelf(self, x, y, largura, altura, cor):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        
        self.cor = cor
    
    def setx(self,x):
        self.x = x
        
    def desenha(self, tel):
        area = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(tel,self.cor,area)
        
     
#Classe do painel       
class Painel():
    
    def __init__(self):
        self.size = 18
        self.cor = preto
        self.font = pygame.font.SysFont('Arial', self.size)

    def desenha(self,tel,aviso,cor,x,y,font):
        text_font = pygame.font.SysFont(font, self.size)
        text = text_font.render(aviso,2,cor)
        text_pos = (x,y)
        tel.blit(text, text_pos)

# Obtém informações da CPU
info_cpu = cpuinfo.get_cpu_info()

def main():
#Variaveis de iniciação
    terminou = False  
    cpuD = Cpu_detalhes()
    geralD = Geral_detalhes()
    surf = 1 
    cont = 0
    
    
    # Repetição para capturar eventos e atualizar tela
    while not terminou:
        # Checar os eventos do mouse aqui:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              terminou = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    surf = surf-1
                    if surf == 0:
                        surf = 7
                    if surf == 1:
                        cont = 0
                        cpuD = Cpu_detalhes()
                    if surf != 1:
                        geralD = Geral_detalhes()
                        
                elif event.key == pygame.K_RIGHT:
                    surf = surf+1              
                    if surf == 8:
                        surf = 1
                    if surf == 1:
                        cont = 0
                        cpuD = Cpu_detalhes()
                    if surf != 1:
                        geralD = Geral_detalhes()
        # Fazer a atualização a cada segundo:

        if surf == 1:
            if cont == 60:
                cpuD.mostra_info_cpu()
                CPU = psutil.cpu_percent(interval=1, percpu=True)
                cpuD.mostra_uso_cpu(s1, CPU)
                cont = 0
            
        if surf == 2: 
            geralD.carragarMemoria()
        if surf == 3:
            geralD.carragarDisco()
        if surf == 4:
            geralD.carragarIp()
        if surf == 5:
            geralD.carragar()
        if surf == 6:
            geralD.lerListaProcessos()
        if surf == 7:
            geralD.lerListaArquivos()


        pygame.display.update()
        clock.tick(60)
        cont = cont + 1

    pygame.quit()
    
if __name__ == '__main__':
    main()

