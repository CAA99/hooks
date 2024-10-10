# Instalación de Hooks

Los hooks de Git utilizados en este proyecto se encuentran en la carpeta `hooks`. Para instalarlos, ejecuta el siguiente script en la raíz del proyecto:

```bash
./install_hooks.sh
```

Este script configurará los hooks en el directorio `.git/hooks/`, lo que permitirá que se ejecuten automáticamente en los momentos correspondientes. 

---

# Git Hooks

Este repositorio utiliza dos hooks de Git personalizados para garantizar que los mensajes de commit y las ramas cumplan con los estándares establecidos. A continuación, se describe el propósito de cada hook y cómo funcionan.

## Hooks Implementados

### 1. Hook `commit-msg`

Este hook se asegura de que el mensaje del commit siga un formato específico antes de permitir que el commit se complete. El formato requerido para los mensajes de commit es el siguiente:

```
<#HU> <tipo>: <título>
```

#### Reglas de Validación:
- El mensaje debe comenzar con un número de ticket (`#HU`) seguido de un espacio y el tipo de commit.
- Los tipos permitidos son: `add`, `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
- El título debe tener entre 10 y 50 caracteres.
- Los commits de tipo "merge" son exentos de validación.

#### Ejemplo de Mensaje Correcto:
```
123 feat: Agregar nueva funcionalidad
```

#### Ejemplo de Uso:
1. Al intentar realizar un commit, el hook validará automáticamente el mensaje.
2. Si el mensaje no cumple con el formato, el commit se cancelará y mostrará un mensaje de error.
3. Si el mensaje es válido, el commit se completará con éxito.

#### Código del Hook `commit-msg`
```python
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
```

### 2. Hook `pre-push`

Este hook asegura que solo se permita hacer `push` a ramas específicas, siguiendo una convención de nombres. 

#### Convenciones Permitidas para las Ramas:
- Las ramas que comiencen con `feature/`.
- Las ramas que comiencen con `hotfix/`.
- La rama `dev`.

#### Ejemplo de Uso:
1. Al intentar hacer `push`, el hook validará el nombre de la rama de destino.
2. Si el nombre de la rama no coincide con las convenciones permitidas, se cancelará el `push` y se mostrará un mensaje de error.
3. Si el nombre de la rama es válido, el `push` procederá normalmente.

#### Código del Hook `pre-push`
```bash
#!/bin/bash

# Leer las referencias que se están pusheando
while read local_ref local_sha remote_ref remote_sha; do
    # Extraer el nombre completo de la rama
    branch_name=$(echo "$remote_ref" | sed 's|refs/heads/||')

    # Verificar si el nombre de la rama empieza con los prefijos permitidos
    if [[ "$branch_name" != feature/* && "$branch_name" != hotfix/* && "$branch_name" != dev ]]; then
        echo "Error: Solo puedes hacer push a ramas que comiencen con 'feature/', 'hotfix/' o a la rama 'dev'."
        exit 1
    fi
done

exit 0
```

---

## Tipos de Hooks en Git

### 1. **Hooks del Lado del Cliente**

Los hooks del lado del cliente se ejecutan en el momento en que ocurren operaciones locales en el repositorio. Algunos de estos hooks también permiten interceptar operaciones de Git antes de que se comuniquen con el servidor remoto.

- **`pre-commit`**: Se ejecuta antes de que se realice el commit. Suele usarse para verificar el código (como linting), ejecutar pruebas unitarias, o formatear archivos.

- **`prepare-commit-msg`**: Se ejecuta después de que se crea el archivo de mensaje de commit, pero antes de que se muestre al usuario. Permite modificar el mensaje de commit predefinido. Se usa generalmente para agregar información adicional de manera automática.

- **`commit-msg`**: Se ejecuta justo después de que se introduce el mensaje de commit. Valida el formato del mensaje de commit para asegurar que cumpla con las convenciones establecidas. *Este hook ya está implementado en tu repositorio.*

- **`post-commit`**: Se ejecuta después de que se completa un commit. Puedes usarlo para enviar notificaciones, actualizar logs locales, o activar otras tareas que deban suceder tras un commit.

- **`pre-rebase`**: Se ejecuta antes de que un rebase comience. Es útil para prevenir el rebase de ciertas ramas, o para realizar acciones de validación antes de un rebase.

- **`post-checkout`**: Se ejecuta después de un cambio de rama (`checkout`). Puede usarse para realizar tareas de configuración de entorno o actualizar archivos específicos según la rama.

- **`post-merge`**: Se ejecuta después de un merge exitoso. Es útil para acciones de limpieza o tareas de configuración, como restablecer permisos de archivos o compilar el proyecto.

- **`pre-push`**: Se ejecuta antes de enviar cambios a un repositorio remoto con `push`. Permite validar las ramas o realizar otras comprobaciones antes de sincronizarse con el servidor. *Este hook también ya está implementado en tu repositorio.*

- **`pre-applypatch`**: Se ejecuta antes de que se aplique un parche con el comando `git am`. Puede usarse para verificar el contenido del parche antes de aplicarlo.

- **`post-applypatch`**: Se ejecuta después de que se aplica un parche con `git am`. Se utiliza para notificaciones o tareas relacionadas tras la aplicación de un parche.

### 2. **Hooks del Lado del Servidor**

Los hooks del lado del servidor se ejecutan en el repositorio remoto y sirven principalmente para gestionar operaciones de sincronización y mantener integridad en el servidor.

- **`pre-receive`**: Se ejecuta cuando el servidor recibe un `push`, pero antes de actualizar las referencias. Puede usarse para validar los cambios entrantes, como verificar políticas de commit o acceso.

- **`update`**: Similar al `pre-receive`, pero se ejecuta una vez por cada referencia a actualizarse. Es útil para aplicar validaciones específicas en cada rama o etiqueta.

- **`post-receive`**: Se ejecuta después de que el servidor ha recibido un `push` y ha actualizado las referencias. Suele utilizarse para desplegar código, enviar notificaciones o actualizar servicios relacionados.

- **`post-update`**: Se ejecuta después de que el servidor ha recibido un `push` y ha actualizado todas las referencias. Es similar a `post-receive`, pero es más útil para realizar tareas que involucran las referencias actualizadas.

