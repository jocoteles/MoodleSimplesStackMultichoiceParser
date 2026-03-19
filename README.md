# Moodle STACK Random Generator Parser

O script `stack_parser.py` facilita a geração de pacotes XML compatíveis com o formato de questões numéricas randômicas do plugin **STACK** no Moodle. Em vez de escrever e manipular XML complexo diretamente, você define todos os parâmetros e lógicas numéricas através de um documento formato YAML.

## Como Executar
```bash
python3 stack_parser.py <arquivo_yaml> <template_xml> <saida_xml>
```
Se omitidos, os argumentos padrão são `stack_example.yaml`, `stack_example.xml` e produzirá `stack_output.xml`. É altamente recomendável usar um template limpo (como `stack_template.xml`) em vez de um arquivo cheio de questões exportadas, já que o parser utilizará a primeira questão nele como a matriz de configuração (fôrma) para construir as demais.

---

## Estrutura do Arquivo YAML

O arquivo segue a sintaxe padrão do YAML dividida em itens do formulário:

1. **Definição da Categoria-mãe (Opcional)**
```yaml
- category: Geometria
```
Isto definirá a categoria no banco de questões do Moodle como `top/Geometria`. Se não for informada, ela assume "Geometria" como padrão.

2. **Definição da(s) Questão(ões)**
Todo novo bloco precedido por `-` deve possuir as seguintes propriedades (ou omitirá quando defaults estiverem listados):

```yaml
- id: 0001
  name: Nome da Questão
  type: numerical
  testoptions: 0.1 # opcional: Tolerância da resposta (default: 0.05)
  significantfigures: 1 # opcional: Número padrão de algarismos significativos aplicado a TODAS as variáveis geradas nesta questão, caso não seja especificado nas tags. Útil para formatar tudo de uma vez. (default: 0, quer dizer: função 'significantfigures' desabilitada)
  penalty: 0.1 # Fator de penalidade a cada tentativa errada (default: 0.1)
  questiontext: |
    <p>... html da questão ...</p>
  questionvariables:
    var1: formula
```

---

## Sintaxe do Texto da Questão (`questiontext`)

Para evitar complicações com as tags proprietárias do STACK no texto, nós utilizamos as representações compactas abaixo via YAML:

### Variáveis de Texto / Output
Aparecem no meio do texto e transmitem valores ao estudante ao invés de pedirem respostas.
**`[[var]]`**
Irá automaticamente interpolar no Moodle a representação da variável especificada no YAML pelas chaves `{@var@}` sem exigir a declaração dessas chaves do Moodle.

*(Opcional - Modificadores)*
Você pode atribuir individualmente uma configuração específica para essa variável:
**`[[var, s:N]]`**
Sobrescreve a opção global informada na questão, forçando essa variável matemática a ter `N` algarismos significativos no Moodle.

---

### Variáveis Ocultas / Respostas do Estudante (Input)
Aparecem no lugar onde o estudante deverá formular uma resposta.
**`{{ans}}`**
O script dinamicamente criará as marcações de resposta no final ou na posição que está:
`[[input:ansX]] [[validation:ansX]] [[feedback:prtX]]`
O XML gerado automaticamente montará a "Validation Tree" e todas as tags subjacentes exigidas. Se um texto secundário ou unidade como "m³" seguir as chaves, as validações e feedbacks serão inseridos respeitosamente envolta disso.

*(Opcional - Modificadores)*
Você também possui modificadores:
**`{{ans, s:N, v:P}}`**
Onde `s:N` é algarismos significativos como acima.
E `v:P` é o valor (peso) de acerto da resposta daquela caixinha específica. Modifica a tag `<value>` da Moodle's PRT. O padrão se ocultado é peso `0.0`.

---

## Definindo as Fórmulas Matemáticas (`questionvariables`)

Dentro do bloco `questionvariables`, você deve listar suas variáveis como funções compatíveis com Maxima no formato clássico, contudo, o *stack_parser* compilará dinamicamente lógicas mais amigáveis à leitura comum. 

**Funções de Randômicos**
Você pode utilizar as seguintes notações exclusivas de pré-compilação com `rand()` / `randint()`:

* **`randint(a, b)`** :  Gera interamente um valor entre `a` e `b`. É convertido de volta em `a + rand(b)`.

* **`randint(a)`**    :  Gera inteiramente um valor entre `0` e `a`. É convertido em `rand(a)`.

* **`rand(a.0, b.0)`**:  Gera valores fracionários entre os decimais. Será convertido internamente de volta para `a.0 + rand(b.0)`.

*Nota sobre notações fracionadas*: Ao utilizar `rand(a, b)` em formato Float (decimal), sempre forneça um dos lados como um Float explícito se precisar tratar as propriedades dos floats (como `.0`), e o parser cuidará da interpolação correta das notações com `.0` onde faltar. 

### Exemplo Completo YAML

```yaml
- category: Geometria Espacial

- id: 101
  name: Volume do Paralelepípedo
  type: numerical
  penalty: 0.1
  questiontext: |
    <p>Calcule o volume de um paralelepípedo que possui largura [[x, s:2]] cm, e altura [[y]] cm com profundidade [[z]] cm.</p>
    <p>O volume é igual a {{ta1, s:2, v:5}} cm³</p>
  questionvariables:
    x: randint(10, 20)
    y: rand(2.0, 5.0)
    z: rand(2.0, 4.0)
    ta1: x*y*z
```
