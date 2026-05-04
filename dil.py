import re

class DILSyntaxError(Exception):
    pass

def _set_path(env, path, value):
    keys = path.split(".")
    cur = env
    for k in keys[:-1]:
        if k not in cur:
            cur[k] = {}
        cur = cur[k]
    cur[keys[-1]] = value

def _get_path(env, path):
    keys = path.split(".")
    cur = env
    for k in keys:
        if k not in cur:
            raise Exception(f"Undefined variable: {path}")
        cur = cur[k]
    return cur

def parse_value(val):
    val = val.strip()
    if val.startswith('"') and val.endswith('"'):
        return val[1:-1]
    if val.isdigit():
        return int(val)
    if val.replace('.', '', 1).isdigit():
        return float(val)
    if val == "true":
        return True
    if val == "false":
        return False
    if val.startswith("[") and val.endswith("]"):
        items = val[1:-1].split(",")
        return [parse_value(x.strip()) for x in items]
    return val  # 変数参照として扱う

def run(path, env=None):
    if env is None:
        env = {}

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for lineno, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # 定義
        if "<" in line and not "<?" in line:
            key, val = line.split("<", 1)
            key = key.strip()
            val = val.strip()
            v = parse_value(val)
            if isinstance(v, str) and "." in v:
                v = _get_path(env, v)
            _set_path(env, key, v)

        # 出力
        elif ">" in line and not ">?" in line:
            src, dst = line.split(">", 1)
            src = src.strip()
            dst = dst.strip()
            val = parse_value(src)
            if isinstance(val, str) and "." in val:
                val = _get_path(env, val)
            _set_path(env, dst, val)

        else:
            raise DILSyntaxError(f"Line {lineno}: Unknown syntax")

    return env

def get(path, key=None):
    env = run(path, {})
    if key:
        return _get_path(env, key)
    return env
