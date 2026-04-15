from pathlib import Path
import shutil


home_path = Path.home()
zshrc_file = home_path / ".zshrc"
backup_file = home_path / ".zshrc_backup"
current_dir = Path(__file__).resolve().parent
venv_path = current_dir / ".venv/bin/python"
alias = f'''
# added by notes cli app
alias notes="PYTHONPATH={current_dir} \\
{venv_path} -m src.app.main"

'''

if zshrc_file.exists():    
    shutil.copy2(zshrc_file, backup_file)
    lines = []
    with open(str(zshrc_file), "r") as file:
        lines = file.readlines()
        for i in range(len(lines)-1,-1,-1):
            if lines[i] == '\n':
                lines[i] = alias
                break
    with open(str(zshrc_file), "w") as file:
        file.writelines(lines)
else:
    print("Could not find the zshrc file")
