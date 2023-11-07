# Assignment 1: "The 6 boxes"

## Introduction

There are 6 golden boxes all positioned in circle around a gray region, as shown in figure, and a mobile robot with an end effector. The robot's characteristics are described in the README in robot-sim folder. 
The aim of the assignment is to bring all the boxes together grabbing them with the robot's end effector.

<p align="center">
  <img src = "images/Arena.png" alt = "How arena looks like">
</p>

<p>
  Even if it wasn't requested, I did this so that the boxes are collected in the gray region. I thought that it was the smartest way to bring toghether all the boxes, because, doing this, the robot takes advantage of the fact that they are all placed in circle so it moves less (minimum Euclidean distance). 

  During the simuliation there will be two windows:
  - The turtle simulator, in which you can see the robot working;
  - Terminal, that displays messagges from the robot, and it is useful to better understand how it works.
</p>

## Steps and Flowchart

The main program is composed by the robot initialization, where are initialized the most important variables, and by a while loop. This while loop is splitted in two sections:

- the first that contains all the actions that the robot do, when isn't grabbing any token, in order to take the nearest and right token;

- the second one that makes the robot release the token in the right place and starts if and only if the robot is moving a token.

<p>
  All the reasonings and steps are described in the flowchart below.
</p>

<p align= "center">
  <img src = "images/Flowchart.png">
  
  While markers is the variables that contains all the markers that the robot sees, marker_taken contains only the markers that are moved to the center. Doing this is easyer to determine wich of the markers that robot seen have been already moved and wich not.
  
</p>

## Functions

For making coding simpler, I've realised some useful functions.

## Results and conclusions
