# Welcome to tabby-catty-elo!

---

# Purpose

## Purpose of this software

The purpose of this software is to enable easy ELO calculation in BP debate tournaments hosted on Tabbycat.

## Purpose of ELO

The purpose of ELO system is to enable comparasons between competitors/debaters, with estimations on likelyhood of one competitor besting another.
The estimated chances shall update based on new data on competition results.

---

# How is ELO calculated?

## Standard ELO system

The standard ELO system formula for determining updates to rankings is used:

$r_1=r_1+k/cdot(1-P_1)$
$r_2=r_2+k/cdot(0-P_1)$

Where $r_1$ is the rating of Team 1 (the team that won), $k$ is the uncertainty factor, and $P_1$ is an estimated probability that Team 1 win and calculated with formula $P_1=r_1/(r_1+r_2)$

## Specific adjustments for BP debate

Team in the first place is considered to have beaten all other teams, team in the second place is considered to have beaten all teams except the team that placed first, and so on...

ELO is calculated as if every debater of the winning team beat every debater of the losing team.

An adjustment is made based on the difference of speaker points awarded to members of the same team. If both speakers received the same amount of speaker points the calculation works as if it were the ordinary ELO system.

$r_1adj = r_1 + (1+S)/cdtok/cdot(1-P_1)$
$r_2adj = r_2 + (1-S)/cdtok/cdot(1-P_2)$

Where $S$ is the amount of speaker points that a team member whose ELO is being adjusted outspoke their partner in that round by.

---

# How to use the software?

## Setup

Clone the repository like you would any other, e.g. by typing 'git clone https://github.com/mikaric-mikaric/tabby-catty-elo' in your favourite terminal.

Make sure you have the required dependencies listed in 'dependencies.txt' file, e.g. by typing 'pip install -r /path/to/requirements.txt' in your favourite terminal.

## Once you start the software

Best commands for getting started:
1. example 1
2. example 2
3. example 3

---

# Credit and thanks

Thanks to the whole debate community for inspiration.

Thanks to all of the makers of Tabbycat software!

All code by Dimitrije Mikarić.
