import csv
import pandas as pd
def ler_csv_chamados():
    with open('consolidado_chamados.csv', newline='',encoding='UTF8') as c:
        reader = csv.reader(c)
        chamados = list(reader)
        return chamados

def ordena_pareto():
    #m=pd.DataFrame(pd.read_csv('consolidado_chamados.csv',header=None))
    m = ((pd.DataFrame(pd.read_csv('consolidado_chamados.csv',header=None))).sort_values(by=[0, 8, 12], ascending=(True, True, False)))
    m.to_csv('paretto.csv',header=None,encoding='UTF8')
    return m



def separa_lotacao():
    entrada=ordena_pareto().values.tolist()
    super=[]
    depto=[]
    divisao=[]
    setor=[]

    for x in range(0,len(entrada)):
        #print(entrada[x][0], entrada[x][7][:11], entrada[x][7][:17], entrada[x][7][:23], entrada[x][7][:29])
        super.append((entrada[x][0], entrada[x][7][:11]))  # 0 é mes, 8 é lotação))
        depto.append((entrada[x][0], entrada[x][7][:17]))
        divisao.append((entrada[x][0],entrada[x][7][:23]))
        setor.append((entrada[x][0], entrada[x][7][:29]))


    super = pd.DataFrame(super).drop_duplicates().sort_values(by=[0,1],ascending=(True,True)).values.tolist()
    depto = pd.DataFrame(depto).drop_duplicates().sort_values(by=[0,1],ascending=(True,True)).values.tolist()
    divisao = pd.DataFrame(divisao).drop_duplicates().sort_values(by=[0,1],ascending=(True,True)).values.tolist()
    setor = pd.DataFrame(setor).drop_duplicates().sort_values(by=[0,1],ascending=(True,True)).values.tolist()


    return super,depto,divisao,setor

#print(list(separa_lotacao()[0]))
def cont_super():
    cd=(separa_lotacao()[0])
    ch=pd.DataFrame(ler_csv_chamados()).sort_values(by=[0, 6, 9], ascending=(True, True, False))#1 é o return da divisão
    ch=pd.DataFrame(ch).values.tolist()
    dados_chamados = []  # usado para append dos chamados, mês, lotação, quantidade e corte da produtividade (meta de 75%)
    dados_pessoas = []
    # contabiliza o total de chamados no setor, por mês e lotação

    for x in range(0,len(cd)):
        cont_tkt=0
        #print(cd[x][0],cd[x][1])
        for y in range(0,len(ch)):
            if ch[y][0]==cd[x][0] and ch[y][6][:11]==cd[x][1]:
                cont_tkt = cont_tkt + float(ch[y][9])
        dados_chamados.append((cd[x][0], cd[x][1], cont_tkt, cont_tkt * 0.75))
    return dados_chamados


def cont_depto():
    cd=(separa_lotacao()[1])
    ch=pd.DataFrame(ler_csv_chamados()).sort_values(by=[0, 6, 9], ascending=(True, True, False))#1 é o return da divisão
    ch=pd.DataFrame(ch).values.tolist()
    dados_chamados = []  # usado para append dos chamados, mês, lotação, quantidade e corte da produtividade (meta de 75%)
    dados_pessoas = []
    # contabiliza o total de chamados no setor, por mês e lotação

    for x in range(0,len(cd)):
        cont_tkt=0
        cont_p=0
        #print(cd[x][0],cd[x][1])
        for y in range(0,len(ch)):
            if ch[y][0]==cd[x][0] and ch[y][6][:17]==cd[x][1]:
                cont_tkt = cont_tkt + float(ch[y][9])
                cont_p = cont_p+1
                #print(ch[y][0], cd[x][0])
        dados_chamados.append((cd[x][0], cd[x][1], cont_tkt, cont_tkt * 0.75,cont_p))
    return dados_chamados


def cont_divisao():
    cd=(separa_lotacao()[2])
    ch=pd.DataFrame(ler_csv_chamados()).sort_values(by=[0, 6, 9], ascending=(True, True, False))#1 é o return da divisão
    ch=pd.DataFrame(ch).values.tolist()
    dados_chamados = []  # usado para append dos chamados, mês, lotação, quantidade e corte da produtividade (meta de 75%)
    dados_pessoas = []

    for x in range(0,len(cd)):
        cont_tkt=0
        cont_p = 0
        #print(cd[x][0],cd[x][1])
        for y in range(0,len(ch)):
            if ch[y][0]==cd[x][0] and ch[y][6][:23]==cd[x][1]:
                cont_tkt = cont_tkt + float(ch[y][9])
                cont_p = cont_p + 1
        dados_chamados.append((cd[x][0], cd[x][1], cont_tkt, cont_tkt * 0.75,cont_p))
    return dados_chamados

def cont_setor():
    cd = (separa_lotacao()[3])
    ch = pd.DataFrame(ler_csv_chamados()).sort_values(by=[0, 6, 9],ascending=(True, True, False))  # 1 é o return da divisão
    ch = pd.DataFrame(ch).values.tolist()

    dados_chamados=[]#usado para append dos chamados, mês, lotação, quantidade e corte da produtividade (meta de 75%)
    dados_pessoas=[]
    #contabiliza o total de chamados no setor, por mês e lotação
    for x in range(0, len(cd)):
        cont_tkt = 0
        cont_p = 0
        cont_perc=0
        cont_perc_pessoas = 0
        #esse for junta a quantidade de pessoas e os tickets atendidos
        for y in range(0, len(ch)):
            if ch[y][0] == cd[x][0] and ch[y][7][:29] == cd[x][1]:
                cont_tkt = cont_tkt + float(ch[y][9])
                cont_p = cont_p + 1
        #esse for vai contar até o atingimento de 75%
        for j in range(0, len(ch)):
            if ch[j][0] == cd[x][0] and ch[j][7][:29] == cd[x][1]:
                if cont_perc + float(ch[j][9])>(cont_tkt*0.75):
                    pass
                else:
                    cont_perc = cont_perc + float(ch[j][9])
                    cont_perc_pessoas = cont_perc_pessoas + 1
                    print(ch[j][0],cd[x][1],ch[j][9],cont_tkt,cont_perc_pessoas,cont_perc)

        dados_chamados.append((cd[x][0], cd[x][1],cont_tkt,cont_tkt*0.75,cont_p,cont_perc_pessoas,cont_perc))
    return dados_chamados

#print(ch[1],'\n',cd[1],'\n',len(cd))



#ch=pd.DataFrame(cont_divisao()).to_csv('hhh.csv')
#print(cont_divisao())
cont_setor()
#print(cont_depto())
#print(cont_super())
#separa_lotacao()

#separa_lotacao()