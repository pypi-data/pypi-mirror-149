from math import pow

class opbinario:

    """
        - Está classe tem como objetivo oferecer funções para realização de operações
          com numeros binarios como: converção de bases, operações aritimeticas e operações
          logicas entre numeros binarios
    """

    @staticmethod
    def bin(num):
        """
        - Está função recebe um numero decimal positivo e retorna o numero convertido
         para binario.

        :param num: recebe um numero inteiro positivo
        :return: numero convertido em binario
        """
        bin = ''

        while(num > 1):
            bin+= f'{num % 2}'
            num //= 2

        bin+= f'{num}'

        return bin[::-1]

    @staticmethod
    def dec(bin):
        """
        - Está função recebe uma string contendo um numero binario e retorna o numero convertido
         para decimal.

        :param num: string contendo um numero binario
        :return: numero convertido em decimal
        """
        dec = 0
        indice = 0
        for i in range(len(bin)-1,-1,-1):

            if bin[i] == '1':
                dec+= pow(2,indice)

            indice+=1


        return int(dec)

    @staticmethod
    def strbin(str):
        """
        - Está função recebe uma string e retorna a string convertida em binario

        :param str: string
        :return: string convertida em binario
        """
        a_bytes = bytes(str, "ascii")

        bin = ''
        for i in a_bytes:
            bin += opbinario.bin(i) + ' '

        return bin

    @staticmethod
    def binstr(bin):
        """
        - recebe uma string contendo um numero binario ou um conjunto de numeros binarios
        separados por espaço e converte o numero binario para caracteres ou conjunto de caracteres

        :param bin: string contendo um numero binario ou um conjunto de numeros binarios
        separados por espaço

        :return: o numero binario convertido para caracteres ou conjunto de caracteres
        """
        str = ''
        bin = bin.split(' ')
        for i in bin:
            if i != '':
                dec = opbinario.dec(i)
                str += chr(dec)

        return str

    @staticmethod
    def oct(num):
        """
        - recebe um numero decimal positivo ou uma string contendo um numero binario e converte o numero decimal
        ou binario para octal

        :param num: numero inteiro positivo ou uma string contendo um numero binario
        :return: numero convetido octal
        """
        bin = num
        if type(num) == int:
            bin = opbinario.bin(num)

        while (len(bin) % 3 != 0 ):
            bin = '0' + bin

        octal = ''
        for i in range(0,len(bin),3):
            dec = opbinario.dec(bin[i:i+3])
            octal += f'{dec}'


        return int(octal)

    @staticmethod
    def hex(num):
        """
        - recebe um numero decimal positivo ou uma string contendo um numero binario e converte o numero decimal
         ou binario para hexadecimal

        :param num: numero inteiro positivo ou uma string contendo um numero binario
        :return: numero convetido hexadecimal
        """
        bin = num

        letras = {10:'a',11:'b',12:'c',13:'d',14:'e',15:'f'}

        if type(num) == int:
            bin = opbinario.bin(num)

        while (len(bin) % 4 != 0):
            bin = '0' + bin

        hexadecimal = ''
        for i in range(0, len(bin), 4):
            dec = opbinario.dec(bin[i:i + 4])
            if dec > 9:
                dec = letras[dec]

            hexadecimal += f'{dec}'

        return hexadecimal


    @staticmethod
    def iguala_bases(n1,n2):
        """
        - recebe dois numeros binarios e iguala suas bases adicionando
        0 a esquerda do numero com menor valor

        :param n1: numero binario tipo str
        :param n2: numero binario tipo str

        :return: n1 e n2
        """

        if len(n1) > len(n2):
            aux = len(n1) - len(n2)
            for i in range(0,aux):
                n2 = '0' + n2

        elif len(n1) < len(n2):
            aux = len(n2) - len(n1)
            for i in range(0,aux):
                n1 = '0' + n1

        return n1,n2

    @staticmethod
    def somabin(n1,n2):
        """
        - recebe dois numeros binarios e realiza a soma dos
        valores e retorna o resultado da operação

        :param n1: numero binario tipo str
        :param n2: numero binario tipo str

        :return: resultado da operação
        """

        sobe = 0
        resul = ''

        n1,n2 = opbinario.iguala_bases(n1,n2)

        for i in range(len(n1)-1,-1,-1):
            nu1 = int(n1[i])
            nu2 = int(n2[i])

            if sobe + nu1 == 2:
                nu1 = 0
                resul = f'{nu1+nu2}' + resul
            else:
                nu1 += sobe
                if nu1 + nu2 == 2:
                    resul = '0' + resul
                    sobe = 1
                else:
                    resul = f'{nu1 + nu2}' + resul
                    sobe = 0

        if sobe == 1:
            resul = '1'+resul

        return resul

    @staticmethod
    def subbin(n1, n2):

        """
        - recebe dois numeros binarios e realiza a subtração dos
        valores e retorna o resultado da operação

        :param n1: numero binario tipo str
        :param n2: numero binario tipo str

        :return: resultado da operação
        """

        sobe = 0
        resul = ''

        n1, n2 = opbinario.iguala_bases(n1, n2)

        if int(n2) > int(n1):
            aux = n1
            n1 = n2
            n2 = aux

        for i in range(len(n1) - 1, -1, -1):
            nu1 = int(n1[i])
            nu2 = int(n2[i])

            if nu1 - sobe == -1:
                nu1 = 1
                resul = f'{nu1 - nu2}' + resul

            else:
                nu1 -= sobe
                if nu1 - nu2 == -1:
                    resul = '1' + resul
                    sobe = 1
                else:
                    resul = f'{nu1 - nu2}' + resul
                    sobe = 0

        if sobe == 1:
            resul = '1' + resul

        return f'{int(resul)}'


    @staticmethod
    def multbin(n1,n2):
        """
        - recebe dois numeros binarios e realiza a multiplicação dos valores e retorna o resultado da operação

        :param n1: numero binario tipo str
        :param n2: numero binario tipo str

        :return: resultado da operação
        """

        if len(n2) > len(n1):
            aux = n1
            n1 = n2
            n2 = aux

        mult = []
        deslocamento = 0
        for i in range(len(n2) - 1, -1, -1):

            if n2[i] == '1':
                mult.append(n1 + ('0'*deslocamento))
            else:
                aux = '0' * len(n1)
                mult.append(aux + ('0'*deslocamento))

            deslocamento+=1

        resul = mult[0]
        for i in range(1,len(mult)):
            resul = opbinario.somabin(resul,mult[i])

        return f'{int(resul)}'


    @staticmethod
    def divbin(n1,n2):
        """
        - recebe dois numeros binarios e realiza a divisão dos
        valores e retorna o resultado da operação

        obs: O primeiro numero(dividendo) tem que ser maior ou igual
        ao segundo numero(dividendo) para que a operação seja valida

        :param n1: numero binario tipo str
        :param n2: numero binario tipo str

        :return: resultado da operação
        """

        dividendo = n1[:len(n2)]
        i = len(n2) - 1

        if int(n2) > int(n1):
            return None
        elif n1 == n2:
            return '1'
        elif int(dividendo) < int(n2):
            i = len(n2)
            dividendo += n1[i]

        resto = -1

        resul = '1'
        while i < len(n1):

            if int(dividendo) >= int(n2):
                resto = opbinario.subbin(dividendo,n2)

            i += 1
            if i < len(n1):
                dividendo = resto + n1[i]
                resto = int(dividendo)
                resto = str(resto)

                if int(dividendo) >= int(n2):
                    resul+= '1'
                else:
                    resul += '0'

        return resul


    @staticmethod
    def And(n1,n2):
        """
        - recebe dois numeros binarios e realiza a operação logica AND
        entre os valores e retorna o resultado da operação

        :param n1: numero binario tipo str
        :param n2: numero binario tipo str

        :return: resultado da operação
        """

        n1, n2 = opbinario.iguala_bases(n1, n2)

        resul = ''
        for i in range(0,len(n1)):
            r = '0'
            if n1[i] == '1' and n2[i] == '1':
                r = '1'

            resul += r

        return f'{int(resul)}'

    @staticmethod
    def Or(n1, n2):
        """
        - recebe dois numeros binarios e realiza a operação logica OR
        entre os valores e retorna o resultado da operação

        :param n1: numero binario tipo str
        :param n2: numero binario tipo str

        :return: resultado da operação
        """

        n1, n2 = opbinario.iguala_bases(n1, n2)

        resul = ''
        for i in range(0,len(n1)):
            r = '1'
            if n1[i] == '0' and n2[i] == '0':
                r = '0'

            resul += r

        return f'{int(resul)}'

    @staticmethod
    def Xor(n1, n2):
        """
        - recebe dois numeros binarios e realiza a operação logica XOR
        entre os valores e retorna o resultado da operação

        :param n1: numero binario tipo str
        :param n2: numero binario tipo str

        :return: resultado da operação
        """

        n1, n2 = opbinario.iguala_bases(n1, n2)

        resul = ''
        for i in range(len(n1) - 1, -1, -1):
            if n1[i] == n2[i]:
                resul = '0' + resul
            else:
                resul = '1' + resul


        return f'{int(resul)}'
