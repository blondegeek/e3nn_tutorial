# E(3) Equivariant Neural Network Tutorial

## Spacetime coordinates
Thursday, November 14, 2019
<br>
10:00 am - noon, 1:30 - 2:30 pm
<br>
Main Lecture Hall
<br>
Institute for Pure and Applied Mathematics (IPAM)
<br>
University of California, Los Angeles

## Tutors: [Tess E. Smidt](https://crd.lbl.gov/departments/computational-science/ccmc/staff/alvarez-fellows/tess-smidt/) and [Risi Kondor](http://people.cs.uchicago.edu/~risi/)

## Agenda
### 10:00 am - noon
Tutorials with lecture and code

### 1:30 - 2:30 pm
Remaining topics and open discussion

## Code
For code examples, we will be using the [`se3cnn` repository](https://github.com/mariogeiger/se3cnn). Installation instructions can be found [here](https://github.com/mariogeiger/se3cnn/#installation). To test your installation of `se3cnn`, we recommend running the [following code example](https://github.com/mariogeiger/se3cnn/blob/point/examples/point/tetris.py).

To follow along during the tutorial, we recommend you clone the tutorial repository in addition to installing `se3cnn`.
```
git clone git@github.com:blondegeek/e3nn_tutorial.git
```
<font color="green"><b>WARNING: Tess is still actively changing these notebooks, so pull frequently. :) </b></font>

### Tutorial notebooks:
* Data types: Going between geometric tensors in Cartesian and spherical harmonic bases and representation lists (`Rs`) in `se3cnn`
  * ( [notebook](https://github.com/blondegeek/e3nn_tutorial/blob/master/data_types.ipynb) // [html](https://github.com/blondegeek/e3nn_tutorial/blob/master/data_types.html) )
* Simple Tasks and Symmetry: Using equivariant networks can have unintuitive consequences, we use 3 simple tasks to illustrate how network outputs must have equal or higher symmetry than inputs.
  *( [notebook](https://github.com/blondegeek/e3nn_tutorial/blob/master/simple_tasks_and_symmetry.ipynb) // [html](https://github.com/blondegeek/e3nn_tutorial/blob/master/simple_tasks_and_symmetry.html) )

## Recommended Reading
* [Cormorant: Covariant Molecular Neural Networks](https://arxiv.org/abs/1906.04015)
  * Brandon Anderson, Truong-Son Hy, Risi Kondor

* [3D Steerable CNNs: Learning Rotationally Equivariant Features in Volumetric Data](https://arxiv.org/abs/1807.02547)
  * Maurice Weiler, Mario Geiger, Max Welling, Wouter Boomsma, Taco Cohen

* [Tensor field networks: Rotation- and translation-equivariant neural networks for 3D point clouds](https://arxiv.org/abs/1802.08219)
  * Nathaniel Thomas, Tess Smidt, Steven Kearnes, Lusann Yang, Li Li, Kai Kohlhoff, Patrick Riley

