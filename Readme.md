# Synthetix Studio - Mini IDE

Este es el repositorio oficial de Synthetix Studio, un entorno de desarrollo minimalista que opera mediante consola de comandos (CLI) aplicando el patrón de diseño **Command Pattern**.


El desarrollo fue realizado estrictamente desde cero en Python mediante Programación Orientada a Objetos (POO).
- Implementada mediante una Lista Enlazada Doble personalizada.
-  Se crearon Pilas (Stacks) manuales para el control de cambios (Undo/Redo) y la verificación de balanceo de paréntesis y llaves.
- Las peticiones de la API de Inteligencia Artificial para refactorización se envían primero a una Cola FIFO personalizada para evitar la saturación.
- Los diagnósticos se procesan utilizando algoritmos construidos desde cero (Mergesort y Shellsort).

1. Instalar Python 3.8+
2. Clonar este repositorio mediante una de las ramas (branches) principales.
3. Ejecutar en consola: `python main.py`
4. Dentro de la terminal, usar comandos como:
   - `config config.json`
   - `new main.cpp`
   - `check`