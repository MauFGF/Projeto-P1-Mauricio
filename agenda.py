import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

def printCores(texto, cor) :
  print(cor + texto + RESET)  
#Adiciona Atividade a agenda
def adicionar(descricao, extras):
    if descricao == '':
        return False
    else:
        data = ''
        hora =''
        pri = ''
        desc = descricao
        contexto = ''
        projeto = ''
        for x in extras:
            if horaValida(x) == True:
                hora = x                    
            elif dataValida(x) == True:
                data = x                   
            elif projetoValido(x)==True:
                projeto = x       
            elif contextoValido(x)==True:
                contexto= x                   
            elif prioridadeValida(x) == True:
                pri = x.upper()
        texto = data + chr(32) + hora + chr(32) + pri + chr(32) + desc + chr(32) + contexto + chr(32) + projeto                
    try:
        fp = open('todo.txt', 'a')
        fp.write("\n"+texto)
        fp.close()
    except IOError as err:
        print("Não foi possível escrever para o arquivo " + TODO_FILE)
        print(erro)
        return False
    return True        
# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero):
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True
# Valida a hora
def horaValida(horaMin):
    horaMin = str(horaMin)
    if len(horaMin) !=4 or not soDigitos(horaMin):
        return False
    hora = horaMin[0] + horaMin[1]
    minuto = horaMin[2] + horaMin[3]
    if hora < '00' or hora>'23' or minuto < '00' or minuto > '59':
        return False
    return True
# Valida datas
def dataValida(data):
    data = str(data)
    if len(data) != 8 or not soDigitos(data):
        return False
    dia = data[0] + data[1]
    mes = data[2] + data[3]
    ano = data[4] + data[5] + data[6] + data[7]
    if dia <'01' or dia > '31':
        return False
    if mes <'01' or mes > '12':
        return False
    if mes == '01' or mes =='03' or mes =='05' or mes =='07' or mes=='08' or mes=='10' or mes =='12':
        if dia <'01' or dia> '31':
            return False
    elif mes =='04' or mes == '06' or mes == '09' or mes == '11':
        if dia <'01' or dia>'30':
            return False
    elif mes =='02':
        if dia < '01' or dia > '29':
            return False
    return True      
# Valida que o string do projeto está no formato correto.
def projetoValido(proj):
    proj = str(proj)
    if len(proj) < 2:
        return False
    if str(proj[0]) != '+':
        return False
    return True           
# Valida que o string do contexto está no formato correto.
def contextoValido(cont):
    cont = str(cont)
    if len(cont) < 2:
        return False
    if str(cont[0]) != '@':
        return False
    return True 
# Valida a prioridade
def prioridadeValida(pri):
    pri = pri.upper()
    if len(pri) !=3:
        return False
    if pri[0] != '('  or pri[2] != ')':
        return False
    if ord(pri[1]) < ord('A') or ord(pri[1])> ord('Z'):
        return False
    return True

def organizar(linhas):
  itens=[]
  for l in linhas:
      data = '' 
      hora = ''
      pri = ''
      desc = ''
      contexto = ''
      projeto = ''  
      l=l.strip()
      tokens = l.split()
      for x in tokens: 
          if horaValida(x) == True and (x == tokens[0] or x == tokens[1]):
              hora = x     
          elif dataValida(x) == True  and  x == tokens[0]:
              data = x    
          elif projetoValido(x)==True  and x == tokens[(len(tokens)-1)]:
              projeto = x
          elif contextoValido(x)== True and (x == tokens[(len(tokens)-1)] or x == tokens[(len(tokens)-2)]):
              contexto= x   
          elif prioridadeValida(x) == True and (x == tokens[0] or x == tokens[1] or x == tokens[2]):
              pri = x    
          else:
              desc = desc + chr(32)+ x
      itens.append((desc,(data,hora,pri,contexto,projeto)))        
  return itens

def numero(parametro):
  arq = open('todo.txt','r')
  arqLido = arq.readlines()
  contador = 1
  for z in arqLido:
    if parametro in z:
      return contador
      contador=1
    else:
      contador+=1  
              
def listar():
  tuplas = ordenar(organizar(open('todo.txt','r'))) 
  for x in tuplas:
    data = x[1][0]
    orgData=data[:2] + '/' + data[2:4] + '/' + data[4:]
    hora = x[1][1]
    orgHora = hora[:2] + 'h' + hora[2:] + 'm'
    prioridade = x[1][2]
    parametro=x[0]
    if data!='':
      if hora!='':
         texto = str(numero(parametro))+ chr(32) + orgData  + chr(32) + orgHora  + prioridade + x[0] + chr(32) + x[1][3] + chr(32) + x[1][4]
         if prioridade == '(A)':
             printCores(texto, RED + BOLD)
         elif prioridade == '(B)':
             printCores(texto,BLUE)
         elif prioridade == '(C)':
             printCores(texto,YELLOW)
         elif prioridade == '(D)':
             printCores(texto,GREEN)
         else:
             print(texto)            
      elif hora=='':
         texto = str(numero(parametro))+ chr(32) + orgData  + chr(32) + hora  + prioridade + x[0] + chr(32) + x[1][3] + chr(32) + x[1][4]
         if prioridade == '(A)':
             printCores(texto, RED + BOLD)
         elif prioridade == '(B)':
             printCores(texto,BLUE)
         elif prioridade == '(C)':
             printCores(texto,YELLOW)
         elif prioridade == '(D)':
             printCores(texto,GREEN)
         else:
             print(texto)
    else:
      if hora!='':
         texto = str(numero(parametro))+ chr(32)+ data  + chr(32) + orgHora  + prioridade + x[0] + chr(32) + x[1][3] + chr(32) + x[1][4]
         if prioridade == '(A)':
             printCores(texto, RED + BOLD)
         elif prioridade == '(B)':
             printCores(texto,BLUE)
         elif prioridade == '(C)':
             printCores(texto,YELLOW)
         elif prioridade == '(D)':
             printCores(texto,GREEN)
         else:
             print(texto)
      elif hora =='':
         texto = str(numero(parametro))+ chr(32)+ data  + chr(32) + hora  + prioridade + x[0] + chr(32) + x[1][3] + chr(32) + x[1][4]
         if prioridade == '(A)':
             printCores(texto, RED + BOLD)
         elif prioridade == '(B)':
             printCores(texto,BLUE)
         elif prioridade == '(C)':
             printCores(texto,YELLOW)
         elif prioridade == '(D)':
             printCores(texto,GREEN)
         else:
             print(texto)    
                                   
def invert(valor):
    valor = valor[4:] + valor[2:4] + valor[:2]
    return valor               
      
def ordenarPorData(itens):
    for x in itens:          
        cont = 0
        while cont < len(itens)-1:
            if invert(itens[cont][1][0]) > invert(itens[cont+1][1][0])  :
                temp = itens[cont]
                itens[cont] = itens[cont+1]
                itens[cont+1] = temp
            cont+=1       
    lista=[]
    num=0
    for  y in itens:
        if y[1][0] =='':
            lista.append(y)
            num+=1
    while num !=0 :
        itens.pop(0)
        num-=1
    itens+=lista    
    return itens

def ordenarHora(itens):
    itens = ordenarPorData(itens)
    for x in itens:
        cont = 0
        while cont < len(itens)-1:
            if itens[cont][1][0] == itens[cont+1][1][0]  :
                if itens[cont][1][1] > itens[cont+1][1][1] and itens[cont+1][1][1]!='' :
                    temp = itens[cont]
                    itens[cont] = itens[cont+1]
                    itens[cont+1] = temp
            cont+=1    
    return itens
    
def ordenarPorPrioridade(itens):
  itens.sort(key=lambda x: x[1][2]) 
  lista=[]
  num=0
  for  y in itens:
      if y[1][2] =='':
          lista.append(y)
          num+=1
  while num !=0 :
      itens.pop(0)
      num-=1
  itens+=lista    
  return itens  

def ordenar(itens):
    itens = ordenarHora(itens)
    itens = ordenarPorPrioridade(itens)       
    return itens

def remover(num):
  num=int(num)
  arq = open('todo.txt','r')
  x= arq.readlines()
  if len(x) < num:
    return print('Número Invalido')    
  x.pop(num-1)
  arq.close()
  arq2= open('todo.txt','w')
  for y in x:
    arq2.write(y)
  arq2.close()  
 
     
def priorizar(num,prioridade):
  num= int(num)
  arq = open('todo.txt','r')
  arqLeitor= arq.readlines()
  orgArq = organizar(arqLeitor)
  tarefa = orgArq[num-1]
  extras=[]
  desc=tarefa[0]
  for x in tarefa[1]:
    extras.append(x)
  extras[2] = prioridade
  extras= tuple(extras)
  if len(arqLeitor) < num:
    return print('Número Invalido') 
  remover(num)
  adicionar(desc,extras)
  

def adicionar2(descricao,extras):
    if descricao == '' or descricao[0]=='@' or descricao[0]=='+' or horaValida(descricao[0])== True or dataValida(descricao[0])== True:
        return False
    else:
        data = ''
        hora =''
        pri = ''
        desc = descricao
        contexto = ''
        projeto = ''
        for x in extras:
            if horaValida(x) == True:
                hora = x        
            elif dataValida(x) == True:
                data = x       
            elif projetoValido(x)==True:
                projeto = x
            elif contextoValido(x)==True:
                contexto= x          
            elif prioridadeValida(x) == True:
                pri = x.upper()                
            else:
              desc = desc + chr(32) + x      
        texto = data + chr(32) + hora + chr(32) + pri + chr(32) + desc + chr(32) + contexto + chr(32) + projeto             
    try:
        fp = open('done.txt','a')
        fp.write( "\n" + texto )
        fp.close()
    except IOError as err:
        print("Não foi possível escrever para o arquivo " + ARCHIVE_FILE)
        print(erro)
        return False
    return True

def fazer(num):
  num=int(num)
  arq = open('todo.txt','r')
  x= arq.readlines()
  arq.close()
  arqOrg = organizar(x)
  tarefa = arqOrg[num-1]
  desc = tarefa[0]
  extras = tarefa[1]
  adicionar2(desc,extras)
  remover(num)
   
def filtrar(lista):
  arq = open('todo.txt','r')
  if projetoValido(lista[2])== True: 
    for x in arq:
      if lista[2] in x:
        print(x)
  elif contextoValido(lista[2])== True:
    for x in arq:
      if lista[2] in x:
        print(x)
  elif prioridadeValida(lista[2])== True:
    for x in arq:
      if lista[2] in x:
        print(x) 
  elif lista[2]== chr(32):
    print (listar())

def processarComandos(comandos):
  if comandos[1] == ADICIONAR:
    comandos.pop(0) 
    comandos.pop(0)   
    x = organizar([chr(32).join(comandos)])
    itemParaAdicionar = x[0]
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) 
    print('Adicionado')   
  elif comandos[1] == LISTAR:
    if len(comandos)-1 == 1:
      comandos += [chr(32)]
    comandos[2] = comandos[2].upper() 
    filtrar(comandos)     
  elif comandos[1] == REMOVER:
    num = comandos[2]
    remover(num)
    return print('Removido')
  elif comandos[1] == FAZER:
    num = comandos[2]
    print('Feito')
    return fazer(num)   
  elif comandos[1] == PRIORIZAR:
    num = comandos[2]
    prioridade = comandos[3]
    print('Modificado')
    return priorizar(num,prioridade)   
  else :
    print("Comando inválido.")    
processarComandos(sys.argv)




    


