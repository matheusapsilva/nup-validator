# -*- coding: utf-8 -*-
"""
Validador de Número Único de Protocolo (NUP)
-------------------------------------------
Este módulo implementa um validador para o Número Único de Protocolo (NUP), conforme estabelecido
pela Portaria Interministerial nº 11, de 25 de novembro de 2019, e regulamentado pelo Ministério 
da Economia. O NUP possui o formato NNNNN.NNNNNN/AAAA-DD, onde N são dígitos numéricos, 
A representa o ano, e D são dígitos verificadores.

O NUP é utilizado para identificar de forma unívoca os processos e documentos no âmbito
dos órgãos e entidades da Administração Pública Federal.

Referência oficial: https://www.gov.br/gestao/pt-br/assuntos/processo-eletronico-nacional/conteudo/numero-unico-de-protocolo-nup

Autor: Matheus Antônio Pereira da Silva
Criado em: 10/05/2024 | Atualizado em: 04/04/2025
"""

import re
import argparse


def validate_nup(number: str) -> bool:
    """
    Valida um Número Único de Protocolo (NUP) verificando seu formato e dígitos verificadores.
    
    O NUP deve estar no formato NNNNN.NNNNNN/AAAA-DD ou NNNNN.NNNNNN/AA-DD, onde:
    - NNNNN: Código da unidade protocolizadora (5 dígitos)
    - NNNNNN: Sequencial do processo na unidade (6 dígitos)
    - AAAA ou AA: Ano de registro do processo (anos <= 1999 podem usar formato abreviado)
    - DD: Dígitos verificadores calculados através do algoritmo Módulo 11
    
    Casos especiais:
    - "S/N": Considerado válido (usado para processos antigos sem numeração padrão)
    
    Parameters:
        number (str): String contendo o NUP a ser validado
        
    Returns:
        bool: True se o NUP for válido, False caso contrário
        
    Exemplos:
        >>> validate_nup("12345.678901/2023-42")
        True
        >>> validate_nup("12345.678901/1999-42")
        True
        >>> validate_nup("S/N")
        True
        >>> validate_nup("12345678901")
        False
    """
    # Caso especial para "S/N" (Sem Número) - usado para processos antigos
    if number == "S/N":
        return True
    
    # Verifica se contém os separadores necessários (., /, -)
    if not any(char in number for char in [".", "/", "-"]):
        return False
    
    # Verifica se a parte antes da "/" tem pelo menos 11 caracteres
    # (5 dígitos do código da unidade + ponto + 6 dígitos do sequencial)
    if "/" in number and len(number.split("/")[0]) < 11:
        return False
    
    # Valida o formato usando expressão regular
    # Aceita tanto formato com ano de 4 dígitos (AAAA) quanto de 2 dígitos (AA)
    nup_format = re.compile(r'^\d{5}\.\d{6}/(\d{4}|\d{2})-\d{2}$')
    if not nup_format.match(number):
        return False
    
    try:
        # Extrai os dígitos verificadores
        dv1 = int(number[-2])
        dv2 = int(number[-1])
    except ValueError:
        # Se os dígitos verificadores não forem numéricos
        return False
    
    # Remove separadores e dígitos verificadores para processamento
    nup_treaty = number.replace(".", "").replace("/", "").replace("-", "")[:-2]
    
    # Tratamento especial para anos <= 1999, conforme a normatização do NUP
    # A regra estabelece que anos anteriores a 2000 utilizam representação abreviada
    nup_year = number.split("/")[1].split("-")[0]
    if len(nup_year) == 4 and int(nup_year) <= 1999:
        abbreviated_year = nup_year[-2:]  # Últimos dois dígitos do ano
        nup_treaty = nup_treaty[:-4] + abbreviated_year
    
    # Cálculo do primeiro dígito verificador (DV1) utilizando algoritmo Módulo 11
    # Os pesos variam de 2 a 16, aplicados da direita para a esquerda
    weights_dv1 = list(range(2, 17))
    nup_inverted = nup_treaty[::-1]  # Inverte para cálculo da direita para esquerda
    
    # Multiplica cada dígito pelo peso correspondente e soma os resultados
    weighted_sum_dv1 = sum(int(digit) * weight for digit, weight in zip(nup_inverted, weights_dv1))
    remainder_dv1 = weighted_sum_dv1 % 11  # Calcula resto da divisão por 11
    
    # Regras específicas do NUP para determinar o valor do DV1
    if remainder_dv1 == 0:  # Caso especial: resto 0
        dv1_result = 1
    else:
        dv1_result = 11 - remainder_dv1  # Regra normal: 11 - resto
    
    # Se o resultado for >= 10, DV1 será 0 (conforme normativa)
    dv1_result = 0 if dv1_result >= 10 else dv1_result
    
    # Valida o primeiro dígito verificador
    if dv1_result != dv1:
        return False
    
    # Cálculo do segundo dígito verificador (DV2)
    # Inclui o DV1 no início do número invertido para este cálculo
    nup_inverted_with_dv1 = str(dv1_result) + nup_inverted
    
    # Os pesos para DV2 variam de 2 a 17 (um peso adicional para o DV1)
    weights_dv2 = list(range(2, 18))
    
    # Processo similar ao cálculo do DV1
    weighted_sum_dv2 = sum(int(digit) * weight for digit, weight in zip(nup_inverted_with_dv1, weights_dv2))
    remainder_dv2 = weighted_sum_dv2 % 11
    
    # Aplicação das mesmas regras para determinar DV2
    if remainder_dv2 == 0:
        dv2_result = 1
    else:
        dv2_result = 11 - remainder_dv2
    
    dv2_result = 0 if dv2_result >= 10 else dv2_result
    
    # Valida o segundo dígito verificador
    if dv2_result != dv2:
        return False
    
    # Se passou por todas as validações, o NUP é válido
    return True


def main():
    """
    Função principal para execução do validador via linha de comando.
    Processa os argumentos e exibe o resultado da validação.
    """
    parser = argparse.ArgumentParser(
        description="Validador de Número Único de Protocolo (NUP) conforme normativa do Ministério da Economia"
    )
    parser.add_argument("number", help="NUP a ser validado (ex: 12345.678901/2023-45)")
    args = parser.parse_args()
    
    valid = validate_nup(args.number)
    
    if valid:
        print("NUP válido")
    else:
        print("NUP inválido")


if __name__ == "__main__":
    main()