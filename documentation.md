# Moran [Py]cess: Documentation & How-to

- [Moran [Py]cess: Documentation & How-to](#moran-pycess-documentation--how-to)
  - [Statement of need](#statement-of-need)
  - [Dependencies](#dependencies)
  - [General Moran Process](#general-moran-process)
  - [Moran Model based on 2D neighbourhood](#moran-model-based-on-2d-neighbourhood)
  - [Moran Model based on 3D neighbourhood](#moran-model-based-on-3d-neighbourhood)
  - [Use cases](#use-cases)

## Statement of need

Moran [Py]cess is a Python package with a general game-theoretical framework for scientific simulations according to the Moran model. It is aimed to capture dynamics of populations composed of individuals of distinct phenotypes (which correspond to *strategies* in the language of game theory). Individual's fitness is calcualted based on its average payoff, averaged over interactions with other members of the group. The package is both simple in use and robust, allowing any possible model of an antagonistic game to be considered. It serves well as a research aid for evolutionary, computational as well as cell biologists as it allows to simulate two-dimensional and three-dimensional populations too.

## Dependencies

For a complete list of dependencies for this package please inspect the [conda environment recipe](env/main.yml).

## General Moran Process

From the user's perspective only one class is relevant: *MoranProcess*.

Initializer of the *MoranProcess* has the follwing signature:
```python
def __init__(self, size_list, label_list, BirthPayoffMatrix, DeathPayoffMatrix, TransitionMatrix=None):
```

With the following arguments:
```python
size_list # list of integers which represent the cardinality of distinct sub-populations

label_list # list of strings which represent the labels of individuals from distinct sub-populations

BirthPayoffMatrix # payoff matrix based on which individuals' Birth Fitness is calculated. Used for the roulette-based selection of an individual to reproduce

DeathPayoffMatrix # payoff matrix based on which individuals' Death Fitness is calculated. Used for the roulette-based selection of an individual to die

TransitionMatrix # an optional parameter: a matrix similar to Birth/Death payoffs which specifies transition probabilities from a given Strategy (rows) to another (columns). Row sums must equal to one. If this parameter is specified at the end of each Birth-Death cycle each of the individuals will randomly sample to switch Strategies.
```

Both individuals' selection for reproduction and death are proportional to individuals' fitnesses calculated based on two separate payoff matrices (Birth/Death). For a *random* selection please provide a `numpy` array composed entirely of single values.  
**Payoffs always need to be non-negative**

Example of creating a *MoranProcess* instance:  
(assuming working in an environment where the package is installed)

```python
import numpy as np
import moranpycess

size_list = [10, 10]
label_list = ["a", "b"]
BirthPayoffMatrix = np.array([[1, 2], [3, 4]])
DeathPayoffMatrix = np.array([[0.1, 0.2], [0.3, 0.4]])

mp = moranpycess.MoranProcess(
    size_list=size_list,
    label_list=label_list,
    BirthPayoffMatrix=BirthPayoffMatrix,
    DeathPayoffMatrix=DeathPayoffMatrix,
)
```

The key method of this object is a called `simulate(generations)` and it takes an integer as an argument (simulation time specified as a number of birth-death cycles). This function returns a `pandas` dataframe with a per-cycle summary of the population's state.
The following code demonstrated the simulation:
```python
import pandas as pd

df = mp.simulate(1000)
```

Information which are stored in the dataframe's columns include:
* per-sub-population sub-population's size
* per-sub-population Average Birth Payoff for a single individual of a given sub-population (averaged over interactions with all other individuals of the whole population)
* per-sub-population Average Death Payoff for a single individual of a given sub-population (averaged over interactions with all other individuals of the whole population)
* per-sub-population Birth Fitness of an individual from a given sub-popualtion
* per-sub-population Death Fitness of an individual from a given sub-popualtion
* Entropy of the distribution of Strategies in the whole population

Additionally to the *MoranProcess* class the user is equipped with several plotting functions to visualise results of the simulation:
* `PlotSize`
* `PlotAvgBirthPayoff`
* `PlotAvgDeathPayoff`
* `PlotBirthFitness`
* `PlotDeathFitness`
* `PlotEntropy`

Each of which with the same signature:
```python
def FUNCTION(mp, df, path):
```

With the following arguments:
```python
mp # instance of the MoranProcess

df # simulation results - pandas dataframe returned by the method .simulate()

path # path for the output plot in png format
```

Following the previous simulation one may generate the plots with:
```python
moranpycess.PlotSize(mp, df, "Size.png")
moranpycess.PlotAvgBirthPayoff(mp, df, "AvgBirthPayoff.png")
moranpycess.PlotAvgDeathPayoff(mp, df, "AvgDeathPayoff.png")
moranpycess.PlotBirthFitness(mp, df, "BirthFitness.png")
moranpycess.PlotDeathFitness(mp, df, "DeathFitness.png")
moranpycess.PlotEntropy(mp, df, "Entropy.png")
```

## Moran Model based on 2D neighbourhood

From the user's perspective only one class is relevant: *MoranProcess2D*.

Initializer of the *MoranProcess2D* has the follwing signature:
```python
def __init__(self, size_list, label_list, grid, BirthPayoffMatrix, DeathPayoffMatrix, TransitionMatrix=None):
```

All arguments are the same as for the class *MoranProcess* except the additional one:

```python
grid # 2-dimensional numpy array filled with strings from the "label_list" according to their cardinality in "size_list". This argument essentially specifies the initial spatial state of the population.
```

Similarly as in the previous case:  
Both individuals' selection for reproduction and death are proportional to individuals' fitnesses calculated based on two separate payoff matrices (Birth/Death).  
However, the average payoffs (and therefore fitnesses) of each individual is calculated based only on its direct neighbourhood in the population (8 neighbours). For individuals at boundaries we apply periodic boundary conditions.  
For a *random* selection please provide a `numpy` array composed entirely of single values.  
**Payoffs always need to be non-negative**

Example of creating a *MoranProcess2D* instance:  
(assuming working in an environment where the package is installed)

```python
import numpy as np
import moranpycess

size_list = [3, 1]
label_list = ["A", "B"]
grid = np.array([["A", "A"], ["A", "B"]])
BirthPayoffMatrix = np.array([[10, 10], [15, 1]])
DeathPayoffMatrix = np.array([[1, 1], [1, 1]])

mp = moranpycess.MoranProcess2D(
    size_list=size_list,
    label_list=label_list,
    grid=grid,
    BirthPayoffMatrix=BirthPayoffMatrix,
    DeathPayoffMatrix=DeathPayoffMatrix,
)
```

Similarly as in the previous case:  
The key method of this object is a called `simulate(generations)` and it takes an integer as an argument (simulation time specified as a number of birth-death cycles). This function returns a `pandas` dataframe with a per-cycle summary of the population's state.
The following code demonstrated the simulation:
```python
import pandas as pd

df = mp.simulate(10)
```

In case of the simulation in 2D each Birth-Death cycle consist of the following steps:
1. Select an individual for reproduction (fitness-proportional selection)
2. Out of its neigbours: select an individual to die (fitness-proportional selection)
3. Copy the selected individual from (1) in place of the one from (2)
4. Perform Transitions for each individual (in case `TransitionMatrix` was specified)
5. Update Payoffs and Fitnesses

Information which are stored in the dataframe's columns include:
* per-sub-population sub-population's size
* Entropy of the distribution of Strategies in the whole population

Additionally to the *MoranProcess2D* class the user is equipped with three plotting functions to visualise results of the simulation:
* `PlotSize2D`
* `PlotEntropy2D`
* `PlotPopulationSnapshot2D`

With `PlotSize2D` and `PlotEntropy2D` having the same signatures as their previous analogues. The latter, `PlotPopulationSnapshot2D`, may produce a heatmap-like snapshot of a population at it's current state:
```python
def PlotPopulationSnapshot2D(mp, path):
```

With the following arguments:
```python
mp # instance of the MoranProcess

path # path for the output plot in png format
```

Following the previous simulation one may generate the plots with:
```python
moranpycess.PlotSize2D(mp, df, "Size2D.png")
moranpycess.PlotEntropy2D(mp, df, "Entropy2D.png")
moranpycess.PlotPopulationSnapshot2D(mp, "PopulationSnapshot2D.png")
```

## Moran Model based on 3D neighbourhood

From the user's perspective only one class is relevant: *MoranProcess3D*.

Initializer of the *MoranProcess3D* has the follwing signature:
```python
def __init__(self, size_list, label_list, grid, BirthPayoffMatrix, DeathPayoffMatrix, TransitionMatrix=None):
```

All arguments are the same as for the class *MoranProcess2D* with the note that this time `grid` is a 3-dimensional array.

Similarly as in the previous case:  
Both individuals' selection for reproduction and death are proportional to individuals' fitnesses calculated based on two separate payoff matrices (Birth/Death).  
However, the average payoffs (and therefore fitnesses) of each individual is calculated based only on its direct neighbourhood in the population (26 neighbours). For individuals at boundaries we apply periodic boundary conditions.  
For a *random* selection please provide a `numpy` array composed entirely of single values.  
**Payoffs always need to be non-negative**

Example of creating a *MoranProcess3D* instance:  
(assuming working in an environment where the package is installed)

```python
import numpy as np
import moranpycess

size_list = [7, 1]
label_list = ["A", "B"]
grid = np.array([[["A", "A"], ["A", "B"]], [["A", "A"], ["A", "A"]]])
BirthPayoffMatrix = np.array([[10, 20], [30, 40]])
DeathPayoffMatrix = np.array([[1, 2], [3, 4]])

mp = moranpycess.MoranProcess3D(
    size_list=size_list,
    label_list=label_list,
    grid=grid,
    BirthPayoffMatrix=BirthPayoffMatrix,
    DeathPayoffMatrix=DeathPayoffMatrix,
)
```

Similarly as in the previous cases:  
The key method of this object is a called `simulate(generations)` and it takes an integer as an argument (simulation time specified as a number of birth-death cycles). This function returns a `pandas` dataframe with a per-cycle summary of the population's state.
The following code demonstrated the simulation:
```python
import pandas as pd

df = mp.simulate(10)
```

In case of the simulation in 3D each Birth-Death cycle consist of the following steps:
1. Select an individual for reproduction (fitness-proportional selection)
2. Out of its neigbours: select an individual to die (fitness-proportional selection)
3. Copy the selected individual from (1) in place of the one from (2)
4. Perform Transitions for each individual (in case `TransitionMatrix` was specified)
5. Update Payoffs and Fitnesses

Information which are stored in the dataframe's columns include:
* per-sub-population sub-population's size
* Entropy of the distribution of Strategies in the whole population

Additionally to the *MoranProcess3D* class the user is equipped with two plotting functions to visualise results of the simulation:
* `PlotSize3D`
* `PlotEntropy3D`

The functions have the same signatures as their previous analogues.  
Following the previous simulation one may generate the plots with:
```python
moranpycess.PlotSize3D(mp, df, "Size3D.png")
moranpycess.PlotEntropy3D(mp, df, "Entropy3D.png")
```

## Use cases

For more real-life examples of how to utilise the package please take a look at our use-case [notebook](tests/usecase.ipynb).
