import yaml
import re
import sys

def parse_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def modify_rand(expr):
    # YAML -> XML
    # rand(a, b) -> a + rand(b.0)
    # rand(a) -> rand(a.0)
    # randint(a, b) -> a + rand(b)
    # randint(a) -> rand(a)
    
    # Process randint first so it doesn't conflict with rand
    def repl_randint_ab(m):
        return f"{m.group(1)} + rand({m.group(2)})"
    
    def repl_randint_a(m):
        return f"rand({m.group(1)})"

    def to_float_str(val):
        val = val.strip()
        if '.' not in val:
            return val + '.0'
        return val

    def repl_rand_ab(m):
        return f"{m.group(1)} + rand({to_float_str(m.group(2))})"

    def repl_rand_a(m):
        return f"rand({to_float_str(m.group(1))})"

    expr = re.sub(r'randint\s*\(\s*([^,]+?)\s*,\s*([^)]+?)\s*\)', repl_randint_ab, expr)
    expr = re.sub(r'randint\s*\(\s*([^,)]+?)\s*\)', repl_randint_a, expr)
    expr = re.sub(r'rand\s*\(\s*([^,]+?)\s*,\s*([^)]+?)\s*\)', repl_rand_ab, expr)
    expr = re.sub(r'rand\s*\(\s*([^,)]+?)\s*\)', repl_rand_a, expr)
    
    return expr

def process_question(q, stack_base, input_template, prt_template):
    # Extract defaults
    testoptions_default = str(q.get('testoptions', '0.05'))
    global_s = str(q.get('significantfigures', '0'))
    
    q_name = q.get('name', 'Generated Question')
    q_penalty = str(q.get('penalty', '0.1'))
    q_text = q.get('questiontext', '')
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
        v_val = "0"
        
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
        expr = modify_rand(str(expr))
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
                   r'\g<1>' + q_text + r'\g<2>', xml_q, flags=re.DOTALL)
                   
    xml_q = re.sub(r'(<questionvariables>\s*<text>).*?(</text>\s*</questionvariables>)', 
                   r'\g<1>' + qv_text + r'\g<2>', xml_q, flags=re.DOTALL)
                   
    xml_q = re.sub(r'(<questionnote>\s*<text>).*?(</text>\s*</questionnote>)', 
                   r'\g<1>' + q_notes + r'\g<2>', xml_q, flags=re.DOTALL)
    
    # Insert inputs and prts before </question>
    xml_q = re.sub(r'</question>', f'{inputs_xml}\n{prts_xml}\n</question>', xml_q)
    
    return xml_q


def main():
    if len(sys.argv) < 3:
        yaml_file = 'stack_example.yaml'
        xml_file = 'stack_example.xml'
    else:
        yaml_file = sys.argv[1]
        xml_file = sys.argv[2]
        
    out_file = 'stack_output.xml'
    if len(sys.argv) > 3:
        out_file = sys.argv[3]
        
    data = parse_yaml(yaml_file)
    with open(xml_file, 'r', encoding='utf-8') as f:
        xml = f.read()
        
    category_match = re.search(r'(<question type="category">.*?</question>)', xml, re.DOTALL)
    category_xml = category_match.group(1) if category_match else ""
    
    cat_name = "Geometria"
    if isinstance(data, list):
        for item in data:
            if 'category' in item:
                cat_name = item['category']
                break
    else:
        cat_name = data.get('category', 'Geometria')

    if category_xml:
        category_xml = re.sub(r'(<category>\s*<text>).*?(</text>\s*</category>)', 
                              r'\g<1>top/' + str(cat_name) + r'\g<2>', category_xml, flags=re.DOTALL)

    stack_match = re.search(r'(<question type="stack">.*?</question>)', xml, re.DOTALL)
    if not stack_match:
        print("Stack template not found in XML!")
        sys.exit(1)
        
    stack_template = stack_match.group(1)

    input_match = re.search(r'(<input>.*?</input>)', stack_template, re.DOTALL)
    input_template = input_match.group(1) if input_match else ""

    prt_match = re.search(r'(<prt>.*?</prt>)', stack_template, re.DOTALL)
    prt_template = prt_match.group(1) if prt_match else ""

    stack_base = re.sub(r'<input>.*?</input>\s*', '', stack_template, flags=re.DOTALL)
    stack_base = re.sub(r'<prt>.*?</prt>\s*', '', stack_base, flags=re.DOTALL)

    out = ['<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n']
    if category_xml:
        out.append(category_xml + '\n')

    items = data if isinstance(data, list) else [data]
    for q in items:
        if 'type' in q and q['type'] == 'numerical':
            xml_q = process_question(q, stack_base, input_template, prt_template)
            out.append(xml_q + '\n')

    out.append('</quiz>\n')

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("".join(out))
        
    print(f"Generated {out_file} successfully.")

if __name__ == '__main__':
    main()
