# FunGameEngineTakeTwo

![test_suite](https://github.com/GregSym/FunGameEngineTakeTwo/actions/workflows/test-suite.yml/badge.svg)


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
Conda environments should work too, but are untested.

* currently you can get the package via installation from the gh
repo directly
```
python -m pip install git:github.com/GregSym/FunGameEngineTakeTwo
```

# Running the Engine
## The most basic engine setup:

```
from gamethonic import Engine


engine = Engine()
# make your modifications at this point
engine.run()
```

# Experimentation

I've started to include a bunch of experimental implementations of games / frontends using the engine

Use of these is currently done by installing gamethonic to an environment and then copying the experimentation folder to that
environment.

<h1> Roadmap: </h1>
<li> A finished product involves incorporating the engine into a graphical frontend so that it can be used as exactly that - an engine </li>
<li> The immediate goal is to mock up some more examples with which to drive engine development </li>

<h2> Some fun extras under consideration </h2>
<li> Ultimately, an abstraction for plugging in Neural Networks would be a cool place to go and a lot of the required abstractions are already in place </li>
<li> A built in UI layout toolkit for python that uses declarative language </li>

<h1> Devices: </h1>

<p> The ones I've tested </p>

<li> Windows 10 </li>
<li> Ubuntu (WSL + Azure/GH-Actions Server) </li>
