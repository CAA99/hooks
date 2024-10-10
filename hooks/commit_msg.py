#!/usr/bin/env python3
import sys
import re

def main():
    commit_msg = sys.argv[1]
    with open(commit_msg, 'r') as f:
        commit_msg = f.read()
    
    if commit_msg.lower().startswith("merge"):
        print("Commit de merge detectado, se omite la validación de formato.")
        sys.exit(0)  
    
    # Separa el título y la descripción usando el primer salto de línea
    title, *description = commit_msg.splitlines()
    description = '\n'.join(description).strip()
    commit = ['add','feat','fix','docs','style','refactor','test','chore']
    
    # Define la expresión regular para el formato
    regex = r'^[0-9]+ (add|feat|fix|docs|style|refactor|test|chore): .{10,50}$'

    # Validar el título
    if not re.match(regex, title):
        print(f'''
        ❌ ERROR! El mensaje de commit debe tener la siguiente estructura:
        <#HU> <tipo:{commit}>: <titulo>
        Ejemplo ✅: 123 feat: Agregar nueva funcionalidad
        El commit actual es: {title}
        ''')
        sys.exit(1)

    print("El mensaje de commit cumple con el formato ✅.")

if __name__ == '__main__':
    main()
