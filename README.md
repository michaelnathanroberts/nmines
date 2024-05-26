# nmines

An open-source game of Minesweeper, powered by pygame.

<h2> Execution </h2>
~/nmines $ python3 main.py

<h2> Manual </h2>
<h3> Setup </h3>

Create a m*k game with n mines. The game has m cells widthwise and k cells heightwise.
Change the parameters through the sliders.

<h3> Gameplay </h3>

<h4> Objective </h4>
The objective is to reveal all non-mine cells without revealing a single mine cell.

<h4> Revealing Cells </h4>
Click a cell in order to reveal its contents. For every non-mine cell, there is a number indicating how many mine cells are adjacent to it (including diagonally). If the number is zero, the number is omitted and all adjacentcells are revealed. If all non-mine cells are
revealed, the player wins. If the player reveals a mine cell, the game is over and they lose.
Furthermore, all mine cells are released.

<h4> Flags </h4>

The flag feature exists to assist the player. A player may flag an unrevealed cell
by hovering over it while pressing the 'f' key. If the player hovers over a flagged cell
while pressing the 'f' key, they unflag it. Clicking a flagged cell has no effect.

<h3> Navigation </h3>

A player may restart the game at any time, keeping the current settings. A player may access the menu at any time to create a new game with their desired settings. Accessing the menu 
terminates the current game.