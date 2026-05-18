*This project has been created as part of the 42 curriculum by lbonnet*

# Fly-in 🛩️

<span style="color:turquoise">

## 📝 Description
</span>

The main objective of this project is to move a given number of drones from a starting area to  
a goal. It seems easy at first glance, but there is a lot of constraints to take into accounts...

Between start and end, the drones may go through different zones and connections with different  
behaviors. Some zones are blocked, which means no drone can access it, some others are restricted  
or have priority, so drones respectively takes two turns to get there or should prioritize access  
to this area over another. And of course, all drones must reach the end in a minimal number of turns !

Given all this information, the main challenge of the project is to create an algorithm capable  
of managing the routes of all the drones, respecting the capacity of the zones over the course of  
the flights and avoiding collisions. All this from a "simple" text file...

<span style="color:turquoise">

## 🖥️ Instructions
</span>

This project has a Makefile, allowing you to use different rules serving different purposes:

-> **make install:**
    install the project with all its needed dependencies using uv

-> **make debug:**
    run the main script in debug mode using Python’s built-in debugger

-> **make clean:**
    remove temporary files or caches to keep the project environment clean

-> **make lint:**
    execute flake8 and mypy with mandatory flags

-> **make lint-strict:**
    execute flake8 and mypy -- strict

-> **make run:**
    execute the main script of the project

    ⚠️ To run the program, execute 'make run path-to-input-file' from the  
    root directory.

    The input file follows strict rules. To avoid parsing errors, you may  
    respect the constraints detailed in the next section.

<span style="color:lightblue">

### ⤵️ Input
</span>

The input file corresponds to an entire map in the form of a .txt file. It may contain zones,  
connections between them, comments and the number of drones to process, all of this following  
a well-defined structure:

Each line is treated independently, comments must start with '#' and are ignored.  
The first line of the file must define the number of drones using 'nb_drones: positive int'.

More details on zones and connections below :

#### Zones attributes

A zone has the following attributes:
- **Type** (start_hub, hub, end_hub)
- **Name** (a string, dashes and spaces forbidden)
- **Coordinates** x y (two integers separated by a space)
- **Optional metadata**, between brackets, that may contain:
    - color as a single word (default set to white)
    - zone being either normal, blocked, restricted or priority (default set to normal)
    - max_drones as a positive integer

    Expected format: *type: name x y [metadata1=string, ...]*  
    Any difference in the format will raise an error during parsing.

#### Connections attributes

A connection has the following attributes:
- **Always** starts with connection
- **Shows** which zones it is connecting
- **Optional metadata**, between brackets, that may contain:
    - max_link_capacity as a positive integer

    Expected format: *connection: zone1-zone2 [metadata=string, ...]*  
    Any difference in the format will raise an error during parsing.

<span style="color:lightblue">

### ⤴️ Output
</span>

This project has two types of 'output':

**1- The logs file:**

This file contains, for each turn, a line showing all the drones that moved during this turn.

Example : 'Turn 3: D1-maze_trap_a2 D2-maze_trap_a1 D3-gate_hell1'

We see here that during turn 3, drone D1 moved to 'maze_trap_a2', drone D2 moved to  
'maze_trap_a1' and drone D3 moved to 'gate_hell1'  

These informations will also be displayed on our second 'output':

**2- The visualizer:**

Built with Pygame, the visualizer displays the whole map with zones and connections, following  
the data from the input files, and processes all the drones through it, from start to end.  
We will return to this in more detail later (cf. *Additional sections*).

<span style="color:turquoise">

## 📚 Resources
</span>

Some articles, references and tutorials I used during the elaboration of this project:

- https://fr.wikipedia.org/wiki/Algorithme_de_Dijkstra :  
A well-documented page explaining how a Dijkstra works, how it was invented, as well as  
multiple variants and comparisons.

- https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm :  
This may seem redundant with the previous one, and it is in a certain proportion, but it  
also adds a lot of documentation on the subject the first was not providing.

- https://zestedesavoir.com/tutoriels/846/pygame-pour-les-zesteurs/ :  
A very complete Pygame tutorial, in french. It helped me a lotfr my first steps in Pygame.

- https://www.pygame.org/docs/ :  
Litteraly everything you need to know on Pygame : classes, methods, usage... everything !

- http://pygametutorials.wikidot.com/tutorials-two :  
Once again, a very nice tutorial, in english this time, that complements the other one.

AI was used mainly for learning purposes and to improve my understanding of what I read before  
if needed. I also used it one time to find an issue I couldn't find myself in my algorithm, and  
regretted it as it took 2 days before I finally managed to find it...


<span style="color:turquoise">

## 🚀 Additional sections
</span>

### -> Algorithm explanation

As we've seen, our algorithm has to take into acccount a lot of parameters. My algorithm is what  
we could call a *Dijkstra space-time*, as it is managing both available space and time.

**The global idea is quite simple and can be broken down into several stages:**

**1)** The first drone looks for the shortest path from his position (start) to the end:
- For each neighboring zone, it gets the cost (in turns) needed to access it
- The area with the lowest access cost is given priority and stored in a queue, building the  
path step by step.
- We then repeat these steps until a complete path from start to end is found

**2)** Once we have the path for the first drone, all the zones he occupies at each turn are stored in  
a dict 'global_state'.

**3)** We then repeat step 1, for the second drone. However this time, we'll look, for each zone he  
tries to access, if this zone is available or occupied by a previous drone at the given turn with our  
'global_state'. If the zone is occupied and at full capacity when our second drone wants to access it,  
it can't enter it and therefore has to count the wait time as the cost, or choose another zone.

**4)** Each time a drone finds his path, we update the 'global_state' with its position for each turn.

**5)** These steps are repeated until all drones found or failed to find a way to the end.

### -> Visual reprsentation

The visualizer is a graphical interpretation of the result produced by the algorithm. I chose to create  
mine with Pygame rather than on the terminal.

At launch, a pygame window opens and displays all the zones with their connections. All drones are set  
at start. Then, based on the paths we got from the algorithm, each drone moves, turn by turn, until  
every one of them reaches the end.

During execution, you can hold or press several keys, each performing an action:

|Key|Type|Effect|
|---|---|---|
|f|Press or Hold|Increases animation speed|
|s|Press or Hold|Reduces animation speed|
|p|Press|Pauses or plays the animation|
|r|Press|Reloads the animation from the beginning|
|c|Press|Displays real-time occupancy of every connection|
|z|Press|Displays real-time occupancy of every zone|
|h|Press|Hides every activated occupancy display|
|esc|Press|Closes the window & ends animation|

With this tool, the user can clearly see what is happening, where and when each drone is moving in  
real-time, in a playful and enjoyable way.

<!-- Je dois, pour un projet python, realiser un algorithme permettant a un nombre donne de drones de partir d'une zone 'start' pour arriver a une zone 'end', en passant par de multiples autres zones, le tout en depensant le moins de tours possible. Plusieurs parametres sont a prendre en compte :

- Chaque zone a des coordonnees fixes x et y,
- Chaque zone est liee a une autre par au moins une connexion,
- Chaque deplacement d'un drone vers une zone prend 1 tour,
- Certaines zones sont 'restreintes', le deplacement vers celles-ci prend donc deux tours,
- Les zones ont une capacite maximale : certaines ne peuvent accueillir qu'un drone a la fois, d'autres plus de 1,
- Les connexions ont aussi une capacite maximale,
- Un drone ne peut donc pas entrer dans une zone dont la capacite maximale est deja atteinte,
- Un drone peut attendre sur sa zone actuelle si necessaire.

Pour resoudre ce probleme, je pensais utiliser un algorithme Dijkstra avec prioritized planning, mais cela necessite evidemment l'ecriture d'un dijkstra, que je ne vois pas comment structurer. Peux-tu me donner une structure pour le dijkstra a integrer, puis une pour son integration au sein du graphe espace-temps ? -->
