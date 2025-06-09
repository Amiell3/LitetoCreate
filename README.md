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

  Instale usando o pip:
  ```
  pip install "nbtlib==1.12.1"
  ```
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

No terminal/prompt, execute:

python schem2nbt.py -i caminho/para/sua_estrutura.schematic


O arquivo `.nbt` será gerado na mesma pasta, com o mesmo nome.

#### Opções

- `-i`, `--input`: Caminho do arquivo `.schematic` de entrada (obrigatório)
- `-o`, `--output`: Caminho do arquivo `.nbt` de saída (opcional)
- `-f`, `--folder`: Converter todos os `.schematic` de uma pasta
- `-v`, `--verbose`: Mostra logs detalhados

Exemplo para converter todos os arquivos de uma pasta:

python schem2nbt.py -i ./minhas-schematics -f


---

## 🛠️ Funcionalidades

- Converte `.schematic` para `.nbt` compatível com Structure Block e Schematicannon (Create)
- Suporte a arquivos WorldEdit clássicos
- Corrige IDs negativos de blocos automaticamente
- Processa entidades de bloco (TileEntities)

---

## 📁 Estrutura do Projeto

schem2nbt.py
README.md
requirements.txt


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



