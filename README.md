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
Este proyecto fue desarrollado utilizando el lenguaje de programación *Python* en su versión $3.9$. No es necesario instalar ninguna dependencia adicional si cuenta con la versión de Python mencionada. En última instancia se recomienda comprobar la correcta instalación de los paquetes mencionados en [requirements.txt](https://github.com/rolysr/traders-dsl/blob/main/requirements.txt).

## Ejecución del proyecto:
Para ejecutar un archivo de código, nótese que es necesario crea un fichero con terminación *.traders*. Luego localice dicho fichero obteniéndo su dirección de localización en su *PC*.

Por ejemplo, sea el archivo `strong_test.traders` en la carpeta `examples` del proyecto. Para poder ejecutar bastaría con hacer en una consola con *Python* habilitado:

```
$ python main.py ./examples/strong_test.traders
```
Finalmente se ejecutará el archivo con el resultado esperado.

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

 - Recursividad:

 Es posible diseñar métodos recursivos a partir de las sentencias `stop` y `restart behave`. La primera es equivalente a la clásica sentencia `return` en varios lenguajes de programación y la segunda permite que el agente pueda reiniciar su lógica de funcionamiento teniendo en cuenta el valor de las variables que posee actualmente.

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

### Agentes:
Los agentes son un tipo que representan a los entes que participarán en las simulaciones de un entorno específico. Estos son inicializados directamente un con identificador y un conjunto de parámetros principales:
```
behave b1 {
    move left;
    move down;

    talk "Hola Mundo";
}

agent a1 {
    location = [2,0,];
    let atrr : string = "Pedro";
    let atrr2 : string = "Jose";
    let abc : number;
    behavior = b1;
    on_keep = {"carne" : (5, ), "mondongo" : (99999999, ),};
    on_sale = {"carne" : (5, 100, ), "mondongo" : (99999999, 1000, ), };
    let extra_attr: list = dim2;
}
```
Con este código estamos inicializando un agente denominado *a1*, que al añadirse a un entorno este será colocado en la posición *(2, 0)*. Este cuenta con los atributos adicionales (otra de las capacidades de un agente) *attr*, *attr2* y *abc*. Tiene un comportamiento definido denominado *b1* y posee los conjuntos *on_keep* y *on_sale* (son considerados los conjuntos destinados a tener seguimiento de los objetos a conservar y a vender respectivamente). El conjunto *on_keep* relaciona al nombre de un objeto con la cantidad del mismo mientras que *on_sale* lo relaciones con una cantidad y un precio de venta.

### Entornos:
Los entornos representan los espacios acotados donde coexistirán un conjunto de agentes. Como ya se mecionó, estos están representados internamente por una grilla rectangular con dimensiones especificadas. A continuación se muestra una forma de inicializar un entorno:
```
env la_tinta{
    agents = [Pepito, Juan, Pepito, ];
    log = true;
    rows = 5;
    columns = 5;
}
```
En este caso estamos inicializando un entorno denominado *la_tinta*, que posee unos agentes denominados *Pepito* (dos instancias de *Pepito*) y *Juan* (nótese que la repetición del nombre *Pepito* demuestra la capacidad de reutilizar tipos de agentes ya definidos). El campo *log* denota si se desean imprimir el historial de sucesos que ocurren en el ambiente.

Para trabajar con un entorno se dispone de un conjunto de operaciones fundamentales:

- Ejecutar el entorno:

Para la ejecución del entorno se utiliza la siguiente sintaxis:
```
run e1 with 5 iterations;
```
Con lo cual estamos haciendo que un entorno denominado *e1* ejecute cinco iteraciones, lo cual es recorrer cinco veces el conjunto de agentes del mismo y por cada uno ejecutar su comportamiento predefinido.

- Reiniciar el entorno:

```
reset e1;
```
Con este código logramos que un entorno vuelva al estado inicial que tenía justo antes de la primera iteración.

## Gramática:
La gramática implementada fue diseñada con el objetivo de ser parseable de la mejor manera posible por un *paser* **LALR(1)**.

```
Rule 0     S' -> program
Rule 1     program -> declarationList
Rule 2     declarationList -> empty
Rule 3     declarationList -> declaration declarationList
Rule 4     declaration -> envFunc
Rule 5     declaration -> varAssign
Rule 6     declaration -> varDecl
Rule 7     declaration -> behaveDecl
Rule 8     declaration -> agentDecl
Rule 9     declaration -> envDecl
Rule 10    envDecl -> ENV ID { envBody }
Rule 11    agentDecl -> AGENT ID { agentBody }
Rule 12    behaveDecl -> BEHAVE ID { behaveBody }
Rule 13    varDecl -> LET ID : type ASSIGN expr SEP
Rule 14    varDecl -> LET ID : type SEP
Rule 15    varAssign -> getter ASSIGN expr SEP
Rule 16    envFunc -> PUT expr IN ID AT expr , expr SEP
Rule 17    envFunc -> RUN ID WITH expr ITERATIONS SEP
Rule 18    envFunc -> RESET ID SEP
Rule 19    envBody -> varList
Rule 20    agentBody -> varList
Rule 21    behaveBody -> statementList
Rule 22    varList -> empty
Rule 23    varList -> varAssign varList
Rule 24    varList -> varDecl varList
Rule 25    statementList -> empty
Rule 26    statementList -> statement statementList
Rule 27    statement -> primFuncStmt
Rule 28    statement -> incaseStmt
Rule 29    statement -> foreachStmt
Rule 30    statement -> repeatStmt
Rule 31    statement -> varAssign
Rule 32    statement -> varDecl
Rule 33    statement -> expr SEP
Rule 34    repeatStmt -> REPEAT WHEN expr { statementList }
Rule 35    foreachStmt -> FOREACH ID IN expr { statementList }
Rule 36    incaseStmt -> IN CASE expr { statementList } inothercaseStmt
Rule 37    inothercaseStmt -> empty
Rule 38    inothercaseStmt -> OTHERWISE { statementList }
Rule 39    inothercaseStmt -> IN OTHER CASE expr { statementList } inothercaseStmt
Rule 40    primFuncStmt -> PUT expr , expr SEP
Rule 41    primFuncStmt -> PICK expr SEP
Rule 42    primFuncStmt -> STOP SEP
Rule 43    primFuncStmt -> RESTART BEHAVE SEP
Rule 44    primFuncStmt -> SELL expr , expr , expr SEP
Rule 45    primFuncStmt -> buyStmt SEP
Rule 46    primFuncStmt -> moveStmt SEP
Rule 47    primFuncStmt -> TALK expr SEP
Rule 48    moveStmt -> MOVE RIGHT
Rule 49    moveStmt -> MOVE LEFT
Rule 50    moveStmt -> MOVE DOWN
Rule 51    moveStmt -> MOVE UP
Rule 52    moveStmt -> MOVE expr , expr
Rule 53    buyStmt -> BUY expr
Rule 54    buyStmt -> BUY expr , expr , expr
Rule 55    expr -> call
Rule 56    expr -> - expr  [precedence=right, level=9]
Rule 57    expr -> ! expr  [precedence=right, level=10]
Rule 58    expr -> expr / expr  [precedence=left, level=8]
Rule 59    expr -> expr * expr  [precedence=left, level=8]
Rule 60    expr -> expr - expr  [precedence=left, level=7]
Rule 61    expr -> expr + expr  [precedence=left, level=7]
Rule 62    expr -> expr GREATER expr  [precedence=left, level=5]
Rule 63    expr -> expr GREATEREQ expr  [precedence=left, level=5]
Rule 64    expr -> expr LESSEQ expr  [precedence=left, level=5]
Rule 65    expr -> expr LESS expr  [precedence=left, level=5]
Rule 66    expr -> expr EQEQ expr  [precedence=left, level=4]
Rule 67    expr -> expr NOTEQ expr  [precedence=left, level=4]
Rule 68    expr -> expr AND expr  [precedence=left, level=3]
Rule 69    expr -> expr OR expr  [precedence=left, level=2]
Rule 70    call -> ID dotTail
Rule 71    call -> primitiveValue
Rule 72    call -> primary
Rule 73    getter -> ID dotTail
Rule 74    dotTail -> empty
Rule 75    dotTail -> [ expr ] dotTail
Rule 76    dotTail -> . idTail dotTail
Rule 77    idTail -> listFunc
Rule 78    idTail -> ID
Rule 79    listFunc -> REVERSE
Rule 80    listFunc -> POP
Rule 81    listFunc -> PUSH expr
Rule 82    listFunc -> SIZE
Rule 83    primitiveValue -> FIND PEERS
Rule 84    primitiveValue -> FIND OBJECTS
Rule 85    primitiveValue -> RANDOM FROM expr TO expr
Rule 86    primary -> ( expr )
Rule 87    primary -> { bookItems }
Rule 88    primary -> [ listItems ]
Rule 89    primary -> STRING
Rule 90    primary -> NUMBER
Rule 91    primary -> FALSE
Rule 92    primary -> TRUE
Rule 93    listItems -> empty
Rule 94    listItems -> expr , listItems
Rule 95    bookItems -> empty
Rule 96    bookItems -> STRING : ( listItems ) , bookItems
Rule 97    type -> BOOK_TYPE
Rule 98    type -> LIST_TYPE
Rule 99    type -> STRING_TYPE
Rule 100   type -> BOOL_TYPE
Rule 101   type -> NUMBER_TYPE
Rule 102   empty -> <empty>
```

## Arquitectura del proyecto:
El proyecto está dividido en tres módulos fundamentales: `backend`, `sly` y `src`. Las implementaciones realizadas en `src` dependen de aquellas contenidas en `backend` y `sly`. El punto de entrada a la aplicación del proyecto lo denota el archivo *main.py*, que cuenta con la funcionalidad básica para ejecutar el compilador del **DSL** ya que importa las principales herramientas del proyecto implementadas en `src`.

### Módulo `backend`:
Este módulo contiene las implementaciones de los tipos básico utilizados para el proyecto. Dentro del mismo tenemos:
- `TradersAgent`:
    Representa un agente del entorno y es el encargado de contener los campos y métodos principales a ejecutar por el tipo `agent`.

- `Number`, `String`, `Bool`: 
    Representaciones de los tipos `number` (representado de forma interna como flotantes, trata siempre de parsear cualquier dato numérico de esta forma), `string` y `bool`.

- `Behavior`: 
    Contiene las especificaciones fundamentales para la ejecución de métodos. Esta clase recibe un identificador (nombre del comportamiento) una lista de sentencias a ejecutar (instrucciones del lenguaje a ejecutar).

- `List`, `Book`: 
    Implementaciones de los tipos `list` y `book`, los cuales son manejados internamente como listas y diccionarios de *Python* respectivamente.

- `TradersEnvironment`: 
    Representación de los entornos del **DSL**.

- `Env`: 
    Clase utilizada para manejar el contexto de los procesos ejecutados en el lenguaje. Internamente contiene un diccionario que representa el espacio de nombres definidos en un archivo de código. Contiene el método `find(...)`, el cual permite comprobar la presencia o no de un determinado identificador en el espacio de nombres definido.

### Módulo `sly`:
Este módulo se encarga de contener las implementaciones de los objetos encargados de realizar el análisis lexicográfico y los procesos de *parsing*. 

Para la primera de estas tareas se cuenta con la clase `Lexer`, la cual contiene una implementación báscia de un *lexer* que recibe un conjunto de tokens principales, y logra identificar a estos en una cadena cualquiera del lenguaje. En el caso de la segunda tarea se cuenta con la clase `Parser`, el cual es un *parser* de tipo **LALR(1)**.

Este módulo fue tomado de una [biblioteca](https://github.com/dabeaz/sly) que contiene ya implementada dichos algoritmos de *lexing* y *parsing*.

### Módulo `src`:
Es el módulo principal del proyecto y el mismo fue implementado desde cero. Contiene tres principales clases que componen la base de funcionamiento del proyecto: `TradersLexer`, ``TradersParser` y `TradersInterpreter`.

- `TradersLexer`: 
    Hereda de la clase `Lexer` del módulo `sly`. Contiene las especificaciones de los token y palabras resevadas principales del proyecto. Contiene el método `tokenize(...)` encargado de identificar y separar los *tokens* del lenguaje.

- `TradersParser`:
    Hereda de la clase `Parser` del módulo `sly`. Contiene la gramática del lenguaje y genera el autómata **LALR(1)** utilizado durante el proceso de *parsing*.

- `TradersInterpreter`:
    Contituye el intérprete del lenguaje. Permite la ejecución de cada uno de los procesos y funcionalidades del proyecto, además de que realiza todos los análisis semánticos principales (chequeo y consistencia de tipos).
