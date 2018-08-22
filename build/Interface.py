# -*- coding: utf-8 -*-

# importa as classes de dias, grupos e hora
from Organizacao import *
# importa o tkinter
from Tkinter import *
# importa a caixa de mensagem
import tkMessageBox
# importa pandas (trabalho com dados do excel)
import pandas as pd
# importa pickle (trabalha com a serialização de objetos para um arquivo)
# .dumps(objeto) - > serializa ; .loads(texto) -> cria objeto serializado
import pickle as pk
# importa o módulo os (lida com ambientes de pastas)
import os

# variáveis globais
    # fontes
global PRINCIPAL 
PRINCIPAL = ('Arial', '14', 'bold') #títulos
global INFO
INFO = ('Arial', '12') #informações

# essa vai ser a classe fodona que inicializa toda a interface
class Interface(object): 
    
    # inicialização da classe
    def __init__(self,root):
        
        # cria a pasta que irá conter as informações necessárias para o programa rodar
        try:
            os.mkdir('build')
        except:
            pass
        
        # inicialização do layout
        self.root = root
        # definições da janela
        root.geometry("1200x400+100+100")
        root.minsize(width='1200', height='400')
        root.title('Scheduler BETA')
        
        # inicializa os dias da semana        
        self.initDiasSemana()
        
        # MENUS
        menubar = Menu(root)
        
            # Novo
        novoMenu = Menu(menubar, tearoff=0)
                # Reunião
        novoMenu.add_command(label='Nova Reunião', command=self.novaReuniao,accelerator="Ctrl+R")
        # atalho
        root.bind('<Control-r>', self.novaReuniao)
                # Grupo
        novoMenu.add_command(label='Novo Grupo', command=self.novoGrupo,accelerator="Ctrl+G")
        # atalho
        root.bind('<Control-g>', self.novoGrupo)
        # mostra o menu
        menubar.add_cascade(label='Novo', menu=novoMenu)
        
            # Opções
        opcoesMenu = Menu(menubar, tearoff=0)
                # Editar Grupo
        opcoesMenu.add_command(label='Editar Grupo', command=self.editarGrupo,accelerator="Ctrl+E")
        # atalho
        root.bind('<Control-e>', self.editarGrupo)
                # Excluir Grupo
        opcoesMenu.add_command(label='Excluir Grupo', command=self.excluirGrupo,accelerator="Ctrl+X")
        # atalho
        root.bind('<Control-x>', self.excluirGrupo)
        # mostra o menu
        menubar.add_cascade(label='Opções', menu=opcoesMenu)
        
            # Ajuda
        ajudaMenu = Menu(menubar, tearoff=0)
                # Sobre
        ajudaMenu.add_command(label='Sobre', command=self.sobre)
                # Tutoriais
        ajudaMenu.add_command(label='Tutoriais', command=self.tutoriais)
        # mostra o menu
        menubar.add_cascade(label='Ajuda', menu=ajudaMenu)
        
        # faz a configuração dos menus
        root.config(menu=menubar)
    
    # inicializa os dias da semana
    def initDiasSemana(self):
        # abre o arquivo do excel
        try:
            horarios = pd.ExcelFile('build\Horarios.xlsx')
        except:
            tkMessageBox.showerror('ERRO DE ABERTURA', 'NÃO FOI POSSÍVEL ABRIR A TABELA DE HORÁRIOS!\nVERIFIQUE SE A TABELA ESTÁ NA PASTA CORRETA.', parent=self.root)
            self.root.destroy()
            return -1
        
        # abre a tabela de cada dia
        try:
            segunda = horarios.parse('Segunda')
        except:
            tkMessageBox.showerror('ERRO DE ABERTURA', 'NÃO FOI POSSÍVEL ABRIR A TABELA DE SEGUNDA!\nVERIFIQUE SE A TABELA EXISTE DENTRO DOS HORÁRIOS.', parent=self.root)
            self.root.destroy()
            return -1
        try:
            terca = horarios.parse('Terca') 
        except:
            tkMessageBox.showerror('ERRO DE ABERTURA', 'NÃO FOI POSSÍVEL ABRIR A TABELA DE TERÇA!\nVERIFIQUE SE A TABELA EXISTE DENTRO DOS HORÁRIOS.', parent=self.root)
            self.root.destroy()
            return -1
        try:
            quarta= horarios.parse('Quarta')
        except:
            tkMessageBox.showerror('ERRO DE ABERTURA', 'NÃO FOI POSSÍVEL ABRIR A TABELA DE QUARTA!\nVERIFIQUE SE A TABELA EXISTE DENTRO DOS HORÁRIOS.', parent=self.root)
            self.root.destroy()
            return -1
        try:
            quinta= horarios.parse('Quinta')
        except:
            tkMessageBox.showerror('ERRO DE ABERTURA', 'NÃO FOI POSSÍVEL ABRIR A TABELA DE QUINTA!\nVERIFIQUE SE A TABELA EXISTE DENTRO DOS HORÁRIOS.', parent=self.root)
            self.root.destroy()
            return -1
        try:
            sexta = horarios.parse('Sexta')   
        except:
            tkMessageBox.showerror('ERRO DE ABERTURA', 'NÃO FOI POSSÍVEL ABRIR A TABELA DE SEXTA!\nVERIFIQUE SE A TABELA EXISTE DENTRO DOS HORÁRIOS.', parent=self.root)
            self.root.destroy()
            return -1
        
            # inicialização dos objetos dos dias da semana
        try:
            self.segunda = Dia(segunda,'SEG')
            self.terca = Dia(terca, 'TER')
            self.quarta = Dia(quarta, 'QUA')
            self.quinta = Dia(quinta, 'QUI')
            self.sexta = Dia(sexta, 'SEX') 
        except:
            tkMessageBox.showerror('ERRO', 'NÃO HÁ INFORMAÇÃO DE HORÁRIO DE ALGUMA PESSOA!\nVERIFIQUE SE EM ALGUMA TABELA HÁ INFORMAÇÃO NÃO PREENCHIDA.', parent=self.root)
            self.root.destroy()
            return -1
        
        # verifica se há o mesmo número de pessoas em cada dia
        tamanho = len(self.segunda.getPessoas())
        if (len(self.terca.getPessoas())!=tamanho or len(self.quarta.getPessoas())!=tamanho or len(self.quinta.getPessoas())!=tamanho or len(self.sexta.getPessoas())!=tamanho):
            tkMessageBox.showerror('ERRO', 'O NÚMERO DE PESSOAS EM CADA DIA DA SEMANA É DIFERENTE!\nVERIFIQUE SE TODAS AS PESSOAS ESTÃO EM TODAS AS TABELAS.', parent=self.root)
            self.root.destroy()
            return -1
        if (len(self.segunda.getPessoas())==0 or len(self.terca.getPessoas())==0 or len(self.quarta.getPessoas())==0 or len(self.quinta.getPessoas())==0 or len(self.sexta.getPessoas())==0):
            tkMessageBox.showerror('ERRO', 'NÃO HÁ PESSOAS EM ALGUMA DAS TABELAS!', parent=self.root)
            self.root.destroy()
            return -1
        
        # vetor com os dias da semana
        self.vetorDias = [self.segunda, self.terca, self.quarta, self.quinta, self.sexta]
    
    def novaReuniao(self, event=None):
        # muda o nome para identificar qual a função esta sendo executada
        self.root.title('Scheduler - Nova Reunião')
        # destrói a frame atual que está sendo usada
        try:
            self.framePrincipal.destroy()
        except:
            pass
        self.framePrincipal = Frame(self.root)
        # inicializa a classe
        NovaReuniao(self.framePrincipal,self.segunda,self.vetorDias)
    
    def novoGrupo(self, event=None):
        # muda o nome para identificar qual a função esta sendo executada
        self.root.title('Scheduler - Novo Grupo')
        # destrói a frame atual que está sendo usada
        try:
            self.framePrincipal.destroy()
        except:
            pass
        self.framePrincipal = Frame(self.root)
        # inicializa a classe
        NovoGrupo(self.framePrincipal,self.segunda)
        
    def editarGrupo(self, event=None):
        # muda o nome para identificar qual a função esta sendo executada
        self.root.title('Scheduler - Editar Grupo')
        # destrói a frame atual que está sendo usada
        try:
            self.framePrincipal.destroy()
        except:
            pass
        self.framePrincipal = Frame(self.root)
        # inicializa a classe
        EditarGrupo(self.framePrincipal,self.segunda)
        
    def excluirGrupo(self, event=None):
        # muda o nome para identificar qual a função esta sendo executada
        self.root.title('Scheduler - Excluir Grupo')
        # destrói a frame atual que está sendo usada
        try:
            self.framePrincipal.destroy()
        except:
            pass
        self.framePrincipal = Frame(self.root)
        # inicializa a classe
        ExcluirGrupo(self.framePrincipal)
        
    def sobre(self, event=None):
        tkMessageBox.showinfo('Sobre','Programa Scheduler\n'
                              'Versão BETA\n\n'
                              'Desenvolvido por Sinc Jr\n')
    
    def tutoriais(self, event=None):
        os.system('build\Tutorial.pdf')
        
# a classe NovoGrupo herda os atributos e métodos da classe Interface
class NovoGrupo(Interface):
    # recebe a frame para a nova reunião que foi criada em Interface
    def __init__(self, frame, diaSemana):
        
        # inicialização da frame
        self.frame = frame
        self.frame.pack()
        
        # vetor contendo todas as pessoas
        self.vetorPessoas = diaSemana.getPessoas()
        
        # vetor selecionados
        self.vetorSelecionados = []
        
        # SELECIONAR PESSOA
        label = Label(self.frame, text="Selecionar Pessoas:", font=PRINCIPAL).grid(row=0,column=0,padx=40,pady=20)
            # cria uma frame para armazenar os objetos com scroll
        def myfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=200)
        frameSeleciona=Frame(self.frame,relief=GROOVE,width=50,height=100,bd=1)
        frameSeleciona.grid(row=1,column=0,padx=40,pady=20)
        
        canvas=Canvas(frameSeleciona)
        frameInterna=Frame(canvas)
        myscrollbar=Scrollbar(frameSeleciona,orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=myscrollbar.set)
        
        myscrollbar.pack(side="right",fill="y")
        canvas.pack(side="bottom")
        canvas.create_window((0,0),window=frameInterna,anchor='nw')
        frameInterna.bind("<Configure>",myfunction)
        
        # função para marcar/desmarcar todas pessoas        
        def selecionarTodos():
            # se todas as pessoas estavam marcadas, desmarca todas
            if len(self.vetorPessoas)==len(self.vetorSelecionados):
                self.checkTodos.deselect()
                # limpa o vetor com as pessoas selecionadas
                self.vetorSelecionados=[]
                # desmarca todos
                for b in self.vetorChecks:
                    b.deselect()
                # deleta todas as pessoas que foram adicionadas a listbox
                self.listbox.delete(0,len(self.vetorPessoas))
                
            # caso tivessem pessoas que não estavam no vetor, marca todas
            else:
                self.checkTodos.select()
                # adiciona todas as pessoas ao vetor
                self.vetorSelecionados = self.vetorPessoas
                # marca todos
                for b in self.vetorChecks:
                    b.select()
                # deleta todas as pessoas que foram adicionadas a listbox para atualiza-lá corretamente
                self.listbox.delete(0,len(self.vetorPessoas))
                # adiciona todas as pessoas a listbox
                for pessoa in self.vetorSelecionados:
                    self.listbox.insert(self.vetorSelecionados.index(pessoa),pessoa)
                
        # o primeiro checkbutton é o para marcar/desmarcar todas pessoas
        self.checkTodos = Checkbutton(frameInterna, text="Marcar/Desmarcar Todos", font=INFO, command=selecionarTodos)
        self.checkTodos.deselect()
        self.checkTodos.pack(side=TOP, anchor='w')
        # armazena todos os checkbuttons dentro de um vetor para poder marcar/desmarcar todos
        self.vetorChecks = []
        # itera sobre as pessoas no vetor contendo todas pessoas
        for pessoa in self.vetorPessoas:
            # cria uma função que envia o nome da pessoa sempre que o checkbutton for clicado
            comando = lambda x=pessoa:self.verificaPessoa(x)
            # cria o checkbutton com o nome da pessoa
            check = Checkbutton(frameInterna, text=pessoa, font=INFO, command=comando)
            check.deselect()
            check.pack(side=TOP, anchor='w')
            # adiciona o checkbutton ao vetor
            self.vetorChecks.append(check)       
        
        # PESSOAS SELECIONADAS
        label = Label(self.frame, text="Pessoas Selecionadas:", font=PRINCIPAL).grid(row=0,column=1,padx=40,pady=20)
            # cria uma frame para armazenar os objetos com scroll
        frameSelecionado = Frame(self.frame)
        frameSelecionado.grid(row=1, column=1, padx=25)
            # cria a scroll bar para a listbox
        scrollbar = Scrollbar(frameSelecionado)
        scrollbar.pack(side=RIGHT, fill=Y)
            # cria um listbox que irá armazenar o nome das pessoas selecionadas
        self.listbox = Listbox(frameSelecionado, font=INFO)
        self.listbox.pack(side=BOTTOM, anchor='w')
            # vincula a scrollbar a listbox
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        
        # NOME DO GRUPO
        label = Label(self.frame, text="Nome do Grupo:", font=PRINCIPAL).grid(row=0,column=2,padx=40,pady=20)
            # cria uma entry para armazenar o nome do grupo
        self.entryNomeGrupo = Entry(self.frame, font=INFO)
        self.entryNomeGrupo.grid(row=1,column=2,padx=10)
        
        # botão que armazena todas as informações fornecidas
        botaoSalvar = Button(self.frame,text="Salvar", font=INFO, command=self.armazenar).grid(row=2,column=2,padx=60,pady=10)
        
    # função que verifica se a pessoa foi adicionada o retirada do grupo e a adiciona/remove da listbox
    def verificaPessoa(self, pessoa):
        # caso a pessoa não esteja já no vetor de pessoas selecionadas, a adiciona...
        if pessoa not in self.vetorSelecionados:
            self.vetorSelecionados.append(pessoa)
        # ...caso contrário a remove
        else:
            self.vetorSelecionados.remove(pessoa)
        # ordena o vetor com as pessoas selecionadas alfabeticamente
        self.vetorSelecionados=sorted(self.vetorSelecionados)
        # atualiza a Listbox
            # deleta todas as pessoas que foram adicionadas a listbox para atualiza-lá corretamente
        self.listbox.delete(0,len(self.vetorPessoas))
            # adiciona cada pessoa do vetor com as pessoas selecionadas na listbox
        for pessoa in self.vetorSelecionados:
            self.listbox.insert(self.vetorSelecionados.index(pessoa),pessoa)
    
    # função que o botaoSalvar usa para armazenar as informações do grupo criado
    def armazenar(self):
        # pega o nome do grupo da entry
        nomeGrupo = self.entryNomeGrupo.get()
        
        # verificação de erros
        if (nomeGrupo=='' or nomeGrupo=='\t' or nomeGrupo=='\n'):            
            tkMessageBox.showwarning("AVISO","NÃO HÁ NOME NO GRUPO!\nVERIFIQUE SE FOI ESCOLHIDO UM NOME PARA O NOVO GRUPO.", parent=self.frame)
            return -1
        if len(self.vetorSelecionados)==0:
            tkMessageBox.showwarning("AVISO","NÃO HÁ NENHUMA PESSOA SELECIONADA PARA O NOVO GRUPO!\nMARQUE AS PESSOAS QUE FARÃO PARTE DO NOVO GRUPO", parent=self.frame)
            return -1
            
        # verificação dos dados
        if tkMessageBox.askokcancel('VERIFICAÇÃO', 'Verifique os dados fornecidos\n\nNome do Grupo: '+nomeGrupo+'\nPessoas: '+', '.join(self.vetorSelecionados))==False:
            return -1
        
        # cria o grupo
        novoGrupo = Grupo(self.vetorSelecionados,nomeGrupo)
        # serializa os dados de novoGrupo para passar ao arquivo de armazenamento dos grupos
        serializacao = pk.dumps(novoGrupo)
        # salva informações do grupo no arquivo
        arquivo = open('build\grupos.txt','a+')
        arquivo.write(serializacao)
        arquivo.write('$$$') # caracteres responsáveis por separar cada objetos do texto
        arquivo.close()
        
        self.frame.destroy()

# classe que edita um grupo
class EditarGrupo(Interface):
    # inicializa a classe
    def __init__(self,frame,diaSemana):
        # inicialização da frame
        self.frame = frame
        self.frame.pack()
        
        # abre o arquivo com todos os grupos já criados
        try:
            arquivo = open('build\grupos.txt','r')
        except:
            tkMessageBox.showerror("ERRO DE ABERTURA","NÃO FOI POSSÍVEL ABRIR O ARQUIVO DOS GRUPOS!\NVERIFIQUE A EXISTÊNCIA DO ARQUIVO E SUA PASTA.", parent=self.frame)
            frame.destroy()
            return -1
        grupos = arquivo.read()
        # cria um vetor com cada um dos grupos que foram separados pelos '$$$'
        grupos = grupos.split('$$$')
        grupos.remove('')
        
        # verifica se há algum grupo
        if len(grupos)==0:
            tkMessageBox.showwarning("AVISO","NÃO HÁ GRUPOS NO ARQUIVO!\nCRIE UM NOVO GRUPO PARA PODER SELECIONÁ-LO.", parent=self.frame)
            frame.destroy()
            return -1
        
        # vetor contendo todas as pessoas
        self.vetorPessoas = diaSemana.getPessoas()
        
        # vetor selecionados
        self.vetorSelecionados = []        
        
        # vetor que irá conter o nome dos grupos
        self.nomesGrupos = []
        # vetor que contém os grupos
        self.vetorGrupos = []
        # cria os grupos e os adiciona nos vetores
        for g in grupos:
            gr = pk.loads(g)
            self.vetorGrupos.append(gr)
            self.nomesGrupos.append(gr.getNome())
        
        # SELECIONAR GRUPO
        label = Label(self.frame, text="Selecionar Grupo:", font=PRINCIPAL).grid(row=0,column=0,padx=40,pady=20)
            # cria uma frame para armazenar os objetos com scroll
        def myfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=200)
        frameSeleciona=Frame(self.frame,relief=GROOVE,width=50,height=100,bd=1)
        frameSeleciona.grid(row=1,column=0,padx=40,pady=20)
        
        canvas=Canvas(frameSeleciona)
        frameInterna=Frame(canvas)
        myscrollbar=Scrollbar(frameSeleciona,orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=myscrollbar.set)
        
        myscrollbar.pack(side="right",fill="y")
        canvas.pack(side="bottom")
        canvas.create_window((0,0),window=frameInterna,anchor='nw')
        frameInterna.bind("<Configure>",myfunction)        
        
        # variável que guarda o valor dos radiobuttons
        VarVal = IntVar()
        # inicia os valores da variável
        val = 1
        # itera sobre os grupos no vetor contendo todos grupos
        for grupo in self.nomesGrupos:
            # cria uma função que envia o nome da pessoa sempre que o checkbutton for clicado
            comando = lambda x=grupo:self.verificaGrupo(x)
            # cria o checkbutton com o nome da pessoa
            radio = Radiobutton(frameInterna, text=grupo, font=INFO, variable=VarVal, value=val, command=comando)
            radio.deselect()
            radio.pack(side=TOP, anchor='w')
            val = val+1
        
        # SELECIONAR PESSOA
        label = Label(self.frame, text="Selecionar Pessoas:", font=PRINCIPAL).grid(row=0,column=1,padx=40,pady=20)
            # cria uma frame para armazenar os objetos com scroll
        def myfunction(event):
            canvasPessoa.configure(scrollregion=canvasPessoa.bbox("all"),width=200,height=200)
        framePessoa=Frame(self.frame,relief=GROOVE,width=50,height=100,bd=1)
        framePessoa.grid(row=1,column=1,padx=40,pady=20)
        
        canvasPessoa=Canvas(framePessoa)
        frameInterna=Frame(canvasPessoa)
        myscrollbar=Scrollbar(framePessoa,orient="vertical",command=canvasPessoa.yview)
        canvasPessoa.configure(yscrollcommand=myscrollbar.set)
        
        myscrollbar.pack(side="right",fill="y")
        canvasPessoa.pack(side="bottom")
        canvasPessoa.create_window((0,0),window=frameInterna,anchor='nw')
        frameInterna.bind("<Configure>",myfunction)
        
        # função para marcar/desmarcar todas pessoas        
        def selecionarTodos():
            # se todas as pessoas estavam marcadas, desmarca todas
            if len(self.vetorPessoas)==len(self.vetorSelecionados):
                self.checkTodos.deselect()
                # limpa o vetor com as pessoas selecionadas
                self.vetorSelecionados=[]
                # desmarca todos
                for b in self.vetorChecks:
                    b.deselect()
                # deleta todas as pessoas que foram adicionadas a listbox
                self.listbox.delete(0,len(self.vetorPessoas))
                
            # caso tivessem pessoas que não estavam no vetor, marca todas
            else:
                self.checkTodos.select()
                # adiciona todas as pessoas ao vetor
                self.vetorSelecionados = self.vetorPessoas
                # marca todos
                for b in self.vetorChecks:
                    b.select()
                # deleta todas as pessoas que foram adicionadas a listbox para atualiza-lá corretamente
                self.listbox.delete(0,len(self.vetorPessoas))
                # adiciona todas as pessoas a listbox
                for pessoa in self.vetorSelecionados:
                    self.listbox.insert(self.vetorSelecionados.index(pessoa),pessoa)
                
        # o primeiro checkbutton é o para marcar/desmarcar todas pessoas
        self.checkTodos = Checkbutton(frameInterna, text="Marcar/Desmarcar Todos", font=INFO, command=selecionarTodos)
        self.checkTodos.deselect()
        self.checkTodos.pack(side=TOP, anchor='w')
        # armazena todos os checkbuttons dentro de um vetor para poder marcar/desmarcar todos
        self.vetorChecks = []
        # itera sobre as pessoas no vetor contendo todas pessoas
        for pessoa in self.vetorPessoas:
            # cria uma função que envia o nome da pessoa sempre que o checkbutton for clicado
            comando = lambda x=pessoa:self.verificaPessoa(x)
            # cria o checkbutton com o nome da pessoa
            check = Checkbutton(frameInterna, text=pessoa, font=INFO, command=comando)
            check.deselect()
            check.pack(side=TOP, anchor='w')
            # adiciona o checkbutton ao vetor
            self.vetorChecks.append(check)       
        
        # PESSOAS SELECIONADAS
        label = Label(self.frame, text="Pessoas Selecionadas:", font=PRINCIPAL).grid(row=0,column=3,padx=40,pady=20)
            # cria uma frame para armazenar os objetos com scroll
        frameSelecionado = Frame(self.frame)
        frameSelecionado.grid(row=1, column=3, padx=25)
            # cria a scroll bar para a listbox
        scrollbar = Scrollbar(frameSelecionado)
        scrollbar.pack(side=RIGHT, fill=Y)
            # cria um listbox que irá armazenar o nome das pessoas selecionadas
        self.listbox = Listbox(frameSelecionado, font=INFO)
        self.listbox.pack(side=BOTTOM, anchor='w')
            # vincula a scrollbar a listbox
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        
        # NOME DO GRUPO
        label = Label(self.frame, text="Nome do Grupo:", font=PRINCIPAL).grid(row=0,column=4,padx=40,pady=20)
            # cria uma entry para armazenar o nome do grupo
        self.entryNomeGrupo = Entry(self.frame, font=INFO)
        self.entryNomeGrupo.grid(row=1,column=4,padx=10)
        
        # botão que armazena todas as informações fornecidas
        botaoSalvar = Button(self.frame,text="Salvar", font=INFO, command=self.armazenar).grid(row=2,column=4,padx=60,pady=10)
        
    # função que verifica se a pessoa foi adicionada o retirada do grupo e a adiciona/remove da listbox
    def verificaPessoa(self, pessoa):
        # caso a pessoa não esteja já no vetor de pessoas selecionadas, a adiciona...
        if pessoa not in self.vetorSelecionados:
            self.vetorSelecionados.append(pessoa)
        # ...caso contrário a remove
        else:
            self.vetorSelecionados.remove(pessoa)
        # ordena o vetor com as pessoas selecionadas alfabeticamente
        self.vetorSelecionados=sorted(self.vetorSelecionados)
        # atualiza a Listbox
            # deleta todas as pessoas que foram adicionadas a listbox para atualiza-lá corretamente
        self.listbox.delete(0,len(self.vetorPessoas))
            # adiciona cada pessoa do vetor com as pessoas selecionadas na listbox
        for pessoa in self.vetorSelecionados:
            self.listbox.insert(self.vetorSelecionados.index(pessoa),pessoa)
            
    # função que verifica qual grupo foi selecionado e atualiza os valores (pessoas, nome do grupo)
    def verificaGrupo(self,grupo):
        # coloca o nome atual do grupo na entry
        self.entryNomeGrupo.delete(0,END)
        self.entryNomeGrupo.insert(END, grupo)
        # limpa o vetor com as pessoas selecionadas
        self.vetorSelecionados = []
        # itera sobre todos os grupos
        for g in self.vetorGrupos:
            # verifica se o grupo atual é o grupo selecionado
            if g.getNome()==grupo:
                # armazena o index desse grupo dentro do vetor
                index = self.vetorGrupos.index(g)
                break
        # seleciona o grupo selecionado
        grupo = self.vetorGrupos[index]
        # armazena o grupo selecionado para edição
        self.grupoSelecionado = grupo
        # vetor com as pessoas que estão atualmente no grupo
        pessoas = grupo.getPessoas()
        
        # itera sobre os checkbuttons das pessoas
        for ck in self.vetorChecks:
            ck.deselect()
            if ck.cget('text') in pessoas:
                ck.select()
                self.vetorSelecionados.append(ck.cget('text'))
        # coloca o vetor em ordem alfabética
        self.vetorSelecionados = sorted(self.vetorSelecionados)
        # atualiza a Listbox
            # deleta todas as pessoas que foram adicionadas a listbox para atualiza-lá corretamente
        self.listbox.delete(0,len(self.vetorPessoas))
            # adiciona cada pessoa do vetor com as pessoas selecionadas na listbox
        for pessoa in self.vetorSelecionados:
            self.listbox.insert(self.vetorSelecionados.index(pessoa),pessoa)
            
    # função que o botaoSalvar usa para armazenar as informações do grupo criado
    def armazenar(self):
        # pega o nome do grupo da entry
        nomeGrupo = self.entryNomeGrupo.get()
        
        # verificação de erros
        if nomeGrupo=='' or nomeGrupo=='\t' or nomeGrupo=='\n':
            tkMessageBox.showwarning("AVISO","NÃO HÁ NOME NO GRUPO!\nINSIRA UM NOME AO GRUPO.")
            return -1
        if len(self.vetorSelecionados)==0:
            tkMessageBox.showwarning("AVISO","NÃO HÁ PESSOAS SELECIONADAS!\nSELECIONE OS MEMBROS QUE PARTICIPARÃO DO NOVO GRUPO.")           
            return -1
        
        # verificação dos dados
        # verificação dos dados
        if tkMessageBox.askokcancel('VERIFICAÇÃO', 'Verifique os dados fornecidos\n\nNome do Grupo: '+nomeGrupo+'\nPessoas: '+', '.join(self.vetorSelecionados))==False:
            return -1
            
        # cria o grupo
        novoGrupo = Grupo(self.vetorSelecionados,nomeGrupo)
        # serializa os dados de novoGrupo para passar ao arquivo de armazenamento dos grupos
        serializacao = pk.dumps(novoGrupo)
        
        # abre o arquivo que contém os grupos para leitura
        arquivo = open('build\grupos.txt', 'r')
        
        # cria o vetor com todos os grupos serializados
        grupos = arquivo.read()
        grupos = grupos.split('$$$')
        grupos.remove('')
        
        arquivo.close()
        
        # reabre o arquivo para escrita
        arquivo = open('build\grupos.txt', 'w')
        
        # remove a versão anterior do grupo editado e coloca a nova
        grupos.remove(pk.dumps(self.grupoSelecionado)) #notar que ele compara com o valor serializado do grupo!
        grupos.append(serializacao)
            
        # novo texto contendo os grupos serializados
        texto = ''
        
        # compoe o texto no formato definido
        for g in grupos:
            texto=texto+g+'$$$'
        # escreve o texto no arquivo e o fecha
        arquivo.write(texto)
        arquivo.close()
        
        self.frame.destroy()
        
# classe que exclui um ou mais grupos
class ExcluirGrupo(Interface):
    # inicializa a classe
    def __init__(self,frame):
        # inicialização da frame
        self.frame = frame
        self.frame.pack()
        
        # abre o arquivo com todos os grupos já criados
        try:
            arquivo = open('build\grupos.txt','r')
        except:
            tkMessageBox.showerror("ERRO","NÃO FOI POSSÍVEL ABRIR O ARQUIVO CONTENDO OS GRUPOS!\nVERIFIQUE SUA EXISTÊNCIA NA PASTA \\build\\grupos.txt")
            frame.destroy()
            return -1
            
        grupos = arquivo.read()
        # cria um vetor com cada um dos grupos que foram separados pelos '$$$'
        grupos = grupos.split('$$$')
        grupos.remove('')
        
        # verifica se há grupos
        if len(grupos)==0:
            tkMessageBox.showwarning("AVISO","NÃO HÁ GRUPOS NA PASTA!\nCRIE UM NOVO GRUPO PARA PODER SELECIONÁ-LO.")
            frame.destroy()
            return -1
        
        # vetor que irá conter o nome dos grupos
        self.nomesGrupos = []
        # vetor que contém os grupos
        self.vetorGrupos = []
        # cria os grupos e os adiciona nos vetores
        for g in grupos:
            gr = pk.loads(g)
            self.vetorGrupos.append(gr)
            self.nomesGrupos.append(gr.getNome())
            
        # vetor com os grupos selecionados
        self.vetorSelecionados = []
            
                # GRUPOS PARA SELECIONAR
        label = Label(self.frame, text="Selecionar Grupo:", font=PRINCIPAL).grid(row=0,column=0,padx=40,pady=20)
            # cria uma frame para armazenar os objetos com scroll
        def myfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=200)
        frameSeleciona=Frame(self.frame,relief=GROOVE,width=50,height=100,bd=1)
        frameSeleciona.grid(row=1,column=0,padx=40,pady=20)
        
        canvas=Canvas(frameSeleciona)
        frameInterna=Frame(canvas)
        myscrollbar=Scrollbar(frameSeleciona,orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=myscrollbar.set)
        
        myscrollbar.pack(side="right",fill="y")
        canvas.pack(side="bottom")
        canvas.create_window((0,0),window=frameInterna,anchor='nw')
        frameInterna.bind("<Configure>",myfunction)
        
        # função para marcar/desmarcar todos grupos        
        def selecionarTodos():
            # se todas as pessoas estavam marcadas, desmarca todas
            if len(self.nomesGrupos)==len(self.vetorSelecionados):
                self.checkTodos.deselect()
                # limpa o vetor com as pessoas selecionadas
                self.vetorSelecionados=[]
                # desmarca todos
                for b in self.vetorChecks:
                    b.deselect()
                # deleta todas as pessoas que foram adicionadas a listbox
                self.listbox.delete(0,len(self.nomesGrupos))
                
            # caso tivessem pessoas que não estavam no vetor, marca todas
            else:
                self.checkTodos.select()
                # adiciona todas as pessoas ao vetor
                self.vetorSelecionados = self.nomesGrupos
                # marca todos
                for b in self.vetorChecks:
                    b.select()
                # deleta todas as pessoas que foram adicionadas a listbox para atualiza-lá corretamente
                self.listbox.delete(0,len(self.nomesGrupos))
                # adiciona todas as pessoas a listbox
                for grupo in self.vetorSelecionados:
                    self.listbox.insert(self.vetorSelecionados.index(grupo),grupo)
                
        # o primeiro checkbutton é o para marcar/desmarcar todas pessoas
        self.checkTodos = Checkbutton(frameInterna, text="Marcar/Desmarcar Todos", font=INFO, command=selecionarTodos)
        self.checkTodos.deselect()
        self.checkTodos.pack(side=TOP, anchor='w')
        # armazena todos os checkbuttons dentro de um vetor para poder marcar/desmarcar todos
        self.vetorChecks = []
        # itera sobre as pessoas no vetor contendo todas pessoas
        for g in self.nomesGrupos:
            # cria uma função que envia o nome da pessoa sempre que o checkbutton for clicado
            comando = lambda x=g:self.verificaGrupo(x)
            # cria o checkbutton com o nome da pessoa
            check = Checkbutton(frameInterna, text=g, font=INFO, command=comando)
            check.deselect()
            check.pack(side=TOP, anchor='w')
            # adiciona o checkbutton ao vetor
            self.vetorChecks.append(check)
            
            # GRUPOS SELECIONADOS
        label = Label(self.frame, text="Grupos Selecionadas:", font=PRINCIPAL).grid(row=0,column=1,padx=40,pady=20)
            # cria uma frame para armazenar os objetos com scroll
        frameSelecionado = Frame(self.frame)
        frameSelecionado.grid(row=1, column=1, padx=25)
            # cria a scroll bar para a listbox
        scrollbar = Scrollbar(frameSelecionado)
        scrollbar.pack(side=RIGHT, fill=Y)
            # cria um listbox que irá armazenar o nome das pessoas selecionadas
        self.listbox = Listbox(frameSelecionado, font=INFO)
        self.listbox.pack(side=BOTTOM, anchor='w')
            # vincula a scrollbar a listbox
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        
        # botão que exclui os grupos selecionados
        botaoExcluir = Button(self.frame,text="Excluir", font=INFO, command=self.excluir).grid(row=2,column=2,padx=60,pady=10)

    # função para excluir os grupos selecionados        
    def excluir(self):
        
        # vetor que contém os grupos a serem excluídos
        vetorExcluidos = []   
        
        # vetor que contém o nome dos grupos
        nomeExcluidos = []
        
        # itera sobre todos os grupos possíveis
        for grupo in self.vetorGrupos:
            # verfica se esse grupo está no vetor de grupos selecionados
            if grupo.getNome() in self.vetorSelecionados:
                # adiciona o grupo ao vetor que contém os grupos a serem excluídos
                vetorExcluidos.append(grupo)
                nomeExcluidos.append(grupo.getNome())
                
        if len(vetorExcluidos)==0:
            tkMessageBox.showwarning("AVISO","NENHUM GRUPO FOI SELECIONADO!\nSELECIONE ALGUM GRUPO PARA SER EXCLUÍDO.")
            return -1
            
        if (tkMessageBox.askokcancel("VERIFICAÇÃO", "Você tem certeza que quer excluir os grupos: "+', '.join(nomeExcluidos)+"?"))==False:
            return -1
        
        # abre o arquivo que contém os grupos para leitura
        arquivo = open('build\grupos.txt', 'r')
        
        # cria o vetor com todos os grupos serializados
        grupos = arquivo.read()
        grupos = grupos.split('$$$')
        grupos.remove('')
        
        # reabre o arquivo para escrita
        arquivo.close()
        arquivo = open('build\grupos.txt', 'w')
        
        # exclui cada um dos grupos que devem ser removidos
        for g in vetorExcluidos:
            grupos.remove(pk.dumps(g)) #notar que ele compara com o valor serializado do grupo!
            
        # novo texto contendo os grupos serializados que permanecerem
        texto = ''
        
        # compoe o texto no formato definido
        for g in grupos:
            texto=texto+g+'$$$'
        # escreve o texto no arquivo e o fecha
        arquivo.write(texto)
        arquivo.close()
        self.frame.destroy()

    # função que verifica se o grupo foi adicionada ou retirado
    def verificaGrupo(self, grupo):
        # caso a pessoa não esteja já no vetor de pessoas selecionadas, a adiciona...
        if grupo not in self.vetorSelecionados:
            self.vetorSelecionados.append(grupo)
        # ...caso contrário a remove
        else:
            self.vetorSelecionados.remove(grupo)
        # ordena o vetor com as pessoas selecionadas alfabeticamente
        self.vetorSelecionados=sorted(self.vetorSelecionados)
        # atualiza a Listbox
            # deleta todas as pessoas que foram adicionadas a listbox para atualiza-lá corretamente
        self.listbox.delete(0,len(self.nomesGrupos))
            # adiciona cada pessoa do vetor com as pessoas selecionadas na listbox
        for grupo in self.vetorSelecionados:
            self.listbox.insert(self.vetorSelecionados.index(grupo),grupo)
            
class NovaReuniao(Interface):
    # inicializa a classe
    def __init__(self, frame, diaSemana, vetorDias):
        # inicialização da frame
        self.frame = frame
        self.frame.pack()

        # vetor contendo todos os dias da semana
        self.vetorDias = vetorDias

        # abre o arquivo com todos os grupos já criados
        arquivo = open('build\grupos.txt', 'r')
        grupos = arquivo.read()
        # cria um vetor com cada um dos grupos que foram separados pelos '$$$'
        grupos = grupos.split('$$$')
        grupos.remove('')

        # vetor contendo todas as pessoas
        self.vetorPessoas = diaSemana.getPessoas()

        # vetor selecionados
        self.vetorPessoasSelecionadas = []

        # vetor grupos selecionados
        self.vetorGruposSelecionados = []

        # vetor pessoas selecionados dos grupos
        self.vetorPessoasGrupos = []

        # vetor pessoas obrigatorias
        self.vetorObrigatorias = []

        # index grupos selecionados
        self.IndexGrupos = []

        # vetor que irá conter o nome dos grupos
        self.nomesGrupos = []
        # vetor que contém os grupos
        self.vetorGrupos = []
        # cria os grupos e os adiciona nos vetores
        for g in grupos:
            gr = pk.loads(g)
            self.vetorGrupos.append(gr)
            self.nomesGrupos.append(gr.getNome())

            ################# CRIANDO A PARTE PARA GERAR AS 3 COLUNAS = GRUPOS , PESSOAS , PESSOAS OBRIGATORIAS ##############
            # primeira frame e canvas : selecionar grupo

        # GRUPOS PARA SELECIONAR
        label = Label(self.frame, text="Selecionar Grupo:", font=PRINCIPAL).grid(row=0, column=0, padx=40, pady=20)

        # cria uma frame para armazenar os objetos com scroll
        def myfunction(event):
            canvasGrupos.configure(scrollregion=canvasGrupos.bbox("all"), width=200, height=200)

        frameGrupos = Frame(self.frame, relief=GROOVE, width=50, height=100, bd=1)
        frameGrupos.grid(row=1, column=0, padx=40, pady=20)

        canvasGrupos = Canvas(frameGrupos, width=200, height=200)
        frameInternaGrupos = Frame(canvasGrupos)
        myscrollbar = Scrollbar(frameGrupos, orient="vertical", command=canvasGrupos.yview)
        canvasGrupos.configure(yscrollcommand=myscrollbar.set)

        myscrollbar.pack(side="right", fill="y")
        canvasGrupos.pack(side="bottom")
        canvasGrupos.create_window((0, 0), window=frameInternaGrupos, anchor='nw')
        frameInternaGrupos.bind("<Configure>", myfunction)

        # função que armazena os grupos quando tu clica neles , remove se já foi clicado

        def listaGrupos(grupo):
            if grupo not in self.vetorGruposSelecionados:
                marcaPessoas(grupo)
                self.vetorGruposSelecionados.append(grupo)
            else:
                removePessoas(grupo)
                self.vetorGruposSelecionados.remove(grupo)
            for elemento in self.vetorObrigatorias:
                self.vetorObrigatorias.remove(elemento)
            criaObrigatorias()

        def marcaPessoas(grupo):
            for g in self.vetorGrupos:
                # verifica se o grupo atual é o grupo selecionado
                if g.getNome() == grupo:
                    # armazena o index desse grupo dentro do vetor
                    index = self.vetorGrupos.index(g)
                    self.IndexGrupos = index

            pessoas = self.vetorGrupos[self.IndexGrupos]
            for pessoa in pessoas.getPessoas():
                if pessoa not in self.vetorPessoasSelecionadas:
                    self.vetorPessoasSelecionadas.append(pessoa)

            # itera sobre os checkbuttons das pessoas
            for ck in self.vetorChecksPessoas:
                ck.deselect()
                if ck.cget('text') in self.vetorPessoasSelecionadas:
                    ck.select()
                    # coloca o vetor em ordem alfabética

        def removePessoas(grupo):
            for g in self.vetorGrupos:
                # verifica se o grupo atual é o grupo selecionado
                if g.getNome() == grupo:
                    # armazena o index desse grupo dentro do vetor
                    index = self.vetorGrupos.index(g)
                    self.IndexGrupos = index

            pessoas = self.vetorGrupos[self.IndexGrupos]
            for pessoa in pessoas.getPessoas():
                if pessoa in self.vetorPessoasSelecionadas:
                    self.vetorPessoasSelecionadas.remove(pessoa)

                    # itera sobre os checkbuttons das pessoas
            for ck in self.vetorChecksPessoas:
                if ck.cget('text') not in self.vetorPessoasSelecionadas:
                    ck.deselect()

        # armazena todos os checkbuttons dentro de um vetor para poder marcar/desmarcar todos
        self.vetorChecksGrupos = []
        # itera sobre as pessoas no vetor contendo todas pessoas
        for g in self.nomesGrupos:
            # cria uma função que envia o nome do grupo sempre que o checkbutton for clicado
            comando = lambda x=g: listaGrupos(x)
            # cria o checkbutton com o nome dos grupos
            check = Checkbutton(frameInternaGrupos, text=g, font=INFO, command=comando)
            check.deselect()
            check.pack(side=TOP, anchor='w')
            # adiciona o checkbutton ao vetor
            self.vetorChecksGrupos.append(check)


            ## PARTE PARA SELECIONAR PESSOAS :)

        # PESSOAS PARA SELECIONAR
        label = Label(self.frame, text="Selecionar Pessoas:", font=PRINCIPAL).grid(row=0, column=1, padx=40, pady=20)

        # cria uma frame para armazenar os objetos com scroll
        def myfunctionpessoas(event):
            canvasPessoas.configure(scrollregion=canvasPessoas.bbox("all"), width=200, height=200)

        framePessoas = Frame(self.frame, relief=GROOVE, width=50, height=100, bd=1)
        framePessoas.grid(row=1, column=1, padx=40, pady=20)

        canvasPessoas = Canvas(framePessoas)
        frameInternaPessoas = Frame(canvasPessoas)
        myscrollbarpessoas = Scrollbar(framePessoas, orient="vertical", command=canvasPessoas.yview)
        canvasPessoas.configure(yscrollcommand=myscrollbarpessoas.set)

        myscrollbarpessoas.pack(side="right", fill="y")
        canvasPessoas.pack(side="bottom")
        canvasPessoas.create_window((0, 0), window=frameInternaPessoas, anchor='nw')
        frameInternaPessoas.bind("<Configure>", myfunctionpessoas)

        def selecionarTodos():
            # se todas as pessoas estavam marcadas, desmarca todas
            if len(self.vetorPessoas) == len(self.vetorPessoasSelecionadas):
                self.checkTodos.deselect()
                # limpa o vetor com as pessoas selecionadas
                self.vetorPessoasSelecionadas = []
                # desmarca todos
                for b in self.vetorChecksPessoas:
                    b.deselect()
                # deleta todas as pessoas que foram adicionadas a listbox
                for pessoa in self.vetorPessoasSelecionadas:
                    self.vetorPessoasSelecionadas.remove(pessoa)

            # caso tivessem pessoas que não estavam no vetor, marca todas
            else:
                self.checkTodos.select()
                # adiciona todas as pessoas ao vetor
                self.vetorPessoasSelecionadas = self.vetorPessoas
                # marca todos
                for b in self.vetorChecksPessoas:
                    b.select()

            criaObrigatorias()

        def listaPessoas(pessoa):
            if pessoa not in self.vetorPessoasSelecionadas:
                self.vetorPessoasSelecionadas.append(pessoa)
            else:
                self.vetorPessoasSelecionadas.remove(pessoa)
            for elemento in self.vetorObrigatorias:
                self.vetorObrigatorias.remove(elemento)

            criaObrigatorias()

        # o primeiro checkbutton é o para marcar/desmarcar todas pessoas
        self.checkTodos = Checkbutton(frameInternaPessoas, text="Marcar/Desmarcar Todos", font=INFO,
                                      command=selecionarTodos)
        self.checkTodos.deselect()
        self.checkTodos.pack(side=TOP, anchor='w')
        # armazena todos os checkbuttons dentro de um vetor para poder marcar/desmarcar todos
        self.vetorChecksPessoas = []
        # itera sobre as pessoas no vetor contendo todas pessoas
        for pessoa in self.vetorPessoas:
            # cria uma função que envia o nome da pessoa sempre que o checkbutton for clicado
            comando = lambda x=pessoa: listaPessoas(x)
            # cria o checkbutton com o nome da pessoa
            check = Checkbutton(frameInternaPessoas, text=pessoa, font=INFO, command=comando)
            check.deselect()
            check.pack(side=TOP, anchor='w')
            # adiciona o checkbutton ao vetor
            self.vetorChecksPessoas.append(check)

            # seleciona pessoas obrigatorias

        # PESSOAS PARA SELECIONAR
        label = Label(self.frame, text="Selecionar Pessoas Obrigatórias:", font=PRINCIPAL).grid(row=0, column=2,
                                                                                                padx=40, pady=20)

        # cria uma frame para armazenar os objetos com scroll
        def myfunctionobrigatorias(event):
            canvasObrigatorias.configure(scrollregion=canvasObrigatorias.bbox("all"), width=200, height=200)

        frameObrigatorias = Frame(self.frame, relief=GROOVE, width=50, height=100, bd=1)
        frameObrigatorias.grid(row=1, column=2, padx=40, pady=20)

        canvasObrigatorias = Canvas(frameObrigatorias, width=200, height=200)
        frameInternaObrigatorias = Frame(canvasObrigatorias)
        myscrollbarobrigatorias = Scrollbar(frameObrigatorias, orient="vertical", command=canvasObrigatorias.yview)
        canvasObrigatorias.configure(yscrollcommand=myscrollbarobrigatorias.set)

        myscrollbarobrigatorias.pack(side="right", fill="y")
        canvasObrigatorias.pack(side="bottom")
        canvasObrigatorias.create_window((0, 0), window=frameInternaObrigatorias, anchor='nw')
        frameInternaObrigatorias.bind("<Configure>", myfunctionobrigatorias)

        def listaObrigatorias(pessoa):
            if pessoa not in self.vetorObrigatorias:
                self.vetorObrigatorias.append(pessoa)
            else:
                self.vetorObrigatorias.remove(pessoa)

        self.vetorChecksObrigatorias = []

        # armazena todos os checkbuttons dentro de um vetor para poder marcar/desmarcar todos
        def criaObrigatorias():
            for botao in self.vetorChecksObrigatorias:
                botao.destroy()

            # itera sobre as pessoas no vetor contendo todas pessoas
            self.vetorPessoasSelecionadas.sort()

            for pessoa in self.vetorPessoasSelecionadas:
                # cria uma função que envia o nome da pessoa sempre que o checkbutton for clicado
                comando = lambda x=pessoa: listaObrigatorias(x)
                # cria o checkbutton com o nome da pessoa
                check = Checkbutton(frameInternaObrigatorias, text=pessoa, font=INFO, command=comando)
                check.deselect()
                check.pack(side=TOP, anchor='w')
                # adiciona o checkbutton ao vetor
                self.vetorChecksObrigatorias.append(check)

            # gerando a reunião:

        frameBotao = Frame(self.frame, relief=GROOVE, width=50, height=100, bd=1)
        frameBotao.grid(row=2, column=2, padx=40, pady=20)

        self.novaReuniao = Button(frameBotao, text='Gerar Reunião', font=INFO, command=self.gerarReuniao).pack(
            side=RIGHT, anchor='w')

    # gera a reunião
    def gerarReuniao(self):
        # verifica se há pessoas selecionadas
        if len(self.vetorPessoasSelecionadas)<2:
            tkMessageBox.askokcancel('AVISO', 'NÃO HÁ PESSOAS SELECIONADAS!\nSELECIONE AO MENOS DUAS PESSOAS PARA MARCAR UMA REUNIÃO.')
            return -1
        
        # cria um grupo qualquer com as pessoas selecionadas
        grupo = Grupo(self.vetorPessoasSelecionadas)

        # vetor com os dias da semana
        dias = self.vetorDias

        # ordena os dias da semana com base no número de disponíveis em ordem crescente
        # algoritmo baseado no *BUBBLE SORT*
        for fim in range(len(dias) - 1, -1, -1):
            for i in range(0, fim):
                # ajeitar essa linha de acordo com o time de reunião que deve ser feita
                if dias[i].getVetorHoraGrupo(grupo)[0].getNumDisponivel() > dias[i + 1].getVetorHoraGrupo(grupo)[
                    0].getNumDisponivel():
                    aux = dias[i]
                    dias[i] = dias[i + 1]
                    dias[i + 1] = aux
        # inverte o vetor dias para se ter em ordem decrescente
        dias = dias[::-1]

        # cria uma nova janela no Tkinter com os dias da semana
        reuniao = Tk()
        reuniao.geometry("800x400+100+100")
        reuniao.minsize(width='800', height='400')
        reuniao.title('Horários Reunião')

        def myfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"), width=800, height=400)
        canvasDias = Canvas(reuniao)
        canvasDias.pack(side = 'top')
        canvas = Canvas(reuniao)
        frameInterna = Frame(canvas)
        myscrollbar = Scrollbar(reuniao, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=myscrollbar.set)

        myscrollbar.pack(side="right", fill="y")
        canvas.pack(side="left")
        canvas.create_window((0, 0), window=frameInterna, anchor='nw')
        frameInterna.bind("<Configure>", myfunction)

        frameDias = Frame(canvasDias)
        frameDias.pack(side = 'top')

        ####################################################################################################################
        # função que abre uma janela contendo as informações daquele horário
        # vetor é composto por [dia hora]
        # dia: dia da semana
        # hora: hora daquele dia da semana
        def getInfoHora(vetor):
            # dia da semana
            dia = vetor[0]
            # hora
            hora = vetor[1]

            # janela que contém as informações das pessoas naquele horário do dia
            infoHora = Tk()
            infoHora.geometry("600x400+100+100")
            infoHora.minsize(width='600', height='400')
            infoHora.title(dia.getDia() + ' ' + hora.getHora())

            def myfunction(event):
                canvasHora.configure(scrollregion=canvasHora.bbox("all"), width=600, height=400)

            canvasHora = Canvas(infoHora)
            frameInterna = Frame(canvasHora)
            myscrollbar = Scrollbar(infoHora, orient="vertical", command=canvasHora.yview)
            canvasHora.configure(yscrollcommand=myscrollbar.set)

            myscrollbar.pack(side="right", fill="y")
            canvasHora.pack(side="left")
            canvasHora.create_window((0, 0), window=frameInterna, anchor='nw')
            frameInterna.bind("<Configure>", myfunction)

            # texto para as pessoas disponíveis
            disp = ''
            # adiciona as pessoas ao texto
            for pessoa in hora.getDisponivel():
                disp = disp + '\n' + pessoa

            # texto para as pessoas talvez
            talvez = ''
            # adiciona as pessoas ao texto
            for pessoa in hora.getTalvez():
                talvez = talvez + '\n' + pessoa

            # texto para as pessoas indisponíveis
            indisp = ''
            # adiciona as pessoas ao texto
            for pessoa in hora.getIndisponivel():
                indisp = indisp + '\n' + pessoa

            # label disponíveis
            label = Label(frameInterna, text='Disponiveis: ', font=PRINCIPAL).grid(row=0, column=0, padx=40)
            label = Label(frameInterna, text=disp, font=INFO).grid(row=1, column=0, padx=40)
            # label talvez
            label = Label(frameInterna, text='Talvez: ', font=PRINCIPAL).grid(row=0, column=1, padx=40)
            label = Label(frameInterna, text=talvez, font=INFO).grid(row=1, column=1, padx=40)
            # label indisponíveis
            label = Label(frameInterna, text='Indisponiveis: ', font=PRINCIPAL).grid(row=0, column=2, padx=40)
            label = Label(frameInterna, text=indisp, font=INFO).grid(row=1, column=2, padx=40)

            infoHora.mainloop()

        ################################################################################################################################

        # coluna que cada dia da semana vai ser colocado
        COL = 0

        # verifica se há pessoas obrigatórias para a reunião
        if (self.vetorObrigatorias > 0):
            # itera sobre cada dia
            for d in dias:
                # label com o dia da semana
                label = Label(frameDias, text=d.getDia(), font=PRINCIPAL).grid(row=0, column=COL, padx=50, pady=20)

                # linha que cada hora vai ser colocada
                LIN = 1
                # itera sobre cada hora do vetor contendo as horas do dia
                for hora in d.getVetorHoraSelecionada(self.vetorObrigatorias, d.getVetorHoraGrupo(grupo)):
                    # texto do botão da hora
                    texto = hora.getHora() + '\nDisponiveis: ' + str(hora.getNumDisponivel()) + '\nTalvez: ' + str(
                        hora.getNumTalvez()) + '\nIndiponiveis: ' + str(hora.getNumIndisponivel())
                    # função que é passada para a frame da hora
                    comando = lambda x=[d, hora]: getInfoHora(x)
                    # botão para a hora
                    botao = Button(frameInterna, text=texto, command=comando).grid(row=LIN, column=COL, pady=5,padx = 30)
                    # incrementa a linha para a hora
                    LIN = LIN + 1
                # incrementa a coluna dos dias
                COL = COL + 1

        # caso ninguém seja obrigatório
        else:
            # itera sobre cada dia
            for d in dias:
                # label com o dia da semana
                label = Label(frameDias, text=d.getNome(), font=PRINCIPAL).grid(row=0, column=COL, padx=50, pady=20)

                # linha que cada hora vai ser colocada
                LIN = 1
                # itera sobre cada hora do vetor contendo as horas do dia
                for hora in d.getVetorHoraGrupo(grupo):
                    # texto do botão da hora
                    text = hora.getHora() + '\nDisponiveis: ' + str(hora.getNumDisponivel()) + '\nTalvez: ' + str(
                        hora.getNumTalvez()) + '\nIndiponiveis: ' + str(hora.getNumIndisponivel())
                    # função que é passada para a frame da hora
                    comando = lambda x=[d, hora]: getInfoHora(x)
                    # botão para a hora
                    botao = Button(frameInterna, text=texto, command=comando).grid(row=LIN, column=COL, pady=20,padx = 30)
                    # incrementa a linha para a hora
                    LIN = LIN + 1
                # incrementa a coluna dos dias
                COL = COL + 1

        reuniao.mainloop()