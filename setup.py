"""
Script de configuración inicial para Vinted Scraper
Instala dependencias y configura el entorno
"""

import subprocess
import sys
import os
from pathlib import Path


def print_header(text):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def check_python_version():
    """Verifica la versión de Python"""
    print_header("Verificando versión de Python")

    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        return False

    print("✓ Versión de Python correcta")
    return True


def create_virtual_environment():
    """Crea un entorno virtual"""
    print_header("Creando entorno virtual")

    venv_path = Path("venv")

    if venv_path.exists():
        print("⚠️  El entorno virtual ya existe")
        respuesta = input("¿Deseas recrearlo? (s/n): ")
        if respuesta.lower() != 's':
            print("✓ Usando entorno virtual existente")
            return True

        print("Eliminando entorno virtual existente...")
        import shutil
        shutil.rmtree(venv_path)

    try:
        print("Creando entorno virtual...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✓ Entorno virtual creado")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error creando entorno virtual")
        return False


def get_pip_command():
    """Obtiene el comando pip según el sistema operativo"""
    if sys.platform == "win32":
        return str(Path("venv/Scripts/pip.exe"))
    else:
        return str(Path("venv/bin/pip"))


def install_dependencies():
    """Instala las dependencias del proyecto"""
    print_header("Instalando dependencias")

    pip_cmd = get_pip_command()

    try:
        print("Actualizando pip...")
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)

        print("\nInstalando dependencias del proyecto...")
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)

        print("✓ Dependencias instaladas")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error instalando dependencias")
        return False


def install_playwright():
    """Instala los navegadores de Playwright"""
    print_header("Instalando navegadores de Playwright")

    pip_cmd = get_pip_command()

    try:
        # Obtener el comando playwright
        if sys.platform == "win32":
            playwright_cmd = str(Path("venv/Scripts/playwright.exe"))
        else:
            playwright_cmd = str(Path("venv/bin/playwright"))

        print("Instalando navegador Chromium...")
        subprocess.run([playwright_cmd, "install", "chromium"], check=True)

        print("✓ Navegadores instalados")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error instalando navegadores")
        print("💡 Intenta ejecutar manualmente: playwright install chromium")
        return False
    except FileNotFoundError:
        print("❌ Comando playwright no encontrado")
        print("💡 Intenta ejecutar manualmente: playwright install chromium")
        return False


def create_data_directory():
    """Crea el directorio de datos"""
    print_header("Creando directorios")

    directories = ["data", "static"]

    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True)
            print(f"✓ Directorio '{directory}/' creado")
        else:
            print(f"⚠️  Directorio '{directory}/' ya existe")

    return True


def print_instructions():
    """Imprime instrucciones finales"""
    print_header("¡Instalación completada!")

    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"

    print("Para usar el scraper:\n")
    print(f"1. Activa el entorno virtual:")
    print(f"   {activate_cmd}\n")
    print("2. Opción A - Usar la interfaz web:")
    print("   python app.py")
    print("   Luego visita: http://localhost:5000\n")
    print("3. Opción B - Ejecutar el scraper directamente:")
    print("   python scraper.py\n")
    print("4. Opción C - Ver ejemplos de uso:")
    print("   python example_usage.py\n")
    print("Para más información, consulta el README.md")
    print("="*60 + "\n")


def main():
    """Función principal"""
    print("\n" + "🛍️ "*20)
    print("   VINTED SCRAPER - INSTALACIÓN Y CONFIGURACIÓN")
    print("🛍️ "*20 + "\n")

    # Verificar Python
    if not check_python_version():
        sys.exit(1)

    # Preguntar qué hacer
    print("\n¿Qué deseas hacer?")
    print("1. Instalación completa (recomendado)")
    print("2. Solo instalar dependencias")
    print("3. Solo instalar navegadores Playwright")
    print("0. Cancelar")

    opcion = input("\nSelecciona una opción: ")

    if opcion == "0":
        print("\n👋 Instalación cancelada")
        return

    if opcion == "1":
        # Instalación completa
        steps = [
            ("Entorno virtual", create_virtual_environment),
            ("Dependencias", install_dependencies),
            ("Navegadores Playwright", install_playwright),
            ("Directorios", create_data_directory)
        ]

        for step_name, step_func in steps:
            if not step_func():
                print(f"\n❌ Error en paso: {step_name}")
                print("💡 Intenta ejecutar los pasos manualmente")
                sys.exit(1)

        print_instructions()

    elif opcion == "2":
        if not create_virtual_environment():
            sys.exit(1)
        if not install_dependencies():
            sys.exit(1)
        print("\n✓ Dependencias instaladas")

    elif opcion == "3":
        if not install_playwright():
            sys.exit(1)
        print("\n✓ Navegadores instalados")

    else:
        print("\n❌ Opción inválida")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Instalación interrumpida")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
