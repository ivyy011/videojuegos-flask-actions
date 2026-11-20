\# Pruebas unitarias de la microaplicación de videojuegos



\## Descripción del proyecto



En esta actividad realicé pruebas unitarias de mi microaplicación de videojuegos desarrollada con Python y Flask. La aplicación utiliza SQLAlchemy como ORM, MySQL como base de datos y Flask-Login para la autenticación de usuarios. También integré una API REST para consultar y administrar videojuegos.



El objetivo fue comprobar que los modelos, las rutas protegidas y la API funcionaran correctamente.



\## Entorno de pruebas



Utilicé Python, Flask, unittest, MySQL, SQLAlchemy y las librerías pytest y pytest-flask.



Creé una base de datos independiente llamada `juegos\_test` para ejecutar las pruebas sin afectar los registros de mi base de datos original.



\## Cobertura de pruebas



\*\*Modelos (`test\_models.py`):\*\* Verifiqué que se pudiera crear y guardar correctamente un videojuego en la base de datos mediante `assertEqual()`.



\*\*Rutas (`test\_routes.py`):\*\* Comprobé que las rutas `/` y `/juegos` solicitaran autenticación y redirigieran al formulario de inicio de sesión cuando el usuario no estuviera autenticado.



\*\*API REST (`test\_api.py`):\*\* Comprobé que el endpoint `GET /api/juegos` devolviera una respuesta HTTP 200 y una lista de videojuegos en formato JSON.



\## Ejecución de pruebas



Para ejecutar las pruebas utilicé el siguiente comando:



`python -m unittest discover -v tests`



También guardé la salida completa de la ejecución en el archivo `results.txt`.



\## Resultados obtenidos



Se ejecutaron cuatro pruebas unitarias y todas finalizaron correctamente.



\- Pruebas de modelos: 1 aprobada.

\- Pruebas de rutas: 2 aprobadas.

\- Pruebas de API: 1 aprobada.

\- Total: 4 pruebas aprobadas, sin errores.



\## Retos encontrados y soluciones



Durante la actividad encontré algunos problemas de configuración, como la ausencia del entorno virtual, dependencias faltantes y variables de entorno no configuradas. Los solucioné creando el entorno virtual, instalando las librerías necesarias y configurando las variables correspondientes.



También tuve que integrar la API REST al proyecto de videojuegos con autenticación, ya que originalmente estaba desarrollada en otro proyecto.



Al ejecutar todas las pruebas juntas, encontré un error porque existían registros de pruebas anteriores en la base de datos. Lo solucioné limpiando los registros de videojuegos antes de realizar la prueba del modelo.



Finalmente, corregí un error de indentación en el archivo `test\_models.py` y logré ejecutar todas las pruebas satisfactoriamente.



\## Conclusión



Con esta actividad comprendí la importancia de las pruebas unitarias para verificar el funcionamiento de una aplicación. Aprendí a utilizar `setUp()`, `tearDown()` y diferentes aserciones de Python para comprobar los resultados esperados. Además, confirmé la utilidad de trabajar con una base de datos exclusiva para pruebas, evitando afectar la información original del proyecto.

