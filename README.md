# FunGameEngineTakeTwo

![test_program](https://github.com/GregSym/FunGameEngineTakeTwo/actions/workflows/test-suite.yml/badge.svg)


<p>
  An attempt at wrapping a more fully functioning engine around python's pygame module - hardly original work, but I figured I'd do it anyway,
  especially as working off of pygame from scratch every time I want to play around with certain kinds of 2D visual simulation in python is a
  little tedious (and probably a bad idea anyway)
</p>

# Installation

* You are adviced to setup a virtual environment of your choice (windows example below)
```
python -m pip install virtualenv
python -m virtualenv venv
.\venv\Scripts\activate
```
Key Linux/bash difference:
```
source ./venv/bin/activate
```

* currently you can get the package via installation from the gh
repo directly
```
python -m pip install git:github.com/GregSym/FunGameEngineTakeTwo
```

# Experimentation

I've started to include a bunch of experimental implementations of games / frontends using the engine

Use of these is currently done by installing gamethonic to an environment and then copying the experimentation folder to that
environment.

<h1> Devices: </h1>

<p> The ones I've tested </p>

<li> Windows 10 </li>
<li> Ubuntu (WSL + Azure/GH-Actions Server) </li>
