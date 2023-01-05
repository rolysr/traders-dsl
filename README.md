# traders-dsl
**Traders DSL** es un proyecto basado en el diseño de un lenguaje de dominio específico (**DSL** por sus siglas en inglés) que tiene como objetivo inicializar y ejecutar múltiples entornos con presencia de agentes y objetos de intercambio entre los mismos. Cada entorno es representado por un mundo con formato de una grilla rectangular, el cual será inicializado con una cantidad de filas y columnas determinada. En cada casilla de dicha matriz se podrán colocar los agentes negociadores. Los entornos también tendrán funcionalidades que permitirán añadir agentes y objetos en ciertas posiciones.

El lenguaje permite crear agentes negociadores, los cuales tendrán definidos una serie de objetos a vender y el precio al cual desea venderlos. Estos contarán también con un conjunto de objetos que prefieren consevar, es decir, que no estarán en venta. Además, los agentes podrán decidir si desean conservar un objeto previamente en estado de venta y viceversa.

Con el **DSL** propuesto es posible definir comportamientos de estos en un entornos. Dichos comportamientos son definidos de forma independiente y permiten estar encapsulados e identificados correctamente de tal forma que puedan ser reutilizados para la lógica de comportamiento de otros agentes. Los comportamientos de los agentes incluyen operaciones para moverse, detectar la presencia de objetos en su posición en la grilla, saber quiénes son los agentes cercanos con los cuáles es posible iniciar un proceso de negociación así como la capacidad de negociar o no con un agente dado.

El lenguaje propuesto será *Turing-Completo*, es decir, podrá ser usado para resolver cualquier problema tratable en lenguajes de propósito general, lo que en este caso utilizando una sintaxis mucho más expresiva y acotada. Será posible realizar operaciones de declaraciones de variables, tipado de variables (`int`, `float`, `string`), expresiones de operaciones aritméticas y booleanas con estas, declaración de funciones (en este caso serían las funciones que expresan las acciones de los agentes) que pueden tener un comportamiento recursivo y control del flujo de código a partir de condicionales e implementación de ciclos.

## Requerimientos:
Este proyecto fue desarrollado utilizando el lenguaje de programación *Python* en su versión $3.9$. No es necesario instalar ninguna dependencia adicional si cuenta con la versión de Python mencionada. En última instancia se recomienda comprobar la correcta instalación de los paquetes mencionados en [requirements.txt]().



