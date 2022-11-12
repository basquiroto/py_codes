#
# Fernando Basquiroto de Souza
# Aula Alura - Python para Iniciantes
# 

def trata_input(mensagem, tipo = 'float'):
    while True:
        try:
            if tipo == 'float':
                number = float(input(mensagem))
            elif tipo == 'int':
                number = int(input(mensagem))
            else:
                pass
            if (number <= 0):
                print('\nERRO: Número igual ou menor que zero. Tente novamente.\n')
                continue
            return number
            break
        except:
            print('\nERRO: Verifique o número digitado e lembre-se que o separador decimal é o ponto. Tente novamente.\n')

def mistura(Qr, Cr, Qe, Ce):
    C0 = ((Qr * Cr)+(Qe * Ce))/(Qr + Qe)
    return C0

print('Informe as características do curso d\'água e do efluente.')

Qr = trata_input('Vazão do rio: ')
Cr = trata_input('Concentração no rio: ')
Qe = trata_input('Vazão do efluente: ')
Ce = trata_input('Concentração no efluente: ')

# Equação de mistura
C0 = mistura(Qr, Cr, Qe, Ce)

print('A concentração na mistura será de: {:.2f}'.format(C0))

next_step = trata_input('\nDeseja verificar qual é a concentração do efluente que irá atender a legislação? \n[1: Sim / 2: Nao]: ', 'int')

if (next_step == 1):
    print('\nDigite agora o limite da concentração no ponto de mistura.')
    lim = trata_input('Limite da concentração: ')

    i = 0
    Ce_ini = Ce
    while(C0 > lim):
        Ce = Ce * 0.9
        C0 = mistura(Qr, Cr, Qe, Ce)

        i += 1
        #print('Calculando ({})'.format(i), end='... ')

    if (i==0):
        print('A concentração atual do efluente já atenderá a legislação.')
    else:
        print('\nA concentração do efluente deverá ser de {:.2f} para atender a legislação.'.format(Ce))
        perc_reduction = (1-(Ce/Ce_ini))*100
        print('\nUma redução de {:.2f}% é necessária na concentração do efluente.'.format(perc_reduction))
    
else:
    print('\nPrograma finalizado.')
