# Practica_2
En el archivo practica2_prpa.py se inicializa el monitor con varias funciones:
  - __init__(self): Se inicializan el semáforo y las variables: coches norte, coches sur y peatones en el puente. Así como unas variables para los coches y peatones que están esperando para entrar al puente y otra "turno" para controlar quien entra cada vez. Además se establece una variable codición para cada elemento (coches norte, coches sur y peatones).
  - are_no_carsnorth(self),are_no_carssouth(self), are_no_peds(self): Indican si hay o no coches norte, coches sur y peatones respectivamente en el puente.
  - wants_enter_car(self, direction: int), wants_enter_pedestrian(self):  Sirven para que los coches y los peatones puedan acceder al puente correctamente, según sus turnos.
  - leaves_car(self, direction: int), leaves_pedestrian(self):  Sirven para controlar la salida del puente de los coches y los peatones.
  - gen_pedestrian(monitor: Monitor), gen_cars(direction: int, time_cars, monitor: Monitor): Generan los peatones y coches norte y sur.

En el archivo practica2_inanicion_prpa.py se muestra el mismo programa que en practica2_prpa.py pero sin utilizar la variable turno y las variables para los coches y peatones que están esperando, por lo que sin tener una variable para regular los turnos ni variables para saber qué elementos están esperando para entrar al puente no se puede controlar el acceso ordenado a este. No funciona.

Por último, en el archivo Práctica 2 PRPA Helena Ferrero.pdf, se contesta a las preguntas que se pedían en la práctica.
