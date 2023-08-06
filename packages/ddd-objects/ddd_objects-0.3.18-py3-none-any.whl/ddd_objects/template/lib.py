import os, re
from types import FunctionType

fn_map = {
    'do_temp.py': 'infrastructure/do.py',
    'converter_temp.py': 'infrastructure/converter.py',
    'entity_temp.py': 'domain/entity.py',
    'value_obj_temp.py': 'domain/value_obj.py',
    'dto_temp.py': 'application/dto.py',
    'assembler_temp.py': 'application/assembler.py',
    'repository_impl_tmp.py': 'infrastructure/repository_impl.py',
    'repository_tmp.py': 'domain/repository.py'
}

def replace_header(target_header, source_header):
    target_header_code = '\n'.join(target_header)
    source_header_code = '\n'.join(source_header)
    # extract import code
    target_entity_code, target_rest = extract_import_entity_code(target_header_code)
    target_obj_value_code, target_rest = extract_import_value_obj_code(target_rest)
    target_converter_code, target_rest = extract_import_converter_code(target_rest)
    target_repository_code, target_rest = extract_import_repository_code(target_rest)
    target_assembler_code, target_rest = extract_import_assembler_code(target_rest)
    target_do_code, target_rest = extract_import_do_code(target_rest)
    target_dto_code, target_test = extract_import_dto_code(target_rest)
    # extract objects and subheader
    target_entities, target_entity_header = extract_object_from_import_code(target_entity_code)
    target_obj_values, target_obj_value_header = extract_object_from_import_code(target_obj_value_code)
    target_converters, target_converter_header = extract_object_from_import_code(target_converter_code)
    target_repositories, target_repository_header = extract_object_from_import_code(target_repository_code)
    target_assemblers, target_assembler_header = extract_object_from_import_code(target_assembler_code)
    target_dos, target_do_header = extract_object_from_import_code(target_do_code)
    target_dtos, target_dto_header = extract_object_from_import_code(target_dto_code)
    # extract import code
    source_entity_code, source_rest = extract_import_entity_code(source_header_code)
    source_obj_value_code, source_rest = extract_import_value_obj_code(source_rest)
    source_converter_code, source_rest = extract_import_converter_code(source_rest)
    source_repository_code, source_rest = extract_import_repository_code(source_rest)
    source_assembler_code, source_rest = extract_import_assembler_code(source_rest)
    source_do_code, source_rest = extract_import_do_code(source_rest)
    source_dto_code, source_test = extract_import_dto_code(source_rest)
    # extract objects and subheader
    source_entities, source_entity_header = extract_object_from_import_code(source_entity_code)
    source_obj_values, source_obj_value_header = extract_object_from_import_code(source_obj_value_code)
    source_converters, source_converter_header = extract_object_from_import_code(source_converter_code)
    source_repositories, source_repository_header = extract_object_from_import_code(source_repository_code)
    source_assemblers, source_assembler_header = extract_object_from_import_code(source_assembler_code)
    source_dos, source_do_header = extract_object_from_import_code(source_do_code)
    source_dtos, source_dto_header = extract_object_from_import_code(source_dto_code)
    # replace objects
    if target_entities and source_entities:
        target_entities = list(set(target_entities+source_entities))
    elif source_entities:
        target_entities = source_entities
    if target_obj_values and source_obj_values:
        target_obj_values = list(set(target_obj_values+source_obj_values))
    elif source_obj_values:
        target_obj_values = source_obj_values
    if target_converters and source_converters:
        target_converters = list(set(target_converters+source_converters))
    elif source_converters:
        target_converters = source_converters
    if target_repositories and source_repositories:
        target_repositories = list(set(target_repositories+source_repositories))
    elif source_repositories:
        target_repositories = source_repositories
    if target_assemblers and source_assemblers:
        target_assemblers = list(set(target_assemblers+source_assemblers))
    elif source_assemblers:
        target_assemblers = source_assemblers
    if target_dos and source_dos:
        target_dos = list(set(target_dos+source_dos))
    elif source_dos:
        target_dos = source_dos
    if target_dtos and source_dtos:
        target_dtos = list(set(target_dtos+source_dtos))
    elif source_dtos:
        target_dtos = source_dtos
    # replace header
    if target_entity_header is None and source_entity_header:
        target_entity_header = source_entity_header
    if target_obj_value_header is None and source_obj_value_header:
        target_obj_value_header = source_obj_value_header
    if target_converter_header is None and source_converter_header:
        target_converter_header = source_converter_header
    if target_repository_header is None and source_repository_header:
        target_repository_header = source_repository_header
    if target_assembler_header is None and source_assembler_header:
        target_assembler_header = source_assembler_header
    if target_do_header is None and source_do_header:
        target_do_header = source_do_header
    if target_dto_header is None and source_dto_header:
        target_dto_header = source_dto_header
    # replace converter declarations
    target_converter_declarations, target_rest = extract_converter_declarations(target_rest)
    source_converter_declarations, source_rest = extract_converter_declarations(source_rest)
    _all_converter_declarations = []
    for tcd in target_converter_declarations:
        if tcd.strip() not in _all_converter_declarations:
            _all_converter_declarations.append(tcd.strip())
    for scd in source_converter_declarations:
        if scd.strip() not in _all_converter_declarations:
            target_converter_declarations.append(scd)
            _all_converter_declarations.append(scd.strip())
    target_code = target_rest.strip() + '\n'
    object_code_pairs = [
        (target_entities, target_entity_header),
        (target_obj_values, target_obj_value_header),
        (target_converters, target_converter_header),
        (target_repositories, target_repository_header),
        (target_assemblers, target_assembler_header),
        (target_dos, target_do_header),
        (target_dtos, target_dto_header)
    ]
    for objs, header in object_code_pairs:
        if header is None:
            continue
        target_code += header + '\n    '
        target_code += ',\n    '.join(objs)
        target_code += '\n' + ')' + '\n'
    for tcd in target_converter_declarations:
        target_code += tcd+'\n'
    lines = [l for l in target_code.split('\n') if l.strip()]
    target_code = '\n'.join(lines)+'\n\n'
    return target_code

def replace(source_dir, fn, target=None, exclude_classes=[]):
    target_root_dir = f'{source_dir}/..'
    if target is None:
        target = fn_map[fn]
    target_fn = f'{target_root_dir}/{target}'
    source_fn = os.path.join(source_dir, fn)
    if os.path.exists(target_fn):
        with open(target_fn, 'r') as f:
            _target_classes = f.read().strip().split('\n\n')
            _target_classes = [t for t in _target_classes if t.strip()]
            target_classes = []
            prev_class = ''
            for c in _target_classes:
                if is_first_char_space(c):
                    prev_class += '\n'+c
                else:
                    target_classes.append(prev_class)
                    prev_class = c
            if prev_class:
                target_classes.append(prev_class)
            target_classes, target_header = _extract_class(target_classes)
    else:
        target_classes = {}
        target_header = None
    with open(source_fn, 'r') as f:
        _source_classes = f.read().strip().split('\n\n')
        source_classes = []
        prev_class = ''
        for c in _source_classes:
            if is_first_char_space(c):
                prev_class += c
            else:
                source_classes.append(prev_class)
                prev_class = c
        if prev_class:
            source_classes.append(prev_class)
        source_classes, source_header = _extract_class(source_classes, exclude_classes)
    target_classes.update(source_classes)
    if not target_header:
        target_header = source_header
    target_code = replace_header(target_header, source_header)
    target_code +=  '\n\n'.join(list(target_classes.values()))
    with open(target_fn, 'w') as f:
        f.write(target_code)

def replace_class_functions(source_dir, fn, target=None, exclude_classes=[]):
    target_root_dir = f'{source_dir}/..'
    if target is None:
        target = fn_map[fn]
    target_fn = f'{target_root_dir}/{target}'
    source_fn = os.path.join(source_dir, fn)
    class_pattern = r' *\n *\n *\n'
    function_pattern = r' *\n *\n'
    target_classes_functions = {}
    source_classes_functions = {}
    if os.path.exists(target_fn):
        with open(target_fn, 'r') as f:
            target_class_strings = re.split(class_pattern, f.read().strip())
            target_class_strings = [t for t in target_class_strings if t.strip()]
            target_classes, target_header = _extract_class(target_class_strings)
            for name in target_classes:
                target_classes_functions[name] = {}
                function_strings = re.split(function_pattern, target_classes[name])
                functions, header = _extract_functions(function_strings)
                target_classes_functions[name]['functions'] = functions
                target_classes_functions[name]['header'] = header
    else:
        target_classes = {}
        target_header = None
    with open(source_fn, 'r') as f:
        source_class_strings = re.split(class_pattern, f.read().strip())
        source_classes, source_header = _extract_class(source_class_strings, exclude_classes)
        for name in source_classes:
            source_classes_functions[name] = {}
            function_strings = re.split(function_pattern, source_classes[name])
            functions, header = _extract_functions(function_strings)
            source_classes_functions[name]['functions'] = functions
            source_classes_functions[name]['header'] = header

    for name in source_classes:
        if name in target_classes:
            target_classes_functions[name]['functions'] \
                .update(source_classes_functions[name]['functions'])
        else:
            target_classes_functions[name] = source_classes_functions[name]
    if not target_header:
        target_header = source_header
    target_code = replace_header(target_header, source_header)
    for name in target_classes_functions:
        function_string = '\n\n'.join(list(target_classes_functions[name]['functions'].values()))
        if function_string.strip():
            class_string = '\n'.join(target_classes_functions[name]['header']) + '\n\n' + function_string
        else:
            class_string = '\n'.join(target_classes_functions[name]['header'])
        target_code += '\n' + class_string + '\n\n'
    with open(target_fn, 'w') as f:
        f.write(target_code)

def is_first_char_space(txt):
    for s in txt:
        if s=='\n':
            continue
        elif s==' ':
            return True
        else:
            return False

def _extract_class(class_strings, exclude_classes=[]):
    classes = {}
    header = []
    pattern = r'class (.*)'
    class_strings = [c for c in class_strings if c.strip()]
    for s in class_strings:
        lines = s.strip().split('\n') 
        lines = [l for l in lines if l.strip()]
        first_line = lines[1] if lines[0].startswith('@dataclass') else lines[0]
        if first_line.startswith('class'):
            if '(' in first_line:
                first_line = first_line.split('(')[0]
            class_name = re.search(pattern, first_line).group(1)
            class_name = class_name.strip()
            if any([c == class_name for c in exclude_classes]):
                continue
            classes[class_name] = s.strip()
        else:
            header.append(s.strip())
    return classes, header

def _extract_functions(function_strings, exclude_functions=[]):
    header = []
    functions = {}
    pattern = r'def (.*)'
    for s in function_strings:
        lines = s.strip().split('\n')
        lines = [l.strip() for l in lines if l.strip()]
        for line in lines:
            if line.startswith('@'):
                continue
            else:
                first_line = line
                break
        if first_line.startswith('def'):
            if '(' in first_line:
                first_line = first_line.split('(')[0]
            function_name = re.search(pattern, first_line).group(1).strip()
            if any([f == function_name for f in exclude_functions]):
                continue
            functions[function_name] = s
        else:
            header.append(s)
    return functions, header

def _extract_import_code(code, pattern1, pattern2, excluede=None):
    if excluede is None:
        excluede = [
            'from src.ddd_objects',
            'from ddd_objects'
        ]
    try: 
        import_code = re.search(pattern1, code, re.DOTALL)
        if import_code:
            import_code = import_code.group(1).strip()
        else:
            import_code = re.search(pattern2, code).group(1).strip()
        if any([import_code.startswith(e) for e in excluede]):
            return None, code
        rest = code.replace(import_code, '')
        return import_code, rest
    except:
        return None, code

def extract_object_from_import_code(import_code):
    if import_code is None:
        return None, None
    import_code = import_code.strip()
    if '(' in import_code and ')' in import_code:
        header_pattern = r'(from .*\()'
        header = re.search(header_pattern, import_code).group(1)
        import_code = import_code[:-1]
        import_code = import_code.replace(header, '')
    else:
        header_pattern = r'(from .*import)'
        header = re.search(header_pattern, import_code).group(1)
        import_code = import_code.replace(header, '')
        header += '('
    objects = import_code.split(',')
    objects = [e.strip() for e in objects if e.strip()]
    return objects, header

def extract_import_entity_code(code):
    pattern1 = r'(from ((?!from).)*entity import \(((?!from).)*?\))'
    pattern2 = r'(from .*?entity import .*)'
    return _extract_import_code(code, pattern1, pattern2)

def extract_import_value_obj_code(code):
    pattern1 = r'(from ((?!from).)*value_obj import \(((?!from).)*?\))'
    pattern2 = r'(from .*?value_obj import .*)'
    return _extract_import_code(code, pattern1, pattern2)

def extract_import_converter_code(code):
    pattern1 = r'(from ((?!from).)*converter import \(((?!from).)*?\))'
    pattern2 = r'(from .*?converter import .*)'
    return _extract_import_code(code, pattern1, pattern2)

def extract_import_assembler_code(code):
    pattern1 = r'(from ((?!from).)*assembler import \(((?!from).)*?\))'
    pattern2 = r'(from .*?entity assembler .*)'
    return _extract_import_code(code, pattern1, pattern2)

def extract_import_repository_code(code):
    pattern1 = r'(from ((?!from).)*repository import \(((?!from).)*?\))'
    pattern2 = r'(from .*?repository import .*)'
    return _extract_import_code(code, pattern1, pattern2)

def extract_import_repository_impl_code(code):
    pattern1 = r'(from ((?!from).)*repository_impl import \(((?!from).)*?\))'
    pattern2 = r'(from .*?repository_impl import .*)'
    return _extract_import_code(code, pattern1, pattern2)

def extract_import_do_code(code):
    pattern1 = r'(from ((?!from).)*do import \(((?!from).)*?\))'
    pattern2 = r'(from .*?do import .*)'
    return _extract_import_code(code, pattern1, pattern2)

def extract_import_dto_code(code):
    pattern1 = r'(from ((?!from).)*dto import \(((?!from).)*?\))'
    pattern2 = r'(from .*?dto import .*)'
    return _extract_import_code(code, pattern1, pattern2)

def extract_converter_declarations(code:str):
    converters = []
    lines = code.strip().split('\n')
    rest = []
    for l in lines:
        if all(['converter' in l, '=' in l, 'Converter' in l]):
            converters.append(l)
        else:
            rest.append(l)
    rest = '\n'.join(rest)
    return converters, rest


def extract_def_header(code):
    try:
        pattern = r'(def.*?\):)'
        header = re.search(pattern, code, re.DOTALL)
        return header.group(1)
    except:
        return None

def extract_wrapped(decorated):
    if decorated.__closure__ is None:
        return decorated
    closure = (c.cell_contents for c in decorated.__closure__)
    return next((c for c in closure if isinstance(c, FunctionType)), None)