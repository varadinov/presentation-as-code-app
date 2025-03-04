
import os
import shutil
import uuid
import re

from utils.command import run_command


def generate_presentation(content: str, template_dir: str = "slidev_template"):
    unique_id = str(uuid.uuid4())
    dist_path = os.path.join("presentations", unique_id)
    os.makedirs(dist_path, exist_ok=True)
    shutil.copytree(template_dir, dist_path, dirs_exist_ok=True)
    slides_path = os.path.join(dist_path, "slides.md")

    with open(slides_path, "w", encoding="utf-8") as file:
        file.write(content)

    run_command(['npm', 'install'], dist_path)
    run_command(['npm', 'run', 'build', '--', '--base', f'/{unique_id}/dist'], dist_path)

    return unique_id


def find_presentations(root_directory: str = "presentations"):
    for dirpath, _, filenames in os.walk(root_directory):
        if 'slides.md' in filenames:
            slides_path = os.path.join(dirpath, 'slides.md')
            with open(slides_path, 'r', encoding='utf-8') as file:
                content = file.read()
                match = re.search(r'^title:\s*(.+)', content, re.MULTILINE)
                if match:
                    title = match.group(1).strip()
                    yield { "directory": os.path.basename(dirpath), "title": title }
    