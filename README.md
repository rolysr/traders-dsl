# traders-dsl
**Traders DSL** es un proyecto basado en el diseño de un lenguaje de dominio específico (**DSL** por sus siglas en inglés) que tiene como objetivo inicializar y ejecutar múltiples entornos con presencia de agentes y objetos de intercambio entre los mismos. Cada entorno es representado por un mundo con formato de una grilla rectangular, el cual será inicializado con una cantidad de filas y columnas determinada. En cada casilla de dicha matriz se podrán colocar los agentes negociadores. Los entornos también tendrán funcionalidades que permitirán añadir agentes y objetos en ciertas posiciones.

El lenguaje permite crear agentes negociadores, los cuales tendrán definidos una serie de objetos a vender y el precio al cual desea venderlos. Estos contarán también con un conjunto de objetos que prefieren consevar, es decir, que no estarán en venta. Además, los agentes podrán decidir si desean conservar un objeto previamente en estado de venta y viceversa.

Con el **DSL** propuesto es posible definir comportamientos de estos en un entornos. Dichos comportamientos son definidos de forma independiente y permiten estar encapsulados e identificados correctamente de tal forma que puedan ser reutilizados para la lógica de comportamiento de otros agentes. Los comportamientos de los agentes incluyen operaciones para moverse, detectar la presencia de objetos en su posición en la grilla, saber quiénes son los agentes cercanos con los cuáles es posible iniciar un proceso de negociación así como la capacidad de negociar o no con un agente dado.

El lenguaje propuesto será *Turing-Completo*, es decir, podrá ser usado para resolver cualquier problema tratable en lenguajes de propósito general, lo que en este caso utilizando una sintaxis mucho más expresiva y acotada. Será posible realizar operaciones de declaraciones de variables, tipado de variables (`number`, `bool`, `string`), expresiones de operaciones aritméticas y booleanas con estas, declaración de funciones (en este caso serían las funciones que expresan las acciones de los agentes) que pueden tener un comportamiento recursivo y control del flujo de código a partir de condicionales e implementación de ciclos.

## Requerimientos:
Este proyecto fue desarrollado utilizando el lenguaje de programación *Python* en su versión $3.9$. No es necesario instalar ninguna dependencia adicional si cuenta con la versión de Python mencionada. En última instancia se recomienda comprobar la correcta instalación de los paquetes mencionados en [requirements.txt]().

## Sintaxis del lenguaje:
La sintaxis del **DSL** propuesto se caracteriza por lograr un balance entre un estilo declarativo y uno imperativo a la hora de expresar las posibles intrucciones válidas en el mismo, lo cual permite una mayor expresividad.

### Declaración e inicialización de variables:
El lenguaje **Traders** es estáticamente tipado, por lo que, toda declaración de variable o tipo predefinido debe ser correctamente especificado.
```
let x: number;
let n: number = 5;
let b: bool = true;
let s: string = "Hola Mundo";
let arr: list = [1, 2, 3,];
let bk: book = { "tomate" : (10, 10,)};
```
Con dichos tipos predefinidos es posible representar una serie de parámetros en el momento de inicializar un agente o entorno determinado. Solo basta especificar el nombre, el tipo y delante colocar la palabra reservada `let`. 

### Condicionales:
Las condicionales son una forma de controlar el flujo del código en el **DSL**. Estas solo pueden ser declaradas dentro de una función de comportamiento de un agente ya que solo tiene sentido realizar las acciones más relevantes del lenguaje a partir de la ejecución de un entorno con la presencia de agentes con distintos comportamientos predefinidos.
```
let a: number = 2;
in case a < 2 {
    ...
}
in other case a > 2 {
    ...
}
otherwise {
    ...
}
```
El funcionamiento de las condicionales es análogo a como ocurre en muchos lenguajes de programación con las sentencias `if`, `else if` y `else`.

### Ciclos:
Los ciclos en el lenguaje propuesto son expresados con una idea parecida a la utilizada en las sentencias `while`. Su uso es exclusivo de los ámbitos definidos por las funciones de comportamiento de agentes.
```
let a: number = 2;
repeat when a > 0 {
    a = a - 1;
}
```
En el segmento de anterior se muestra un ejemplo de un ciclo que se repite mientras la variable `a` sea positiva.
