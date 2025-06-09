Fork and readaptation from: JoshuaVandaele/Schem-File-to-Structure-Block-NBT-Format
---

# 🏗️ Schematic2NBT Converter para Minecraft Create

Ferramenta em Python para converter arquivos `.schematic` do WorldEdit (e `.litematic` exportados como `.schematic` pelo Litematica) para o formato `.nbt` compatível com o Schematicannon do mod Create no Minecraft.

---

## ✨ Descrição

Este script automatiza a conversão de estruturas criadas em editores populares (WorldEdit, Litematica) para o formato de estrutura vanilla (`.nbt`). Assim, você pode importar facilmente suas construções no Schematicannon do Create sem precisar abrir mods dentro do jogo.

---

## ⚙️ Requisitos

- **Python 3.8 ou superior**

  - Baixe e instale o Python no site oficial: [python.org](https://www.python.org/downloads/)
  - Durante a instalação no Windows, marque a opção **Add Python to PATH** para facilitar o uso no terminal.
  - Para Linux, você pode usar o gerenciador de pacotes da sua distribuição ou compilar a partir do código fonte. Exemplo para Ubuntu/Debian:

    ```
    sudo apt update
    sudo apt install python3 python3-pip
    ```

- **nbtlib (versão 1.12.1 recomendada)**
  Instala a biblioteca NBT que é uma estrutura de dados em forma de árvore utilizada pelo Minecraft para armazenar dados arbitrários
  
  Instale usando o pip:
  ```
  pip install "nbtlib==1.12.1"
  ```
TQDM faz com que o Script tenha a barra de progresso da conversão
  ```
  pip install tqdm
  ``` 
---

## 🚀 Guia de Uso

### 1. Prepare seu arquivo

- Para WorldEdit e Litematica use o `.schematic` exportado normalmente.

## 🚀 Guia de Uso

### 1. Prepare seu arquivo

- Para WorldEdit: use o `.schematic` exportado normalmente.
- Para Litematica: abra no Litematica e exporte como `.schematic`.

### 2. Converta para `.nbt`

No terminal/prompt, com o script e o *.schematic NA MESMA PASTA, execute:

python schem2nbt.py -i arquivo.schematic

ou

python schem2nbt.py -i caminho/para/sua_estrutura.schematic

O arquivo `.nbt` será gerado na mesma pasta, com o mesmo nome.

#### Opções

Todos os comandos possíveis do script schem2nbt.py
Baseado na estrutura do parser de argumentos, aqui estão todos os comandos possíveis para testar o script:

###Comandos básicos obrigatórios
Converter arquivo único:

```
python schem2nbt.py -i arquivo.schematic
python schem2nbt.py --input arquivo.schematic
```

# Comandos com saída personalizada

## Definir arquivo de saída:


```
python schem2nbt.py -i IndustrialFurnace.schematic -o MinhaFornalha.nbt
python schem2nbt.py --input IndustrialFurnace.schematic --output MinhaFornalha.nbt
```
# Comandos para pastas
## Converter pasta inteira:

```
python schem2nbt.py -i ./schematics -f
python schem2nbt.py --input ./schematics --folder
python schem2nbt.py -i D:\meusschematics -f -o D:\meusNBTs
```

# Comandos com logs detalhados
## Modo verbose (logs):

```
python schem2nbt.py -i arquivo.schematic -v
python schem2nbt.py --input arquivo.schematic --verbose
python schem2nbt.py -i ./pasta -f -v
```

# Combinações completas
## Todos os parâmetros:

```
python schem2nbt.py -i IndustrialFurnace.schematic -o Industrial.nbt -v
python schem2nbt.py --input ./schematics --output ./converted --folder --verbose
```

# Comandos de ajuda
## Ver ajuda:

```
python schem2nbt.py -h
python schem2nbt.py --help
```

# Para estruturas do Create mod:

```
python schem2nbt.py -i IndustrialFurnace.schematic -v
python schem2nbt.py -i ./create-builds -f -o ./nbt-files -v
```

# Comandos que devem dar erro (para testar)
## Arquivo inexistente:

```
python schem2nbt.py -i naoexiste.schematic
```
# Sem parâmetro obrigatório:

```
python schem2nbt.py
python schem2nbt.py -o saida.nbt
```
---

## 🛠️ Funcionalidades

- Converte `.schematic` para `.nbt` compatível com Structure Block e Schematicannon (Create)
- Suporte a arquivos WorldEdit clássicos
- Corrige IDs negativos de blocos automaticamente
- Processa entidades de bloco (TileEntities)

---
## 📁 Estrutura do Projeto

schem2nbt.py
---

## ❗ Observações

- Blocos de mods não são mapeados para nomes reais por padrão (aparecem como `minecraft:unknown_ID`). Para suporte avançado, personalize a função de palette.
- O script não converte `.litematic` diretamente: exporte para `.schematic` antes.
- Para grandes estruturas, o processo pode demorar alguns minutos.

---

## 🤝 Contribua

Sugestões, melhorias ou correções? Abra uma issue ou envie um pull request!

---

## 📜 Licença

MIT

---

## 📷 Exemplo de uso

python schem2nbt.py -i casa.schematic



