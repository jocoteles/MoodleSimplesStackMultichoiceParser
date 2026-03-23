import yaml
import re
import sys
import markdown

def parse_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def markdown_to_html(text, displaystyle=True):
    # LaTeX fixes: replace \ds with \displaystyle and optionally prepend \displaystyle
    def fix_latex(m):
        content = m.group(2)
        # First always replace \ds with \displaystyle
        content = re.sub(r'\\ds\b', r'\\displaystyle ', content)
        if displaystyle:
            inner = content.strip()
            # If not starting with \displaystyle, add it
            if not inner.startswith('\\displaystyle'):
                content = '\\displaystyle ' + content
        return m.group(1) + content + m.group(3)
    
    # Match \( ... \) and \[ ... \]
    text = re.sub(r'(\\\(|\\\[)(.*?)(\\\)|\\\])', fix_latex, text, flags=re.DOTALL)

    # Escape backslashes so that markdown doesn't strip them (e.g. \( -> \\( )
    text = text.replace('\\', '\\\\')
    
    # Ensure there's a blank line before list starts if one is missing
    text = re.sub(r'([^\n])\n\s*([-*+]|\d+\.)\s+', r'\1\n\n\2 ', text)
    
    return markdown.markdown(text, extensions=['extra', 'nl2br'])


def process_stack_question(q, stack_base, input_template, prt_template, displaystyle=True):
    # Extract defaults
    testoptions_default = str(q.get('testoptions', '0.05'))
    global_s = str(q.get('significantfigures', '0'))
    
    q_name = q.get('name', 'Generated Question')
    q_penalty = str(q.get('penalty', '0.1'))
    q_text = q.get('questiontext', '')

    # Convert Markdown to HTML
    q_text = markdown_to_html(q_text, displaystyle=displaystyle)
    
    q_vars = q.get('questionvariables', {})
    
    inputs_xml = ""
    prts_xml = ""
    
    # Keep track of significant figures for variables
    var_sigs = {}
    
    # Process [[...]] -> outputs
    q_notes_vars = []
    
    def replace_output(m):
        inner = m.group(1).strip()
        parts = [p.strip() for p in inner.split(',')]
        var_name = parts[0]
        
        s_val = global_s
        for part in parts[1:]:
            part = part.strip()
            if part.startswith('s:'):
                s_val = part[2:]
        
        var_sigs[var_name] = s_val
        if var_name not in q_notes_vars:
            q_notes_vars.append(var_name)
            
        return f"{{@{var_name}@}}"
        
    q_text = re.sub(r'\[\[([^\]]+)\]\]', replace_output, q_text)
    
    # Keep track of significant figures for variables
    # Process {{...}} -> inputs
    input_counter = 1
    
    def replace_input(m):
        nonlocal input_counter, inputs_xml, prts_xml
        inner = m.group(1).strip()
        trailing_text = m.group(2)
        
        parts = [p.strip() for p in inner.split(',')]
        var_name = parts[0]
        
        s_val = global_s
        v_val = "1"
        
        for part in parts[1:]:
            part = part.strip()
            if part.startswith('s:'):
                s_val = part[2:]
            elif part.startswith('v:'):
                v_val = part[2:]
                
        var_sigs[var_name] = s_val
        
        ans_name = f"ans{input_counter}"
        prt_name = f"prt{input_counter}"
        
        # Format input XML
        curr_input = input_template
        curr_input = re.sub(r'<name>.*?</name>', f'<name>{ans_name}</name>', curr_input, count=1)
        curr_input = re.sub(r'<tans>.*?</tans>', f'<tans>{var_name}</tans>', curr_input)
        inputs_xml += curr_input + "\n"
        
        # Format PRT XML
        curr_prt = prt_template
        curr_prt = re.sub(r'<name>.*?</name>', f'<name>{prt_name}</name>', curr_prt, count=1)
        curr_prt = re.sub(r'<value>.*?</value>', f'<value>{v_val}.0000000</value>', curr_prt, count=1)
        curr_prt = re.sub(r'<sans>.*?</sans>', f'<sans>{ans_name}</sans>', curr_prt)
        curr_prt = re.sub(r'<tans>.*?</tans>', f'<tans>{var_name}</tans>', curr_prt)
        curr_prt = re.sub(r'<testoptions>.*?</testoptions>', f'<testoptions>{testoptions_default}</testoptions>', curr_prt)
        curr_prt = re.sub(r'<trueanswernote>.*?</trueanswernote>', f'<trueanswernote>{prt_name}-1-T</trueanswernote>', curr_prt)
        curr_prt = re.sub(r'<falseanswernote>.*?</falseanswernote>', f'<falseanswernote>{prt_name}-1-F</falseanswernote>', curr_prt)
        prts_xml += curr_prt + "\n"
        
        input_counter += 1
        return f"[[input:{ans_name}]]{trailing_text} [[validation:{ans_name}]] [[feedback:{prt_name}]]"
        
    q_text = re.sub(r'\{\{([^}]+)\}\}([^<]*)', replace_input, q_text)
    
    # Process questionvariables
    qv_lines = []
    for var_name, expr in q_vars.items():
        expr = str(expr)
        s_val = var_sigs.get(var_name, global_s)
        if s_val == "0":
            qv_lines.append(f"{var_name}: {expr};")
        else:
            qv_lines.append(f"{var_name}: significantfigures({expr}, {s_val});")
            
    qv_text = "\n".join(qv_lines)
    
    # Questionnote
    q_notes = ", ".join([f"{v}={{@{v}@}}" for v in q_notes_vars])
    
    # Fill in the stack_base
    xml_q = stack_base
    xml_q = re.sub(r'(<name>\s*<text>).*?(</text>\s*</name>)', r'\g<1>' + q_name + r'\g<2>', xml_q, flags=re.DOTALL)
    xml_q = re.sub(r'<penalty>.*?</penalty>', f'<penalty>{q_penalty}</penalty>', xml_q)
    
    # Handle CDATA in questiontext
    xml_q = re.sub(r'(<questiontext format="html">\s*<text><!\[CDATA\[).*?(\]\]></text>\s*</questiontext>)', 
                   lambda m: m.group(1) + q_text + m.group(2), xml_q, flags=re.DOTALL)
                   
    xml_q = re.sub(r'(<questionvariables>\s*<text>).*?(</text>\s*</questionvariables>)', 
                   lambda m: m.group(1) + qv_text + m.group(2), xml_q, flags=re.DOTALL)
                   
    xml_q = re.sub(r'(<questionnote>\s*<text>).*?(</text>\s*</questionnote>)', 
                   lambda m: m.group(1) + q_notes + m.group(2), xml_q, flags=re.DOTALL)
    
    # Insert inputs and prts before </question>
    xml_q = re.sub(r'</question>', f'{inputs_xml}\n{prts_xml}\n</question>', xml_q)
    
    return xml_q


def process_multichoice_question(q, multichoice_base, answer_template, displaystyle=True):
    q_name = q.get('name', 'Generated Multichoice Question')
    q_penalty = str(q.get('penalty', '0.3333333'))
    q_text_raw = q.get('questiontext', '')
    
    # Parse options from questiontext
    # Expected format: "- Option text [percentage%]"
    lines = q_text_raw.split('\n')
    body_lines = []
    options = []
    
    option_re = re.compile(r'^\s*-\s+(.*?)\s*\[([+-]?\d+)\s*%\]\s*$')
    
    for line in lines:
        match = option_re.match(line)
        if match:
            opt_text = match.group(1)
            opt_fraction = match.group(2)
            options.append({'text': opt_text, 'fraction': opt_fraction})
        else:
            body_lines.append(line)
            
    q_text = "\n".join(body_lines).strip()
    q_text = markdown_to_html(q_text, displaystyle=displaystyle)
    
    answers_xml = ""
    for opt in options:
        opt_html = markdown_to_html(opt["text"], displaystyle=displaystyle)
        curr_ans = answer_template
        curr_ans = re.sub(r'fraction=".*?"', f'fraction="{opt["fraction"]}"', curr_ans)
        curr_ans = re.sub(r'(<text><!\[CDATA\[).*?(\]\]></text>)', 
                          lambda m: m.group(1) + opt_html + m.group(2), curr_ans, flags=re.DOTALL)
        answers_xml += curr_ans + "\n"
        
    xml_q = multichoice_base
    xml_q = re.sub(r'(<name>\s*<text>).*?(</text>\s*</name>)', lambda m: m.group(1) + q_name + m.group(2), xml_q, flags=re.DOTALL)
    xml_q = re.sub(r'<penalty>.*?</penalty>', f'<penalty>{q_penalty}</penalty>', xml_q)
    xml_q = re.sub(r'(<questiontext format="html">\s*<text><!\[CDATA\[).*?(\]\]></text>\s*</questiontext>)', 
                   lambda m: m.group(1) + q_text + m.group(2), xml_q, flags=re.DOTALL)
    
    # Toggle single/multiple choice based on whether there's a 100% option? 
    # Or just keep template default. Let's look at template.
    # multichoice_template.xml has <single>false</single>
    
    # Insert answers before </question>
    xml_q = re.sub(r'</question>', f'{answers_xml}\n</question>', xml_q)
    
    return xml_q


def load_template(template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        xml = f.read()
    
    stack_match = re.search(r'(<question type="stack">.*?</question>)', xml, re.DOTALL)
    if stack_match:
        stack_template = stack_match.group(1)
        input_match = re.search(r'(<input>.*?</input>)', stack_template, re.DOTALL)
        input_template = input_match.group(1) if input_match else ""
        prt_match = re.search(r'(<prt>.*?</prt>)', stack_template, re.DOTALL)
        prt_template = prt_match.group(1) if prt_match else ""
        stack_base = re.sub(r'<input>.*?</input>\s*', '', stack_template, flags=re.DOTALL)
        stack_base = re.sub(r'<prt>.*?</prt>\s*', '', stack_base, flags=re.DOTALL)
        return {'type': 'stack', 'base': stack_base, 'input': input_template, 'prt': prt_template}
    
    mc_match = re.search(r'(<question type="multichoice">.*?</question>)', xml, re.DOTALL)
    if mc_match:
        mc_template = mc_match.group(1)
        answer_match = re.search(r'(<answer\b.*?>.*?</answer>)', mc_template, re.DOTALL)
        answer_template = answer_match.group(1) if answer_match else ""
        mc_base = re.sub(r'<answer\b.*?>.*?</answer>\s*', '', mc_template, flags=re.DOTALL)
        return {'type': 'multichoice', 'base': mc_base, 'answer': answer_template}
    
    return None


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 xml_parser.py <arquivo_yaml> [saida_xml]")
        print("  <arquivo_yaml>  : arquivo YAML com as questões (obrigatório)")
        print("  [saida_xml]     : arquivo XML de saída (padrão: output.xml)")
        sys.exit(1)

    yaml_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else 'output.xml'
        
    data = parse_yaml(yaml_file)
    
    # Load all needed templates
    templates = {
        'numerical': load_template('stacknumerical_template.xml'),
        'algebraic': load_template('stackalgebraic_template.xml'),
        'multichoice': load_template('multichoice_template.xml')
    }
    
    # For category XML, use numerical template as base if available
    with open('stacknumerical_template.xml', 'r', encoding='utf-8') as f:
        xml_cat_base = f.read()
    
    category_match = re.search(r'(<question type="category">.*?</question>)', xml_cat_base, re.DOTALL)
    category_xml = category_match.group(1) if category_match else ""
    
    cat_name = "StackQuestions"
    if isinstance(data, list):
        for item in data:
            if 'category' in item:
                cat_name = item['category']
                break
    else:
        cat_name = data.get('category', 'StackQuestions')

    if category_xml:
        category_xml = re.sub(r'(<category>\s*<text>).*?(</text>\s*</category>)', 
                               r'\g<1>top/' + str(cat_name) + r'\g<2>', category_xml, flags=re.DOTALL)

    out = ['<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n']
    if category_xml:
        out.append(category_xml + '\n')

    items = data if isinstance(data, list) else [data]
    for q in items:
        q_type = q.get('type')
        if not q_type: continue
        
        # Displaystyle option: default is True (case-insensitive)
        ds = str(q.get('displaystyle', 'true')).lower() == 'true'
        
        if q_type in ['numerical', 'algebraic']:
            tpl = templates.get(q_type)
            if tpl:
                xml_q = process_stack_question(q, tpl['base'], tpl['input'], tpl['prt'], displaystyle=ds)
                out.append(xml_q + '\n')
            else:
                print(f"Warning: Template for {q_type} not found.")
        elif q_type == 'multichoice':
            tpl = templates.get('multichoice')
            if tpl:
                xml_q = process_multichoice_question(q, tpl['base'], tpl['answer'], displaystyle=ds)
                out.append(xml_q + '\n')
            else:
                print(f"Warning: Template for multichoice not found.")

    out.append('</quiz>\n')

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("".join(out))
        
    print(f"Generated {out_file} successfully.")

if __name__ == '__main__':
    main()
