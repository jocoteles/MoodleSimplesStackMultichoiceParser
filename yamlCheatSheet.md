# 📑 YAML Cheat Sheet: Fundamentos e Aplicações Avançadas

O YAML é uma linguagem de serialização de dados simples, porém robusta, que alcança alta flexibilidade com apenas duas estruturas de dados: **sequências** (listas) e **mapeamentos** (pares de chave e valor).

---

## 1. Estruturas de Dados Básicas 

| Estrutura | Exemplo YAML | Descrição |
| :--- | :--- | :--- |
| **Mapping** | `Kernel: Linux` | Par de chave e valor simples. |
| **Sequence** | `- Linux` | Uma lista de itens (identificada por hífens). |
| **Mapping de Sequências** | `Fedora: [34, 35]` | Uma chave que contém múltiplos valores. |
| **Sequência de Mapeamentos**| `- CPU: AMD` | Uma lista onde cada item é um par chave-valor. |

---

## 2. Blocos de Texto e HTML (Inclusão Adicional)
Para trabalhar com variáveis de texto longas ou que contenham tags HTML e símbolos matemáticos, o YAML oferece indicadores de bloco que preservam a estrutura sem a necessidade de aspas.

### O Indicador Literal (`|`)
Mantém as quebras de linha e o formato original. Ideal para códigos HTML e enunciados complexos.
```yaml
question: |
  <p>Dado um terreno de largura <b>$x$</b> por <b>$y$</b>.</p>
  <ul>
    <li>Unidade: metros</li>
  </ul>
```

### O Indicador "Folded" (`>`)
Converte quebras de linha simples em espaços, criando um bloco de texto contínuo.
```yaml
description: >
  Este texto aparecerá como um único parágrafo
  mesmo que esteja escrito em várias linhas no arquivo.
```

---

## 3. Mapeamentos Complexos e Estruturas Compostas 

* **Mapping de Mappings:** Permite aninhar dados de forma hierárquica.
    ```yaml
    Desktop:
      CPU: AMD
      RAM: 32 GB
    ```
* **Complex Mapping (`?`):** Utilizado quando a própria "chave" é uma lista ou uma sequência.
    ```yaml
    ? 
      - Linux
      - GNU
    : Open source
    ```

---

## 4. Exemplo Prático: Banco de Questões (Mix de Conceitos)
Abaixo, uma aplicação real unindo o conteúdo do PDF  com sua necessidade de HTML:

```yaml
# Sequência de mapeamentos para questões
exercicios:
  - id: 101
    tags: [geometria, html_render]
    enunciado: |
      <div class="math-box">
        Calcule a área para $x$ e $y$:
      </div>
    variaveis:
      x: 12
      y: 31
    metadata:
      origem: "Manual de Exercícios"
      licenca: "CC BY-SA 4.0" # Referência ao padrão do PDF 
```

---

## 5. Regras de Ouro para IDEs
* **Espaçamento:** YAML é sensível à identação. Use espaços, nunca TABS.
* **JSON Compatibility:** O YAML é um superconjunto do JSON; qualquer estrutura JSON válida é um YAML válido.
* **Documentos Múltiplos:** Use `---` para separar diferentes documentos dentro do mesmo arquivo físico.

---
 *Baseado no conteúdo de Seth Kenlon (Opensource.com), licenciado sob CC BY-SA 4.0.*