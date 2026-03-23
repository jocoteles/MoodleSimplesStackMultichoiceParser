# Moodle Simple STACK e Multichoice Parser

O script `xml_parser.py` converte questões Moodle STACK randômicas (numéricas e algébricas) e questões de múltipla escolha (multichoice) definidas em YAML para o formato XML compatível com o Moodle. Em vez de editar XML complexo manualmente, o usuário descreve cada questão — variáveis, fórmulas e texto — em um arquivo YAML simples e legível. Restrito a questões com uma única resposta correta e PRTs (Potential response trees) de nodo único.

## Como Executar

```bash
python3 xml_parser.py <arquivo_yaml> [saida_xml]
```

| Argumento        | Descrição                                               | Obrigatório? | Padrão                |
|------------------|---------------------------------------------------------|--------------|-----------------------|
| `<arquivo_yaml>` | Arquivo YAML com a definição das questões               | **Sim**      | —                     |
| `[saida_xml]`    | Nome do arquivo XML gerado                              | Não          | `output.xml`    |

> [!TIP]
> O parser carrega automaticamente os templates necessários (`stacknumerical_template.xml`, `stackalgebraic_template.xml` e `multichoice_template.xml`) do diretório atual.

---

## Estrutura do Arquivo YAML

O arquivo YAML é uma lista de itens sequenciais (`-`). Ele pode conter **uma definição de categoria** e **uma ou mais definições de questões**.

### 1. Categoria (Opcional)

```yaml
- category: Geometria Espacial
```

Define a categoria no banco de questões do Moodle como `top/Geometria Espacial`. Se omitida, o padrão é **`StackQuestions`**.

### 2. Questão

Cada questão é um item da lista com as seguintes propriedades:

```yaml
- id: 0001
  name: Nome da Questão
  type: numerical
  testoptions: 0.1        # Tolerância da resposta (padrão: 0.05) - STACK
  significantfigures: 1   # Alg. significativos globais para TODAS as variáveis (padrão: 0 = desabilitado)
  penalty: 0.1            # Penalidade por tentativa errada (padrão: 0.1)
  displaystyle: true      # Força \displaystyle em todo LaTeX (padrão: true)
  questiontext: |
    Texto da questão em **Markdown**.
  questionvariables:
    var1: expressão_maxima
```

| Campo                | Descrição                                                                                     | Padrão   |
|----------------------|-----------------------------------------------------------------------------------------------|----------|
| `name`               | Nome da questão no Moodle                                                                    | —        |
| `type`               | Tipo (`numerical`, `algebraic` ou `multichoice`)                                             | —        |
| `testoptions`        | Tolerância numérica do teste de resposta (apenas STACK)                                      | `0.05`   |
| `significantfigures` | Algarismos significativos aplicados a todas as variáveis (0 = desabilitado)                   | `0`      |
| `penalty`            | Fator de penalidade por tentativa incorreta                                                  | `0.1`    |
| `displaystyle`       | Se `true`, adiciona `\displaystyle` ao início de todas as fórmulas LaTeX                     | `true`   |
| `questiontext`       | Texto da questão em **Markdown**, com as tags simplificadas descritas abaixo                 | —        |
| `questionvariables`  | Mapa de variáveis → expressões Maxima/STACK (apenas para `numerical` e `algebraic`)           | —        |

---

## Suporte a Markdown e LaTeX

O campo `questiontext` aceita sintaxe Markdown, que é convertida automaticamente para HTML.

### Controle de Display Matemático (LaTeX)

O parser inclui facilidades para o gerenciamento de fórmulas LaTeX (`\( ... \)` ou `\[ ... \]`):

- **`displaystyle`: true**: (Padrão) Insere automaticamente `\displaystyle` no início de cada expressão LaTeX da questão.
- **`\ds`**: Atalho dentro do LaTeX que é sempre convertido para `\displaystyle`. Útil se `displaystyle` global estiver desativado mas você desejar formatar apenas uma equação específica: `\(\ds \int f(x)dx \)`.

> [!IMPORTANT]
> O parser protege as barras invertidas (`\`) do Markdown, então você pode escrever fórmulas LaTeX naturalmente.

---

## Tags Simplificadas no Texto da Questão (STACK)

O `questiontext` utiliza duas notações compactas que o parser converte nas tags plenas exigidas pelo STACK (tipos `numerical` e `algebraic`).

### Variáveis de Exibição (Output): `[[var]]`

Exibe o valor de uma variável para o estudante. É convertido automaticamente em `{@var@}`.

**Modificadores opcionais:**
- `[[var, s:N]]` — Exibe a variável com `N` algarismos significativos (sobrescreve o global).

### Campos de Resposta (Input): `{{var}}`

Cria uma caixa de entrada onde o estudante digita a resposta. O parser gera automaticamente as tags `[[input:ansX]]`, `[[validation:ansX]]` e `[[feedback:prtX]]`, além dos blocos XML `<input>` e `<prt>`.

**Modificadores opcionais:**
- `{{var, s:N}}` — Algarismos significativos para a resposta.
- `{{var, v:P}}` — Peso (valor) da resposta. Modifica a tag `<value>` na PRT. **Padrão: `1.0`** (se omitido).

---

## Questões de Múltipla Escolha (`multichoice`)

Para questões do tipo `multichoice`, o texto da questão deve listar as opções usando uma lista Markdown (`- `), com a porcentagem da nota entre colchetes ao final de cada linha:

```yaml
- id: 0004
  name: Poliedros regulares
  type: multichoice
  penalty: 1.0
  questiontext: |
    Marque as afirmações verdadeiras sobre poliedros regulares.
    - As faces são polígonos quaisquer. [-30%]
    - Todos são convexos. [+30%]
    - Só existem 5 poliedros regulares. [+50%]
    - Pelo menos um deles possui face hexagonal. [-30%]
    - Todos possuem faces triangulares. [-30%]
    - Também são conhecidos como sólidos platônicos. [+20%]
```

> [!NOTE]
> O parser extrairá as linhas que começam com `-` e terminam com `[+/-XX%]` para criar as alternativas do Moodle. O restante do texto será usado como o corpo da questão.

---

## Definindo Fórmulas (`questionvariables`)

As expressões dentro de `questionvariables` são escritas na sintaxe nativa do **Maxima/STACK** e inseridas diretamente no XML gerado. O parser não faz nenhuma transformação nas expressões — elas devem ser válidas para o Maxima.

### Gerando Números Aleatórios

Use a função `rand()` nativa do STACK:

| Expressão                     | Resultado                                        |
|-------------------------------|--------------------------------------------------|
| `rand(n)`                     | Inteiro aleatório entre `0` e `n-1`              |
| `rand(n.0)`                   | Float aleatório entre `0` e `n`                  |
| `rand([a,b,c])`               | Elemento aleatório da lista                      |

**Gerar inteiro em um intervalo `[a, b)`:**
```
a + rand(b - a)
```
Exemplo: um inteiro entre 10 e 29 → `10 + rand(20)`

**Gerar float em um intervalo `[a, b)`:**
```
a + rand((b - a) * 1.0)
```
Exemplo: um float entre 2.0 e 7.0 → `2.0 + rand(5.0)`

---

## Exemplo Completo

Consulte o arquivo `questions_example.yaml` para um exemplo com os três tipos de questões suportados.

---

## Referência de Funções Matemáticas do STACK (Maxima)

As variáveis e fórmulas no campo `questionvariables` utilizam a linguagem do [Maxima](https://maxima.sourceforge.io/), customizada pelo STACK. Abaixo estão as funções mais úteis para a criação de questões numéricas.

### Geração de Aleatórios

| Função | Descrição |
|--------|-----------|
| `rand(n)` | Inteiro aleatório em `[0, n-1]` |
| `rand(n.0)` | Float aleatório em `[0, n)` |
| `rand([a,b,...])` | Seleção aleatória de uma lista |
| `rand_with_step(a, b, s)` | Aleatório no conjunto `{a, a+s, a+2s, ..., b}` |
| `rand_with_prohib(a, b, [x,...])` | Inteiro em `[a,b]` excluindo os da lista |
| `rand_selection(lista, n)` | `n` elementos distintos da lista |

### Manipulação Numérica

| Função | Descrição |
|--------|-----------|
| `significantfigures(x, n)` | Arredonda `x` para `n` algarismos significativos |
| `decimalplaces(x, n)` | Arredonda `x` para `n` casas decimais |
| `dispsf(x, n)` | Exibe `x` com `n` alg. significativos (com zeros à direita) |
| `dispdp(x, n)` | Exibe `x` com `n` casas decimais (com zeros à direita) |
| `float(x)` | Converte para ponto flutuante |
| `round(x)` | Arredonda para o inteiro mais próximo |
| `abs(x)` | Valor absoluto |
| `max(a, b)` / `min(a, b)` | Máximo / mínimo |
| `mod(a, b)` | Resto da divisão |

### Funções Algébricas

| Função | Descrição |
|--------|-----------|
| `expand(ex)` | Expande a expressão |
| `factor(ex)` | Fatora a expressão |
| `simplify(ex)` | Simplifica (equivale a `ev(fullratsimp(ex), simp)`) |
| `ratsimp(ex)` | Simplificação racional |
| `radcan(ex)` | Simplificação de radicais e logaritmos |
| `subst(valor, var, ex)` | Substitui `var` por `valor` em `ex` |
| `solve(eq, var)` | Resolve a equação para `var` |
| `comp_square(ex, v)` | Forma canônica (quadrado completo) do polinômio |

### Cálculo

| Função | Descrição |
|--------|-----------|
| `diff(ex, var)` | Derivada de `ex` em relação a `var` |
| `diff(ex, var, n)` | Derivada de ordem `n` |
| `integrate(ex, var)` | Integral indefinida |
| `integrate(ex, var, a, b)` | Integral definida de `a` a `b` |
| `limit(ex, var, val)` | Limite de `ex` quando `var → val` |
| `sum(ex, var, a, b)` | Somatório de `a` a `b` |
| `product(ex, var, a, b)` | Produtório de `a` a `b` |

### Trigonometria

| Função | Descrição |
|--------|-----------|
| `sin(x)`, `cos(x)`, `tan(x)` | Funções trigonométricas |
| `asin(x)`, `acos(x)`, `atan(x)` | Funções trigonométricas inversas |
| `atan2(y, x)` | Arco tangente de `y/x` (com quadrante correto) |

### Exponenciais e Logaritmos

| Função | Descrição |
|--------|-----------|
| `exp(x)` | Função exponencial `e^x` |
| `log(x)` ou `ln(x)` | Logaritmo natural |
| `lg(x)` | Logaritmo base 10 |
| `lg(x, b)` | Logaritmo base `b` |
| `sqrt(x)` | Raiz quadrada |

### Listas, Conjuntos e Matrizes

| Função | Descrição |
|--------|-----------|
| `makelist(ex, var, a, b)` | Cria lista avaliando `ex` para `var` de `a` a `b` |
| `append(l1, l2)` | Concatena duas listas |
| `length(L)` | Número de elementos |
| `setify(L)` / `listify(S)` | Converte lista ↔ conjunto |
| `matrix([l1], [l2], ...)` | Cria uma matriz |
| `determinant(M)` | Determinante |
| `invert(M)` | Matriz inversa |
| `transpose(M)` | Transposta |

### Constantes

| Símbolo | Valor |
|---------|-------|
| `%pi` ou `pi` | π ≈ 3.14159... |
| `%e` ou `e` | Número de Euler ≈ 2.71828... |
| `%i` ou `i` | Unidade imaginária √(-1) |
| `inf` | Infinito (∞) |

---

> [!NOTE]
> Para uma referência completa das funções do Maxima no STACK, consulte a [documentação oficial](https://docs.stack-assessment.org/en/CAS/).
