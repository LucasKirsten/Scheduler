# -*- coding: utf-8 -*-

# classe para os horários
class Dia(object):
    # inicialização da classe
    # precisa da variável gerada pelo pandas que dá o dia da semana
    def __init__(self,diaSemana, nome):
        self.diaSemana = diaSemana
        self.nome = nome
        
        # vetor que armazena os objetos hora
        self.vetorHora = []
        
        self.separaHora()
        self.vetorHora = self.organizaHoras(self.vetorHora)

    # função separa as horas e as armazena do vetor de horas como objetos
    def separaHora(self):
        diaSemana = self.diaSemana
        
        vetorHora = self.vetorHora       
        
        # itera sobre cada um dos horarios
        for hora in diaSemana:
            # adquire a informação das pessoas
            membro = diaSemana.get(str(hora)) 
            
            # variável que armazenará os dados de disponibilidade de cada membro
            aux = ''
            
            # itera sobre as informações de cada membro
            for info in membro:
                aux = aux+info
            
            # conta nro de pessoas disponíveis naquele horário
            nroDisponiveis = aux.count('S')
            nroTalvez = aux.count('T')
            nroIndisponivel = aux.count('N')
            
            # vetores contendo as pessoas disponiveis, talvez e indisponiveis
            vetorDisponivel = []
            vetorTalvez = []
            vetorIndisponivel = []
            
            # itera sobre os membros            
            for pessoa in diaSemana.index:
                if diaSemana[hora][pessoa]=='S':
                    vetorDisponivel.append(pessoa)
                if diaSemana[hora][pessoa]=='T':
                    vetorTalvez.append(pessoa)
                if diaSemana[hora][pessoa]=='N':
                    vetorIndisponivel.append(pessoa)
                    
            # variável auxiliar que armazena uma hora criada
            aux = Hora(hora,nroDisponiveis,nroTalvez,nroIndisponivel,vetorDisponivel,vetorTalvez,vetorIndisponivel)
            
            # armazena a varíavel auxiliar ao vetor de horas
            vetorHora.append(aux)
        
        self.vetorHora = vetorHora
    
    # organiza as horas em ordem decrescente de pessoas disponíveis
    def organizaHoras(self, vetorHora):
        
        # organiza as horas em ordem crescente de pessoas talvez
        # baseado no algoritmo *BUBBLE SORT*
        for fim in range(len(vetorHora)-1,-1,-1):
            for i in range(0,fim):
                if vetorHora[i].getNumTalvez() > vetorHora[i+1].getNumTalvez():
                    aux = vetorHora[i]
                    vetorHora[i] = vetorHora[i+1]
                    vetorHora[i+1] = aux
                    
        # organiza as horas em ordem crescente de pessoas disponíveis
        # algoritmo baseado no *BUBBLE SORT*
        for fim in range(len(vetorHora)-1,-1,-1):
            for i in range(0,fim):
                if vetorHora[i].getNumDisponivel() > vetorHora[i+1].getNumDisponivel():
                    aux = vetorHora[i]
                    vetorHora[i] = vetorHora[i+1]
                    vetorHora[i+1] = aux
        
        # organiza as horas em ordem decrescente
        vetorHora = vetorHora[::-1]
        
        return vetorHora

    # retorna o vetor com o nome de todas as pessoas em ordem alfabética
    def getPessoas(self):
        vetorPessoas = []
        for pessoa in self.diaSemana.index.sort_values():
            vetorPessoas.append(pessoa)
        return vetorPessoas
    
    # retorna qual o dia da semana
    def getDia(self):
        return self.nome
        
    # retorna o vetor de horas de todas as pessoas
    def getVetorHora(self):
        return self.vetorHora
        
    # seleciona os horários que determinadas pessoas devam *obrigatoriamente* comparecer
    # vetorPessoas é um vetor com o nome das pessoas obrigatórias
    def getVetorHoraSelecionada(self, vetorPessoas, vetorHora):

        diaSemana = self.diaSemana

        # vetor contendo as horas que devem ser excluidas
        horasExcluidas = []
        
        # itera sobre os objetos hora
        for hora in vetorHora:
            # pega o nome da hora
            horario = hora.getHora()
            # itera sobre as pessoas do grupo de exclusão
            for pessoa in vetorPessoas:
                # verifica se essa pessoa está indisponível ou talvez no horário
                if diaSemana[horario][pessoa]=='N' or diaSemana[horario][pessoa]=='T':
                    # verifica se a hora já não está no vetor
                    if hora not in horasExcluidas:
                        # armazena a hora no vetor
                        horasExcluidas.append(hora)
        
        # remove as horas do vetor de horas
        for hora in horasExcluidas:           
            vetorHora.remove(hora)
            
        return vetorHora
        
    # retorna o vetor hora para um determinado grupo
    # recebe um objeto do tipo Grupo
    def getVetorHoraGrupo(self, grupo):
        
        diaSemana = self.diaSemana
        
        # vetor contendo as pessoas do grupo
        vetorGrupo = grupo.getPessoas()
        
        # vetor com o nome das pessoas a serem removidas da serie
        pessoasRemovidas = []
        
        # armazena no vetor de pessoas removidas as pessoas que não estão no grupo
        for pessoa in diaSemana.index:
            if pessoa not in vetorGrupo:
                pessoasRemovidas.append(pessoa)
            
        # remove as pessoas que não estão no grupo selecionado
        diaSemana = diaSemana.drop(pessoasRemovidas)

        vetorHora = []
        
        # itera sobre cada um dos horarios
        for hora in diaSemana:
            
            # adquire a informação das pessoas
            membro = diaSemana.get(str(hora))
            
            # variável que armazenará os dados de disponibilidade de cada membro
            aux = ''
            
            # itera sobre as informações de cada membro
            for info in membro:
                aux = aux+info
            
            # conta nro de pessoas disponíveis naquele horário
            nroDisponiveis = aux.count('S')
            nroTalvez = aux.count('T')
            nroIndisponivel = aux.count('N')
            
            # vetores contendo as pessoas disponiveis, talvez e indisponiveis
            vetorDisponivel = []
            vetorTalvez = []
            vetorIndisponivel = []
            
            # itera sobre os membros            
            for pessoa in diaSemana.index:
                if diaSemana[hora][pessoa]=='S':
                    vetorDisponivel.append(pessoa)
                if diaSemana[hora][pessoa]=='T':
                    vetorTalvez.append(pessoa)
                if diaSemana[hora][pessoa]=='N':
                    vetorIndisponivel.append(pessoa)
                    
            # variável auxiliar que armazena uma hora criada
            aux = Hora(hora,nroDisponiveis,nroTalvez,nroIndisponivel,vetorDisponivel,vetorTalvez,vetorIndisponivel)
            
            # armazena a varíavel auxiliar ao vetor de horas
            vetorHora.append(aux)
        
        # organiza as horas
        vetorHora = self.organizaHoras(vetorHora)        
        
        return vetorHora
        
        
# classe para uma hora
class Hora(object):
    # inicializa com a hora, nro de pessoas disponiveis, nro de talvez, nome dos membros disponiveis e talvez(vetor)
    def __init__(self,hora,disponivel,talvez,indisponivel,pessoaDisponivel,pessoaTalvez,pessoaIndisponivel):
        self.hora = hora
        self.disponivel = disponivel
        self.talvez = talvez
        self.indisponivel = indisponivel
        # vetores
        self.pessoaDisponivel = pessoaDisponivel
        self.pessoaTalvez = pessoaTalvez
        self.pessoaIndisponivel = pessoaIndisponivel
        
    # getters
        # string
    def getHora(self):
        return self.hora
        # números
    def getNumDisponivel(self):
        return self.disponivel
    def getNumTalvez(self):
        return self.talvez
    def getNumIndisponivel(self):
        return self.indisponivel
        # vetores com nome das pessoas
    def getDisponivel(self):
        return self.pessoaDisponivel
    def getTalvez(self):
        return self.pessoaTalvez
    def getIndisponivel(self):
        return self.pessoaIndisponivel
        
    # setters
    def setNumDisponivel(self, disp):
        self.disponivel = disp
    def setNumTalvez(self,talvez):
        self.talvez = talvez
    def setNumIndisponivel(self, ind):
        self.indisponivel = ind
        # vetores
    def setDisponivel(self, disp):
        self.pessoaDisponivel = disp
    def setTalvez(self, talvez):
        self.pessoaTalvez = talvez
    def setIndisponivel(self, ind):
        self.pessoaIndisponivel = ind
        
# classe de um grupo de pessoas
class Grupo (object):
    # inicialização
    # recebe um vetor contendo o nome das pessoas do grupo e o nome do grupo
    def __init__(self, pessoas, nome=None):
        self.pessoas = pessoas
        self.nome = nome
        
    # setters
    def setPessoas(self, novasPessoas):
        self.pessoas = novasPessoas
    def setNome(self, novoNome):
        self.nome = novoNome
    
    # getters
    def getPessoas(self):
        return self.pessoas
    def getNome(self):
        return self.nome
        
    # adiciona uma pessoa ao grupo
    def addPessoa(self, pessoa):
        self.pessoas.append(pessoa)
    # exclui uma pessoa do grupo
    def delPessoa(self, pessoa):
        # verifica se a pessoa já estava na lista
        if pessoa in self.pessoas:
            self.pessoas.remove(pessoa)
        else:
            print "Pessoa não estava originalmente na lista"


# função que escolhe o melhor dia e horario para reunião
# recebe um vetor contendo objetos do tipo Dia com todos os dias da semana a serem analisados
def escolherData(dias):
    
    # ordena os dias da semana com base no número de disponíveis em ordem crescente
    # algoritmo baseado no *BUBBLE SORT*
    for fim in range(len(dias)-1,-1,-1):
        for i in range(0,fim):
            # ajeitar essa linha de acordo com o time de reunião que deve ser feita
            if dias[i].getVetorHoraGrupo(projetoRobotica)[0].getNumDisponivel() > dias[i+1].getVetorHoraGrupo(projetoRobotica)[0].getNumDisponivel():
                aux = dias[i]
                dias[i] = dias[i+1]
                dias[i+1] = aux
     
    # inverte o vetor dias para se ter em ordem decrescente
    dias = dias[::-1]
    
    # texto com os horários
    texto = ""
    
    texto = texto + "Melhores dias para reuniao:\n\n"
    
    # itera sobre os dias
    for d in dias:
        texto = texto + d.getDia()+'\n'
        
        # itera sobre as horas
        for hora in d.getVetorHoraGrupo(projetoRobotica):
            texto = texto + "\nHorario: "+hora.getHora()
            texto = texto + "\n\tDisponiveis: "+str(hora.getNumDisponivel())
            
            # itera sobre as pessoas disponíveis
            for disp in hora.getDisponivel():
                texto = texto + "\n\t\t"+disp+"; "
            
            texto = texto + "\n\tTalvez: "+str(hora.getNumTalvez())
        
            # itera sobre as pessoas talvez
            for talvez in hora.getTalvez():
                texto = texto + "\n\t\t"+talvez+"; "
        
            texto = texto + "\n\tIndisponivel: "+str(hora.getNumIndisponivel())
                
            for indisponivel in hora.getIndisponivel():
                texto = texto + "\n\t\t"+indisponivel+"; "
                
        texto = texto + "\n---------------------------------\n\n"
        
    # manipulação de um txt pra colocar os horários
    arquivo = open('horarios.txt','w')
    arquivo.write(texto)
    arquivo.close()