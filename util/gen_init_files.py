import os


def main():
    SPECIAL_DIRS = [
        'login_server/handlers',
        'login_server/packets',
        'world_server/handlers',
        'world_server/packets',
        'world_server/systems',
    ]

    # Go through each submodule in these modules and generate a __init__.py file.
    for special_dir in SPECIAL_DIRS:
        init_file_lines = []
        module_base = special_dir.replace('/', '.')
        for filename in os.listdir(special_dir):
            if filename.endswith('.py') and filename != '__init__.py':
                module = os.path.splitext(filename)[0]
                init_file_lines.append(f'import {module_base}.{module}')

        init_file_lines.sort()
        with open(os.path.join(special_dir, '__init__.py'), 'w') as f:
            f.write('\n'.join(['## AUTO-GENEATED USING gen_init_files.py'] + init_file_lines))
            f.write('\n')


if __name__ == '__main__':
    main()
