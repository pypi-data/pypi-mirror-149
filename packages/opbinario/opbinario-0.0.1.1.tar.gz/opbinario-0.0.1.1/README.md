opbinario
===========

### Este pacote tem como objetivo oferecer funções para realização de operações com numeros binarios como: converção de bases, operações aritimeticas e operações logicas entre numeros binarios.

## Instalação
    pip install opbinario

# Exemplos de Uso:
## Importando pacote:
    from opbinario.opbinario import opbinario

## Convertendo um numero decimal para binario:
##### Para converter um numero para binario podemos utilizar a função opbinario.bin(), esta função recebe um numero decimal positivo e retorna o numero convertido para binario.
    opbinario.bin(10)


## Convertendo um numero binario para decimal:
##### Para converter um numero binario para decimal podemos utilizar a função opbinario.dec(), esta função recebe uma string contendo um numero binario e retorna o numero convertido para decimal.
    opbinario.dec('101')

## Convertendo uma string para binario:
##### Para converter uma string para binario podemos utilizar a função opbinario.strbin(), esta função recebe uma string e retorna a string convertida em binario.
    opbinario.strbin('hello world')

## Convertendo um numero binario para string:
##### Para converter um numero binario para string podemos utilizar a função opbinario.binstr(), esta função recebe uma string contendo um numero binario ou um conjunto de numeros binarios separados por espaço e converte o numero binario para caracteres ou conjunto de caracteres.
    opbinario.binstr('1001101 1010011')

## Convertendo um numero decimal ou binario para octal:
##### Para converter um numero decimal ou binario para octal podemos utilizar a função opbinario.oct(), esta função recebe um numero decimal positivo ou uma string contendo um numero binario e converte o numero decimal ou binario para octal.
    opbinario.oct(71)
    opbinario.oct('111001')

## Convertendo um numero decimal ou binario para hexadecimal:
##### Para converter um numero decimal ou binario para hexadecimal podemos utilizar a função opbinario.hex(), esta função recebe um numero decimal positivo ou uma string contendo um numero binario e converte o numero decimal ou binario para hexadecimal.
    opbinario.hex(71)
    opbinario.hex('01110001')


## Somando dois numeros binarios:
##### Para somar numeros binarios podemos utilizar a função opbinario.somabin(), esta função recebe dois numeros binarios e realiza a soma dos valores e retorna o resultado da operação.
    opbinario.somabin('1010','101')

## Subtraindo dois numeros binarios:
##### Para subtrair numeros binarios podemos utilizar a função opbinario.subbin(), esta função recebe dois numeros binarios e realiza a subtração dos valores e retorna o resultado da operação.
    opbinario.subbin('1010','101')

## Multiplicando dois numeros binarios:
##### Para multiplicar numeros binarios podemos utilizar a função opbinario.multbin(), esta função recebe dois numeros binarios e realiza a multiplicação dos valores e retorna o resultado da operação.
    opbinario.multbin('1010','101')

## Dividindo dois numeros binarios:
##### Para dividir numeros binarios podemos utilizar a função opbinario.divbin(), esta função recebe dois numeros binarios e realiza a divisão dos valores e retorna o resultado da operação.
    opbinario.divbin('1010','101')


## Realizando operação AND entre dois numeros binarios:
##### Para realizando operação AND entre dois numeros binarios podemos utilizar a função opbinario.And(), esta função recebe dois numeros binarios e realiza a operação logica AND entre os valores e retorna o resultado da operação.
    opbinario.And('1010','101')

## Realizando operação OR entre dois numeros binarios:
##### Para realizando operação Or entre dois numeros binarios podemos utilizar a função opbinario.Or(), esta função recebe dois numeros binarios e realiza a operação logica OR entre os valores e retorna o resultado da operação
    opbinario.Or('1010','101')

## Realizando operação Xor entre dois numeros binarios:
##### Para realizando operação Xor entre dois numeros binarios podemos utilizar a função opbinario.Xor(), esta função recebe dois numeros binarios e realiza a operação logica XOR entre os valores e retorna o resultado da operação.
    opbinario.Xor('1010','101')
