import random


def number_guessing():
    numero_a_adivinhar = random.randint(1, 100)
    tentativas = 0
    numero_adivinhado = None
    while numero_adivinhado != numero_a_adivinhar and tentativas < 3:
        numero_adivinhado = int(input("Digite o número:\n"))
        tentativas += 1
        if numero_adivinhado > numero_a_adivinhar:
            print("Tente um número menor.\n")
        elif numero_adivinhado < numero_a_adivinhar:
            print("Tente um número maior.\n")

    if numero_adivinhado == numero_a_adivinhar:
        return f"Acertaste o numero depois de {tentativas} tentativas."
    else:
        return f"Tentativas esgotadas, o número é '{numero_a_adivinhar}'."


def main():
    print("Bem-vindo ao jogo de adivinhar números!\nTens três tentativas de adivinhar o numero escolhido de 1 a "
          "100\n\nBOA SORTE\n")
    return number_guessing()


print(main())
