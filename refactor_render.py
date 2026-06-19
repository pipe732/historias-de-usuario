import os
import ast
import argparse

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    try:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=SyntaxWarning)
            tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        return 0, 0, [] # Could not parse

    total_renders = 0
    renders_with_dict = 0
    lines_with_dict = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Return) and isinstance(node.value, ast.Call):
            func = node.value.func
            if isinstance(func, ast.Name) and func.id == 'render':
                total_renders += 1
                
                # Context is usually the 3rd positional argument
                has_dict_context = False
                
                if len(node.value.args) >= 3:
                    if isinstance(node.value.args[2], ast.Dict):
                        has_dict_context = True
                
                # Or it could be a keyword argument `context=...`
                for kw in node.value.keywords:
                    if kw.arg == 'context' and isinstance(kw.value, ast.Dict):
                        has_dict_context = True

                if has_dict_context:
                    renders_with_dict += 1
                    lines_with_dict.append(node.lineno)

    return total_renders, renders_with_dict, lines_with_dict

def main():
    parser = argparse.ArgumentParser(description="Analiza archivos para detectar 'return render' usando diccionarios directos.")
    parser.add_argument('directory', nargs='?', default='.', help="Directorio a escanear (por defecto: actual)")
    args = parser.parse_args()

    total_files_scanned = 0
    total_renders_found = 0
    total_with_dict = 0

    print(f"Escanendo el directorio: {os.path.abspath(args.directory)}")
    print("-" * 50)

    for root, dirs, files in os.walk(args.directory):
        # Exclude common non-project directories
        dirs[:] = [d for d in dirs if d not in ('venv', '.venv', 'env', '__pycache__', '.git', 'migrations')]
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                total_files_scanned += 1
                renders, with_dict, lines = process_file(filepath)
                if renders > 0:
                    total_renders_found += renders
                    total_with_dict += with_dict
                    if with_dict > 0:
                        line_str = ", ".join(map(str, lines))
                        print(f"[ALERTA] {filepath}: Tiene {with_dict} render(s) en las líneas [{line_str}].")
                    else:
                        print(f"[OK]     {filepath}: {renders} render(s) correctos.")

    print("-" * 50)
    print("REPORTE FINAL (SOLO LECTURA):")
    print(f"Archivos Python escaneados    : {total_files_scanned}")
    print(f"Total de 'return render'      : {total_renders_found}")
    print(f"Renders usando diccionario    : {total_with_dict}")
    print(f"Renders correctos (variable)  : {total_renders_found - total_with_dict}")

if __name__ == "__main__":
    main()
