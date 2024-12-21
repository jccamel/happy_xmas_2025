import os
import subprocess
from datetime import datetime

# Cargar variables de entorno
git_user_name = os.getenv('GIT_USER_NAME')
git_user_email = os.getenv('GIT_USER_EMAIL')
repo_path = os.getenv('REPO_PATH')
access_token = os.getenv('ACCES_TOKEN') 

# Crear la URL remota con el Access Token de GitHub
access_token = os.getenv('ACCES_TOKEN')  # Obtiene el token del entorno
if not access_token:
    print("Error: El token GITHUB_TOKEN no está configurado. Verifica tus variables de entorno.")
    exit(1)

# Lista de fechas de commits
fechas_commits = [
    '2024-12-20', '2024-12-21', '2024-12-22',
    '2025-01-27', '2025-01-28', '2025-01-29', '2025-01-30', '2025-01-31', '2025-02-01', 
    '2025-02-05', '2025-02-12', '2025-02-17', '2025-02-18', '2025-02-19', '2025-02-20', 
    '2025-02-21', '2025-02-22', '2025-03-04', '2025-03-06', '2025-03-07', '2025-03-08', 
    '2025-03-11', '2025-03-13', '2025-03-15', '2025-03-18', '2025-03-20', '2025-03-22',
    '2025-03-25', '2025-03-26', '2025-03-27', '2025-03-28', '2025-03-29', '2025-04-07',
    '2025-04-08', '2025-04-09', '2025-04-10', '2025-04-11', '2025-04-12', '2025-04-14',
    '2025-04-17', '2025-04-21', '2025-04-24', '2025-04-28', '2025-04-29', '2025-04-30',
    '2025-05-01', '2025-05-12', '2025-05-13', '2025-05-14', '2025-05-15', '2025-05-16',
    '2025-05-17', '2025-05-19', '2025-05-22', '2025-05-26', '2025-05-29', '2025-06-02',
    '2025-06-03', '2025-06-04', '2025-06-05', '2025-06-16', '2025-06-17', '2025-06-18',
    '2025-06-19', '2025-06-21', '2025-06-26', '2025-06-28', '2025-07-03', '2025-07-05',
    '2025-07-07', '2025-07-08', '2025-07-09', '2025-07-10', '2025-07-11', '2025-07-12',
    '2025-07-28', '2025-07-29', '2025-07-31', '2025-08-01', '2025-08-02', '2025-08-04',
    '2025-08-05', '2025-08-06', '2025-08-07', '2025-08-08', '2025-08-09', '2025-08-13',
    '2025-08-18', '2025-08-19', '2025-08-20', '2025-08-21', '2025-08-22', '2025-08-23',
    '2025-08-25', '2025-08-26', '2025-08-28', '2025-08-29', '2025-08-30', '2025-09-09',
    '2025-09-10', '2025-09-11', '2025-09-12', '2025-09-13', '2025-09-17', '2025-09-24',
    '2025-09-25', '2025-09-26', '2025-09-27', '2025-10-01', '2025-10-08', '2025-10-09',
    '2025-10-10', '2025-10-11', '2025-10-21', '2025-10-23', '2025-10-24', '2025-10-25',
    '2025-10-28', '2025-10-30', '2025-11-01', '2025-11-04', '2025-11-06', '2025-11-08',
    '2025-11-11', '2025-11-12', '2025-11-13', '2025-11-14', '2025-11-15', '2025-11-25',
    '2025-11-26', '2025-11-27', '2025-11-29', '2025-12-02', '2025-12-04', '2025-12-06',
    '2025-12-09', '2025-12-11', '2025-12-13', '2025-12-16', '2025-12-18', '2025-12-19',
    '2025-12-20'
]

# Crear y configurar el repositorio local
os.makedirs(repo_path, exist_ok=True)
os.chdir(repo_path)
subprocess.run(["git", "init"], check=True)

# Configurar usuario de Git desde variables de entorno
subprocess.run(["git", "config", "user.name", git_user_name], check=True)
subprocess.run(["git", "config", "user.email", git_user_email], check=True)

# Asegurarse de que estamos en la rama 'main'
try:
    subprocess.run(["git", "checkout", "main"], check=True)  # Cambiar a 'main' si ya existe
except subprocess.CalledProcessError:
    subprocess.run(["git", "checkout", "-b", "main"], check=True)  # Crear 'main' si no existe

# Haz un commit inicial si la rama 'main' está vacía
try:
    subprocess.run(["git", "log"], check=True)  # Verificar si ya hay commits en 'main'
except subprocess.CalledProcessError:
    with open("actividad.txt", "w") as f:
        f.write("Commit inicial\n")
    subprocess.run(["git", "add", "actividad.txt"], check=True)
    subprocess.run(["git", "commit", "-m", "Commit inicial"], check=True)

# Función para realizar un commit
def hacer_commit(fecha, mensaje="Commit para Actividad"):
    os.environ["GIT_AUTHOR_DATE"] = fecha + " 00:00:00"
    os.environ["GIT_COMMITTER_DATE"] = fecha + " 00:00:00"
    with open("actividad.txt", "a") as f:
        f.write(f"Actividad en {fecha}\n")
    subprocess.run(["git", "add", "actividad.txt"], check=True)
    subprocess.run(["git", "commit", "-m", mensaje], check=True)

# Realizar commits en las fechas indicadas
hoy = datetime.now().strftime('%Y-%m-%d')
for fecha in fechas_commits:
    if fecha >= hoy:
        hacer_commit(fecha)

# Crear la URL remota con el Access Token de GitHub
url = f"https://{access_token}@github.com/{git_user_name}/{repo_path}.git"

# Configurar el repositorio remoto (si no está configurado)
try:
    subprocess.run(["git", "remote", "add", "origin", url], check=True)
except subprocess.CalledProcessError:
    print("El remoto ya está configurado. Continuando...")

# Actualizar la rama local antes de empujar
try:
    subprocess.run(["git", "pull", "origin", "main", "--rebase"], check=True)
except subprocess.CalledProcessError:
    print("No se pudieron integrar los cambios remotos. Continúa con precaución.")

# Intentar el push normal
try:
    subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
except subprocess.CalledProcessError:
    print("El push falló. Forzando el push...")
    try:
        subprocess.run(["git", "push", "-u", "origin", "main", "--force"], check=True)
    except subprocess.CalledProcessError:
        print("El push forzado falló. Verifica los logs.")

# Debugging adicional: Verificar el estado del repositorio
try:
    print("\n--- Estado del repositorio ---")
    subprocess.run(["git", "status"], check=True)
    print("\n--- Últimos commits ---")
    subprocess.run(["git", "log", "--oneline", "-5"], check=True)
    print("\n--- Configuración remota ---")
    subprocess.run(["git", "remote", "-v"], check=True)
except subprocess.CalledProcessError:
    print("Error al verificar el estado del repositorio.")
