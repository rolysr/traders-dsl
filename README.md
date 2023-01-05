# traders-dsl
## Autores:
- David Manuel García Aguilera (@dmga44) - C311
- Rolando Sánchez Ramos (@rolysr) - C311
- Andry Rosquet Rodríguez (@aXoXoR2) - C311

## Descripción general:
**Traders DSL** es un proyecto basado en el diseño de un lenguaje de dominio específico (**DSL** por sus siglas en inglés) que tiene como objetivo inicializar y ejecutar múltiples entornos con presencia de agentes y objetos de intercambio entre los mismos. Cada entorno es representado por un mundo con formato de una grilla rectangular, el cual será inicializado con una cantidad de filas y columnas determinada. En cada casilla de dicha matriz se podrán colocar los agentes negociadores. Los entornos también tendrán funcionalidades que permitirán añadir agentes y objetos en ciertas posiciones.

El lenguaje permite crear agentes negociadores, los cuales tendrán definidos una serie de objetos a vender y el precio al cual desea venderlos. Estos contarán también con un conjunto de objetos que prefieren consevar, es decir, que no estarán en venta. Además, los agentes podrán decidir si desean conservar un objeto previamente en estado de venta y viceversa.

Con el **DSL** propuesto es posible definir comportamientos de estos en un entornos. Dichos comportamientos son definidos de forma independiente y permiten estar encapsulados e identificados correctamente de tal forma que puedan ser reutilizados para la lógica de comportamiento de otros agentes. Los comportamientos de los agentes incluyen operaciones para moverse, detectar la presencia de objetos en su posición en la grilla, saber quiénes son los agentes cercanos con los cuáles es posible iniciar un proceso de negociación así como la capacidad de negociar o no con un agente dado.

El lenguaje propuesto será *Turing-Completo*, es decir, podrá ser usado para resolver cualquier problema tratable en lenguajes de propósito general, lo que en este caso utilizando una sintaxis mucho más expresiva y acotada. Será posible realizar operaciones de declaraciones de variables, tipado de variables (`number`, `bool`, `string`), expresiones de operaciones aritméticas y booleanas con estas, declaración de funciones (en este caso serían las funciones que expresan las acciones de los agentes) que pueden tener un comportamiento recursivo y control del flujo de código a partir de condicionales e implementación de ciclos.

## Requerimientos:
Este proyecto fue desarrollado utilizando el lenguaje de programación *Python* en su versión $3.9$. No es necesario instalar ninguna dependencia adicional si cuenta con la versión de Python mencionada. En última instancia se recomienda comprobar la correcta instalación de los paquetes mencionados en [requirements.txt]().

## Sintaxis del lenguaje y principales funcionalidades:
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

### Iteradores:
También es posible realizar iteraciones sobre algunos tipos específicos como por ejempos `list` y `book` utilizando la sentencia `foreach`. 

El tipo `list` funciona como una lista en *Python*, es decir, la misma se puede indexar mediante corchetes (`[]`), además, estas cuentan con funciones predefinidas como `push`, `pop`, `reverse` y `size`, las cuales permiten añadir un elemento al final de la lista, eliminar un elemento al inicio de esta, hallar el reverso y determinar la cantidad de elementos que contiene respectivamente.

El tipo `book` se asemeja al clásico tipo *diccionario* presenten en un gran número de lenguajes. Este permite representar con gran facilidad los elementos que un agente tiene a la venta y aquellos que desea conservar.
```
let arr: list = [1, 2, 3,];
foreach elem in arr {
    ...
}
```
Con el código anterior se logra recorrer una lista predefinida. Nótese la utilidad de esta funcionalidad para revisar el conjunto de agentes cercanos y objetos en el suelo dado el estado actual de un agente.

### Comportamientos:
Los comportamientos de los agente son declarados como funciones. La diferencia fundamente con las funciones convencionales es que estos no pueden ser ejecutados arbitrariamente en el código, para dicho caso, habría que asignarle dicho comportamiento a un agente, añadir a este a un entorno determinado y finalmente ejecutar el entorno. De esta forma cuando toque el turno de ejecución a dicho agente, este realizará todas las acciones predefinidas en su comportamiento.

Dado que los comportamientos tienen un identificador, esto permite crear múltiples agentes con un mismo comportamiento de forma sencilla, lo cual trae consigo aprovechar la reutilización de código. Además, dentro de un comportamiento se puede acceder a los campos definidos en un agente.

```
behave normal {
    move left;
    move down;

    talk "Hola Mundo";
}
```
Este código refleja el comportamiento de un agente que se mueve a la izquiera, luego hacia abajo y finalmente dice *Hola Mundo*. En este caso se muestran ejempos de acciones de un agente en un entorno. Dichas acciones permiten realizar todo el conjunto de operaciones posibles por un agente en el dominio modelado por este proyecto.

- #### Acciones de movimiento:
Las acciones de movimiento expresan la forma en que se debe desplazar un agente en un entorno.
```
move up;
move down;
move left;
move right;
move x,y;
```
Las cuatro primeras acciones mostradas permiten que el agente se mueva en cada una de las cuatro direcciones cardinales principales, mientras que la última de estas permite que el mismo pueda trasladarse instantáneamente a una posición determinada por dos coordenas del tablero separadas por coma (dichas coordenas deben ser expresiones o variables cuyo tipo final de evaluación sea un entero que represente el índice de una casilla del entorno donde se encuentra el agente)

- #### Comprar y vender objetos:
Para comprar objetos se cuentan con dos vías fundamentales:
```
buy agent1, "picadillo", 20;
buy agent1;
```
Con la primera opción se realiza una compra a un agente dado (para lo cual se ofrece un identificador del mismo), el nombre del producto a comprar (representado `string`) y la cantidad que se desea adquirir (representado por un `number`).

Otra de las acciones fundamentales que están relacionadas con el comercio es la venta, para ello un agente puede mover un objeto del conjunto de objetos a conservar hacia el conjunto de objetos en venta. La siguiente sintaxis permite este proceso:
```
sell "pan", 1, 20;
```
Con el código anterior, un agente decide mover una unidad de pan al conjunto de venta y ponerle un precio de $20$ unidades monetarias.

- #### Recoger y tirar objetos:
Las acciones de recoger y lanzar objetos al suelo permite lograr mayor flexibilidad en las acciones y sucesos que ocurren en un entorno. Es interesante lograr darle la capacidad a los agentes de poder buscar en la posición donde están, posibles objetos que puedan ser de su interés, por lo que se pueden programar entes que se dediquen solamente buscar un tipo específico de objeto. Además, la capcidad de colocar objetos en el suelo permite que algunos que no sea deseados por un agente en un momento dado, puedan formar parte de otro agente que lo encuentre en su recorrido por el entorno.

Para recoger objetos se utiliza el comando:
```
pick "zapato";
```
De esta forma el agente intenta coger un objeto llamado "zapato" en el suelo de su posición actual.

Por otro lado, para poner un objeto en el suelo, solo basta con hacer:
```
pick "zapato", 2;
```
Con lo cual un agente toma un objeto de nombre "zapato" y debe colocar en el suelo dos unidades del mismo. 

Es importante aclarar que los objetos que un agente lanza al suelo son desde el conjunto de objetos que este tenía pensado conservar. De forma análoga ocurre cuando se toma un objeto del suelo, este se agrega al conjunto de posesiones de interés, además de que se toman todas las unidades del mismo que se encuentren en el suelo.

- #### Posibles agentes para negociar y objetos en el suelo:
Para obtener los agentes con los que es posible negociar, se tienen en cuenta aquellos que estén en la misma posición en el entorno. Para encontrar nuevos agentes se utiliza el comando:
```
find peers;
```
Este comando devuelve una lista de los agentes que se encuentran disponibles para un posible intercambio de bienes.

Para obtener los objetos posibles a recoger del suelo se utiliza el comando:
```
find objects;
```
El cual devuelve un conjunto de los elementos localizados en la misma posición del agente que ejecuta dicha acción en un entorno dado.

### Entornos:
Los entornos representan los espacios acotados donde coexistirán un conjunto de agentes. Como ya se mecionó, estos están representados internamente por una grilla rectangular con dimensiones especificadas. A continuación se muestra