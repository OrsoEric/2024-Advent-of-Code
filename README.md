# B-AROL-O/aoc-2024

The scope of this project is to practice python and algorithms and build useful classes

Originally https://github.com/B-AROL-O/aoc-2024/tree/dev-orso

PALS:
https://github.com/AB-Normals/advent-of-code-2024
https://github.com/davmacario/aoc

# Map of Symbols

Very useful class that I used a lot
Loads a map from file

- DAY16 - LABIRINTH
used it to load, create, access, manipulate
even convert from string to int for coloring


## DAY17 - HACK HASH
part 2 swas insanely difficult
It's a 16 dimensional to 16 dimensional octal hash function

at first I tried a genetic algorithm. It got me to a 14/16 digit partial match

then I augmented it with spot brute search, it got me to 15/16 digit partial match

[4, 6, 7, 6, 3, 1, 5, 6, 0, 4, 0, 6, 5, 4, 0, 1, 0]
[2, 4, 1, 2, 7, 5, 4, 7, 1, 3, 5, 5, 0, 4, 3, 0]
[2, 4, 1, 2, 7, 5, 4, 7, 1, 3, 5, 5, 0, 3, 3, 0] < DESIRED

[4, 6, 7, 6, 3, 1, 5, 6, 0, 4, 0, 6, 4, 0, 5, 1, 0]
[2, 4, 1, 2, 7, 5, 4, 7, 1, 3, 5, 5, 0, 3, 4, 0]
[2, 4, 1, 2, 7, 5, 4, 7, 1, 3, 5, 5, 0, 3, 3, 0] < DESIRED

I tried really hard, but nothing I tried could make it converge
I found out that it's best if I:
1) conver the hash to octal
2) reverse the input string
3) match the input string from the right to the left
Still couldn't do it with genetics...

So I Mounted a Tree search
starting off it went poorly

I  noticed the tendency that up to 4 to 5 digit to the left can still influence the digit
This has implications for the local minima

So I upgraded the fitness
the fitness counts:
10 points for the index the rightmost digit matched
1 point for matching one digit (irregardless of position)
1 point penalty for each time a node has been visited

Then I implemented two rolls to move the tree cursor up

It's clear I go down whenever I get a better fitness
BUT if the fitness is worse, I have a roll
If the roll is better then how much worse the fitness is, I can still go down
This balances the tendency of exploration

I have a fitness rule that is balanced at -2 to 5, on the point difference between father and child
I have a visit rule that is balanced 0 to 16 on the visit difference, but it was rarely used

It converges stupendously fast and it even found me two solutions! (becasue I forgot to stop the search at the soultion, but it ends as soon as the button is pressed. It converges really fast)
SOLUTION: Level: 16 | Visits: 0 | Num Children: 0 | Payload Fitness: 16 16 | Input:
37221274271220 decimal
1035510065136764 octal
[4, 6, 7, 6, 3, 1, 5, 6, 0, 0, 1, 5, 5, 3, 0, 1]
[2, 4, 1, 2, 7, 5, 4, 7, 1, 3, 5, 5, 0, 3, 3, 0]  
[2, 4, 1, 2, 7, 5, 4, 7, 1, 3, 5, 5, 0, 3, 3, 0] < DESIRED

38886110969332 decimal
1065674065136764 octal 
SOLUTION: Level: 16 | Visits: 0 | Num Children: 0 | Payload Fitness: 16 16 | Input:
[4, 6, 7, 6, 3, 1, 5, 6, 0, 4, 7, 6, 5, 6, 0, 1]
[2, 4, 1, 2, 7, 5, 4, 7, 1, 3, 5, 5, 0, 3, 3, 0]
[2, 4, 1, 2, 7, 5, 4, 7, 1, 3, 5, 5, 0, 3, 3, 0] < DESIRED

IT CONVERGES!!!

It converges really fast, and I found at least three solutions

37221274271220 octal: 0o1035510065136764 
[4, 6, 7, 6, 3, 1, 5, 6, 0, 0, 1, 5, 5, 3, 0, 1]
[2, 4, 1, 2, 7, 5, 4, 7, 1, 3, 5, 5, 0, 3, 3, 0]

38878594776564 octal: 0o1065604065136764
[4, 6, 7, 6, 3, 1, 5, 6, 0, 4, 0, 6, 5, 6, 0, 1]
[2, 4, 1, 2, 7, 5, 4, 7, 1, 3, 5, 5, 0, 3, 3, 0]  

38886110969332 octal: 0o1065674065136764
[4, 6, 7, 6, 3, 1, 5, 6, 0, 4, 7, 6, 5, 6, 0, 1]
[2, 4, 1, 2, 7, 5, 4, 7, 1, 3, 5, 5, 0, 3, 3, 0] 

I did an octal tree search, where each node is an octal digit.
The traversal from the root to a leaf is the solution.
I have a cursor
At any iteration the cursor can descend to a child or go up to the father
This navigation is controlled by a fitness
10 points for getting cconsecutive rightmost digits right
1 point for getting any digit right
-1 point for each time the node was visited

I added a die rolls
One gives an increasing chance to move the cursor up, for every level below the rightmost matched digit
This is there because left digits do have an effect on right digits up to 5 digits away
I make it so it balances exploration of more near digits with higher effect, vs farther digits with lower effect


I added a die roll
It givess chance to go up the more the child is visited compared to the father

Had still not converged, I had the plan of rolling which child to go to weighted by its fitness

I'm very happy with this tree search algorithm, I think this structure will help me solve more multidimensional discrete problems

TODO: ask llama3.2 to improve documentation







