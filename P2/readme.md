README
  Readme del grupo 3 de la asignatura de videojuegos para la segunda práctica
  que trata el trabajo de la cámara, rotaciones y geometría básica con OpenGL en
  Javascript

AUTHORS
  Alexandre Zheng - 776093
  Alonso del Rincón - 783252
  Antonio Gallén - 735184
  Juan Plo - 795105

CHANGELOG (y decisiones de diseño)
  - 20 cubos rotan aleatoriamente respecto al centro, con velocidades, órbitas y
  colores diferentes (salvo que el azar quiera repetidos)
  - Con las flechas del teclado se puede desplazar la cámara en el plano X-Z
  (el plano horizontal según la cámara), con una velocidad ajustable desde el
  fichero en "camSpeed"
  - Con el ratón se puede girar la cámara hacia cualquier dirección, se ha
  decidido que es más orientativo poder girarla 360º en el eje horizontal y solo
  180º en el vertical (conservando el sentido de arriba y abajo)
  - Se puede intercambiar la proyección por ortogonal pulsando la tecla 'O', y
  se puede volver a la proyección perspectiva con la tecla 'P'
  - En la proyección ortogonal se ha optado por permitir ajustar la escala de la
  proyección con las teclas arriba y abajo para permitir "acercarse" y
  "alejarse" del conjunto renderizado
  - Con las teclas '+' y '-' se puede ajustar el field of view en la proyección
  perspectiva. Para evitar confusiones se puede utilizar tanto las teclas del
  NumPad como las del teclado central para esta funcionalidad

DESCRIPTION
  -VID_practica02_Grupo03.zip/
  |-src_practica_02/
  ||-practica_02_base.html
  ||-practica_02_base.js
  |-Common/
  ||-math.js (la biblioteca adicional para el cálculo de raices cuadradas)
  |-readme.md (este fichero)

INSTALL
  Se requiere de una biblioteca adicional, ya especificada en el .html, dentro
  de la carpeta Commons junto con el resto de bibliotecas otorgadas. Esta solo
  se ha incluido para evitar el algoritmo de una raíz cuadrada (utilizada para
  calcular el módulo de un vector)

BUGS
  A veces crashea el navegador si se minimiza o si permanece mucho tiempo activo

CONTRIBUTING
  Alexandre Zheng:    y horas
  Alonso del Rincón:  z horas
  Antonio Gallén:     11.5 horas
  Juan Plo:           w horas
  Total:              11.5 + X horas
