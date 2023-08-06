from inspect import getsource, isfunction
import os, re, json
from dataclasses import dataclass, _MISSING_TYPE
from typing import Any, List, Optional, Union
from .lib import extract_def_header, extract_wrapped


def var_to_value_type(do_name):
    upper_list = ['id']
    parts = do_name.split('_')
    parts = [p.upper() if p in upper_list else p for p in parts ]
    parts = [p.capitalize() if not p.isupper() else p for p in parts]
    return ''.join(parts)

def value_type_to_var(value_type):
    var = ''
    for s in value_type:
        if s.isupper():
            var += '_'+s.lower()
        else:
            var += s.lower()
    if var[0]=='_':
        var = var[1:]
    return var

@dataclass
class Item:
    name: str
    item_type: str
    entity_type: str
    value_type: str
    default_value: int
    value_default_value: str
    entity_default_value: str
    required: bool
    life_time: int = None

@dataclass
class RepositoryFunctionArgument:
    name: str
    is_entity: bool = True
    arg_type: Optional[str] = None
    default: Any = None
    is_list: bool = False
    is_optional: bool = False
    converter: Optional[str] = None
    value_type: Optional[str] = None

    def __post_init__(self):
        if not isinstance(self.is_entity, bool):
            raise ValueError('Invaild argument type of is_entity')
        if self.arg_type is None:
            self.arg_type = var_to_value_type(self.name)
        self.value_type = self.arg_type
        if self.is_list:
            self.arg_type = f'List[{self.arg_type}]'
        if self.is_optional:
            self.arg_type = f'Optional[{self.arg_type}]'
        if self.is_entity and self.converter is None:
            self.converter = f'{value_type_to_var(self.value_type)}_converter'
        assert self.converter is None or isinstance(self.converter, str)

def _extract_args_from_def_header(func_name, header):
    header = header.strip()[:-1]
    line = header.replace(f'def {func_name}', '') \
            .replace('(', '').replace(')', '').replace('\n', '')
    args = [arg.strip() for arg in line.split(',')]
    arg_tuples = []
    for arg in args:
        arg_name = None
        arg_type = None
        default_value = None
        is_list = False
        is_optional = False
        if ':' in arg:
            arg_name, arg = arg.split(':')
            arg_name, arg = arg_name.strip(), arg.strip()
        if '=' in arg:
            if arg_name is None:
                arg_name, default_value = arg.split('=')
                arg_name, default_value = arg_name.strip(), default_value.strip()
            else:
                arg_type, default_value = arg.split('=')
                arg_type, default_value = arg_type.strip(), default_value.strip()
        if arg_name is None:
            arg_name = arg.strip()
        if arg_type is not None and 'Optional' in arg_type:
            is_optional = True
        if arg_type is not None and 'List' in arg_type:
            is_list = True
        arg_tuples.append((arg_name, default_value, is_list, is_optional))
    return arg_tuples

def _extract_ret_from_code(code):
    lines = code.strip().split('\n')
    is_list = False
    for line in lines:
        line = line.strip()
        if line.startswith('return') and '[' in line :
            is_list = True
            break
    return is_list


def extract_repo_info_from_ao(ao_cls, exclude=[], custom_optimize=True):
    # exclude is a ban set with elements in the format (func_name, [arg_name, ...]), * is wildcard
    cls_funcs_str = [o for o in dir(ao_cls) 
        if not o.startswith('_') and isfunction(getattr(ao_cls, o))]
    func_info = {}
    banned_arg_for_all_func = []
    for _banned_func, _banned_arg in exclude:
        if "*"==_banned_func:
            if isinstance(_banned_arg, str):
                banned_arg_for_all_func.append(_banned_arg)
            else:
                banned_arg_for_all_func.extend(_banned_arg)
    for func_str in cls_funcs_str:
        is_func_banned = False
        is_arg_banned = False
        banned_arg = []
        for _banned_func, _banned_arg in exclude:
            if func_str==_banned_func:
                is_func_banned = True
                if banned_arg=='*':
                    is_arg_banned = True
                elif isinstance(banned_arg, str):
                    banned_arg.append(_banned_arg)
                else:
                    banned_arg.extend(_banned_arg)
                break
        if is_func_banned and is_arg_banned:
            continue

        func_info[func_str] = {}
        args_info = []
        func = getattr(ao_cls, func_str)
        code = getsource(extract_wrapped(func))
        def_header = extract_def_header(code)
        arg_tuples = _extract_args_from_def_header(func_str, def_header)
        arg_names = []
        for arg_tuple in arg_tuples:
            arg_name, default_value, is_list, is_optional = arg_tuple
            if (is_func_banned and arg_name in banned_arg) or arg_name in banned_arg_for_all_func:
                continue
            if arg_name == 'self':
                continue
            arg_type = None
            is_entity = True
            if custom_optimize:
                if arg_name[-1]=='s':
                    arg_type = var_to_value_type(arg_name[:-1])
                    is_list = True
                if 'name' in arg_name:
                    arg_type = 'Name'
                    is_entity = False
                if 'path' in arg_name:
                    arg_type = 'Path'
                    is_entity = False
            if default_value is None and not is_list and not is_optional \
                and is_entity and arg_type is None:
                element = arg_name
            elif default_value is None and not is_list and not is_optional and arg_type is None:
                element = (arg_name, False)
            elif not is_list and not is_optional:
                element = (arg_name, is_entity, arg_type, default_value)
            elif not is_optional:
                element = (arg_name, is_entity, arg_type, default_value, True)
            else:
                element = (arg_name, is_entity, arg_type, default_value, True, True)
            args_info.append(element)
            arg_names.append(arg_name)

        func_info[func_str]['args'] = args_info
        ret_is_list = _extract_ret_from_code(code)
        arg_name = 'your_ret'
        func_info[func_str]['ret'] = (
            arg_name, True, None, None, ret_is_list, True)
        if custom_optimize and func_str.startswith('get'):
            arg_names = [f'{{{n}}}' for n in arg_names]
            parts = func_str.split('_')[1:]
            obj = '_'.join(parts)
            func_info[func_str]['key'] = ':'.join(arg_names)+f':{obj}'
    return func_info

def save_repo_info(ao_classes, save_dir, save_name='repo_info_temp.json', exclude=[], indent=4):
    save_fn = os.path.join(save_dir, save_name )
    repo_info = {}
    for cls in ao_classes:
        repo_info[cls.__name__] = extract_repo_info_from_ao(cls, exclude)
    json_str = '{\n'
    for class_name in repo_info:
        json_str += ' '*indent+f'"{class_name}":{{\n'
        for method_name in repo_info[class_name]:
            json_str += ' '*indent*2+f'"{method_name}":{{\n'
            json_str += ' '*indent*3+f'"args":'
            json_str += json.dumps(repo_info[class_name][method_name]['args'])
            json_str += f',\n'
            json_str += ' '*indent*3+f'"ret":'
            json_str += json.dumps(repo_info[class_name][method_name]['ret'])
            json_str += f'\n'
            if 'key' in repo_info[class_name][method_name]:
                json_str = json_str[:-1]+',\n'
                json_str += ' '*indent*3+f'"key":'
                json_str += json.dumps(repo_info[class_name][method_name]['key'])
                json_str += f'\n'
            json_str += ' '*indent*2+'},\n'
        json_str = json_str[:-2]
        json_str += '\n'
        json_str += ' '*indent+f'}},'
    json_str = json_str[:-1]
    json_str += '\n}'
    print(json_str)
    with open(save_fn, 'w') as f:
        f.write(json_str)


@dataclass
class RepositoryMethod:
    name: str
    args: List[RepositoryFunctionArgument]
    ret: Optional[RepositoryFunctionArgument]
    key: str

@dataclass
class RepositoryInfo:
    name: str
    methods: List[RepositoryMethod]

def extract_repo_info(repo_info):
    def _load_arg(arg):
        if isinstance(arg, str):
            return RepositoryFunctionArgument(arg)
        elif isinstance(arg, RepositoryFunctionArgument):
            return arg
        elif isinstance(arg, tuple) or isinstance(arg, list):
            if len(arg)==1:
                return RepositoryFunctionArgument(arg[0])
            elif len(arg)==2:
                return RepositoryFunctionArgument(arg[0], arg[1])
            elif len(arg)==3:
                return RepositoryFunctionArgument(arg[0], arg[1], arg[2])
            elif len(arg)==4:
                return RepositoryFunctionArgument(arg[0], arg[1], arg[2], arg[3])
            elif len(arg)==5:
                return RepositoryFunctionArgument(arg[0], arg[1], arg[2], arg[3], arg[4])
            elif len(arg)==6:
                return RepositoryFunctionArgument(arg[0], arg[1], arg[2], 
                arg[3], arg[4], arg[5])
            elif len(arg)==7:
                return RepositoryFunctionArgument(arg[0], arg[1], arg[2], 
                arg[3], arg[4], arg[5], arg[6])
            else:
                raise ValueError(f'Wrong number({len(arg)}) of arguments')
        else:
            raise ValueError(f'Wrong type of args: {type(arg)}')

    repositories = []
    for repo_name in repo_info:
        methods = []
        key = None
        repo_dict = repo_info[repo_name]
        for met_name in repo_dict:
            met_dict = repo_dict[met_name]
            args = []
            for arg in met_dict['args']:
                args.append(_load_arg(arg))                
            if 'ret' in met_dict and met_dict['ret'] is not None:
                ret = met_dict['ret']
                ret = _load_arg(ret)
            else:
                ret = None
            if 'key' in met_dict:
                key = met_dict['key']
            else:
                key = None
            method = RepositoryMethod(met_name, args, ret, key)
            methods.append(method)
        repository = RepositoryInfo(repo_name, methods)
        repositories.append(repository)
    return repositories


def extract_item(cls):
    class_vars = cls.__annotations__
    class_fields = cls.__dataclass_fields__
    pattern = r'List\[(.*)\]'
    items = []
    for key in class_fields:
        item_type = class_vars[key].__name__  \
            if hasattr(class_vars[key], '__name__') else str(class_vars[key]) \
            .replace('__main__.', '').replace('typing.', '')

        value_type = class_fields[key].default[0]  \
            if isinstance(class_fields[key].default, tuple) else class_fields[key].default \
            if not isinstance(class_fields[key].default, _MISSING_TYPE) else var_to_value_type(key)
        if 'List' in value_type:
            value_type =  re.search(pattern, value_type).group(1)
        if 'List' in item_type:
            entity_type = f'List[{value_type}]'
        else:
            entity_type = value_type
        if 'Optional' in item_type:
            entity_type = f'Optional[{entity_type}]'

        default_value = class_fields[key].default[1] \
            if isinstance(class_fields[key].default, tuple) and len(class_fields[key].default)>1 \
            else None

        if isinstance(class_fields[key].default, tuple) and len(class_fields[key].default)>1:
            required = False
        else:
            required = True

        if default_value is None:
            value_default_value = None
            entity_default_value = None

        elif 'List' in entity_type:
            assert isinstance(default_value, list), f"default value of {key} should be list"
            value_default_value = [f"'{v}'" if isinstance(v, str) else str(v) for v in default_value]
            entity_default_value = [f"{value_type}({v})" for v in value_default_value]
            value_default_value = f"[{','.join(value_default_value)}]"
            entity_default_value = f"[{','.join(entity_default_value)}]"
        else:
            value_default_value = f"'{default_value}'" \
                if isinstance(default_value, str) else default_value
            entity_default_value = f"{value_type}('{default_value}')" \
                if isinstance(default_value, str) else f"{value_type}({default_value})"
        life_time = class_fields[key].default[2] \
            if isinstance(class_fields[key].default, tuple) and len(class_fields[key].default)>2 \
            else None
        items.append(Item(
            key, 
            item_type, 
            entity_type, 
            value_type, 
            default_value, 
            value_default_value, 
            entity_default_value,
            required,
            life_time
        ))
 
    return items
    

if __name__ == '__main__':
    @dataclass
    class Template:
        attr0: str
        attr1: str = ('Number', 1, 1)
        attr2: List[str] = (None, 'a', 1)
        attr3: Optional[str] = 'String'
        attr4: Optional[List[str]] = 'Number'
    items = extract_item(Template)
    print(items)
