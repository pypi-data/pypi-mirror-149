from os.path import join, abspath, dirname

import subprocess

if __name__ == '__main__':
    root = abspath(join(dirname(__file__), '..'))
    src_dir = join(root, 'protocol')
    dst_dir = join(root, 'patchwork/core')
    subprocess.run(["protoc", f"-I={src_dir}", f"--python_out={dst_dir}", join(src_dir, "task.proto")])
