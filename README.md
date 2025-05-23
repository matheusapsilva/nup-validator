# Validador de Número Único de Protocolo (NUP)

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)

Este projeto, desenvolvido em **Python**, implementa um validador para o **Número Único de Protocolo (NUP)**, conforme estabelecido pela [Portaria Interministerial nº 11, de 25 de novembro de 2019](https://www.gov.br/gestao/pt-br/assuntos/processo-eletronico-nacional/conteudo/numero-unico-de-protocolo-nup) e regulamentado pelo Ministério da Economia.

O NUP é utilizado para identificar de forma unívoca os processos e documentos no âmbito dos órgãos e entidades da Administração Pública Federal. Ele segue o formato `NNNNN.NNNNNN/AAAA-DD`, onde:

- `NNNNN`: Código da unidade protocolizadora (5 dígitos)
- `NNNNNN`: Número sequencial do processo (6 dígitos)
- `AAAA` ou `AA`: Ano de registro (4 ou 2 dígitos)
- `DD`: Dígitos verificadores (calculados via Módulo 11)

---

## 📌 Funcionalidades

- Validação completa do NUP, incluindo:
  - Formato correto (pontuação e separadores)
  - Dígitos verificadores com algoritmo Módulo 11
  - Casos especiais como `"S/N"` para processos sem número
  - Suporte a anos com 2 ou 4 dígitos (conforme normatização)

---

## ✅ Exemplo de uso

```bash
python nup_validator.py 12345.678901/2023-94
```

Saída esperada:

```
NUP válido
```

---

## 🧪 Testes automatizados

Este projeto inclui testes automatizados com [`pytest`](https://docs.pytest.org/).

### ✅ Executando os testes

Para rodar os testes, basta executar o seguinte comando no terminal a partir da raiz do projeto:

```bash
pytest
```

> ✔️ O caminho do módulo é configurado automaticamente no início do arquivo de teste (`sys.path.insert(...)`), então **não é necessário definir `PYTHONPATH` manualmente**.

### 📄 Estrutura dos testes

Os testes estão localizados na pasta `tests/` e cobrem:

- NUPs válidos (incluindo anos abreviados e `"S/N"`)
- Formatos inválidos
- Dígitos verificadores incorretos

### 🧪 Exemplo de saída

```bash
=========================== test session starts ===========================
collected 6 items

tests/test_nup_validator.py ......                              [100%]

============================ 6 passed in 0.02s ============================
```

---

## 📁 Estrutura do Projeto

```
validate-nup/
├── nup_validator.py           # Script principal
├── tests/
│   └── test_nup_validator.py  # Testes com pytest
├── README.md
```

---

## 👨‍💻 Autor

- Matheus Antônio Pereira da Silva  
- Criado em: 10/05/2024  
- Última atualização: 04/04/2025
