import sys
import subprocess
import shutil
from pathlib import Path

def main():
    output_dir = Path("docs")
    if output_dir.exists():
        print(f"🧹 Limpiando directorio '{output_dir}'...")
        shutil.rmtree(output_dir)

    cmd = [
        sys.executable, "-m", "pdoc",
        "app", "config.py",
        "-o", str(output_dir),
        "--docformat", "google"
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("Error al generar la documentación")

if __name__ == "__main__":
    main()
