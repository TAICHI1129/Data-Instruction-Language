import re

class DILSyntaxError(Exception):
    pass

def tokenize(line):
    return line.strip()

def parse_value(val, env):
    val = val.strip()

    if val.startswith('"') and val.endswith('"'):
        return val[1:-1]

    if re.match(r'^-?\d+$', val):
        return int(val)

    if re.match(r'^-?\d+\.\d+$', val):
        return float(val)

    if val == "true":
        return True
    if val == "false":
        return False

    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        if not inner:
            return []
        return [parse_value(x.strip(), env) for x in inner.split(",")]

    if val.startswith("{") and val.endswith("}"):
        obj = {}
        inner = val[1:-1].strip()
        if inner:
            pairs = inner.split(",")
            for p in pairs:
                k, v = p.split(":", 1)
                obj[k.strip()] = parse_value(v.strip(), env)
        return obj

    return get_path(env, val)

def set_path(env, path, value):
    keys = path.split(".")
    cur = env
    for k in keys[:-1]:
        cur = cur.setdefault(k, {})
    cur[keys[-1]] = value

def get_path(env, path):
    keys = path.split(".")
    cur = env
    for k in keys:
        if k not in cur:
            raise Exception(f"Undefined variable: {path}")
        cur = cur[k]
    return cur

def eval_cond(cond, env):
    if "<?" in cond:
        a, b = cond.split("<?")
        return parse_value(a, env) < parse_value(b, env)
    if ">?" in cond:
        a, b = cond.split(">?")
        return parse_value(a, env) > parse_value(b, env)
    if "=?" in cond:
        a, b = cond.split("=?")
        return parse_value(a, env) == parse_value(b, env)
    raise DILSyntaxError(f"Invalid condition: {cond}")

def run(path, env=None):
    if env is None:
        env = {}

    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.split("#")[0].strip()
        i += 1

        if not line:
            continue

        if line.startswith("if"):
            cond = line[2:].strip().rstrip("{").strip()
            block = []
            depth = 1

            while i < len(lines):
                l = lines[i]
                i += 1
                if "{" in l:
                    depth += 1
                if "}" in l:
                    depth -= 1
                    if depth == 0:
                        break
                block.append(l)

            if eval_cond(cond, env):
                run_block(block, env)
            continue

        if "<" in line and "<?" not in line:
            k, v = line.split("<", 1)
            set_path(env, k.strip(), parse_value(v.strip(), env))
            continue

        if ">" in line and ">?" not in line:
            s, d = line.split(">", 1)
            set_path(env, d.strip(), parse_value(s.strip(), env))
            continue

        raise DILSyntaxError(f"Syntax error: {raw.strip()}")

    return env

def run_block(lines, env):
    for raw in lines:
        line = raw.split("#")[0].strip()
        if not line:
            continue

        if "<" in line and "<?" not in line:
            k, v = line.split("<", 1)
            set_path(env, k.strip(), parse_value(v.strip(), env))

        elif ">" in line and ">?" not in line:
            s, d = line.split(">", 1)
            set_path(env, d.strip(), parse_value(s.strip(), env))

def get(path, key=None):
    env = run(path, {})
    if key:
        return get_path(env, key)
    return env
