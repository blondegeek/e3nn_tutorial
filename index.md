# E(3) Equivariant Neural Network Tutorial
#### For original tutorial page [click here](/index_orig).

### ([Recommended Reading](#reading) // [Code](#code) // [Slides](https://docs.google.com/presentation/d/1PznWO7HULKSal_fkPttho735UUmNgXXclIT6EQPaeCU/edit?usp=sharing) )

### Tutorials by [Tess E. Smidt](https://crd.lbl.gov/departments/computational-science/ccmc/staff/alvarez-fellows/tess-smidt/) and [Josh Rackers](https://cfwebprod.sandia.gov/cfdocs/CompResearch/templates/insert/profile.cfm?jracker)

#### Special thanks to [Mario Geiger](https://mariogeiger.ch/), [Ben Miller](http://mathben.com/), [Kostiantyn Lapchevskyi](https://www.linkedin.com/in/klsky/) for all they do for the `e3nn` repo and them, [Daniel Murnane](https://www.linkedin.com/in/daniel-murnane-01277031/), and [Sean Lubner](https://eta.lbl.gov/people/Sean-Lubner) for many conversations that lead to the generation of the tutorial notebooks.

* * *

## Recommended Reading {#reading}
* [Cormorant: Covariant Molecular Neural Networks](https://arxiv.org/abs/1906.04015)
  * Brandon Anderson, Truong-Son Hy, Risi Kondor

* [3D Steerable CNNs: Learning Rotationally Equivariant Features in Volumetric Data](https://arxiv.org/abs/1807.02547)
  * Maurice Weiler, Mario Geiger, Max Welling, Wouter Boomsma, Taco Cohen

* [Tensor field networks: Rotation- and translation-equivariant neural networks for 3D point clouds](https://arxiv.org/abs/1802.08219)
  * Nathaniel Thomas, Tess Smidt, Steven Kearnes, Lusann Yang, Li Li, Kai Kohlhoff, Patrick Riley

* * *

## Code {#code}
For code examples, we will be using the [`se3cnn` repository](https://github.com/mariogeiger/se3cnn). Installation instructions can be found [here](https://github.com/mariogeiger/se3cnn/#installation). To test your installation of `se3cnn`, we recommend running the [following code example](https://github.com/mariogeiger/se3cnn/blob/point/examples/point/tetris.py).

To follow along during the tutorial, we recommend you clone the tutorial repository in addition to installing `se3cnn`.
```
git clone git@github.com:blondegeek/e3nn_tutorial.git
```

Be sure to unzip the `cache.zip` which has all Clebsch-Gordon tensors up to L=10 so that you don't have to compute these locally.

### Tutorial notebooks
* Data types: Going between geometric tensors in Cartesian and spherical harmonic bases and representation lists (`Rs`) in `se3cnn`
  * ( [notebook](https://github.com/blondegeek/e3nn_tutorial/blob/master/data_types.ipynb) // [html](https://blondegeek.github.io/e3nn_tutorial/data_types.html) )
* Operations on Spherical Tensors: Visualization of spherical tensor addition and products
  * ( [notebook](https://github.com/blondegeek/e3nn_tutorial/blob/master/operations_on_spherical_tensors.ipynb) // [html](https://blondegeek.github.io/e3nn_tutorial/operations_on_spherical_tensors.html) )
* Simple Tasks and Symmetry: Using equivariant networks can have unintuitive consequences, we use 3 simple tasks to illustrate how network outputs must have equal or higher symmetry than inputs.
  * ( [notebook](https://github.com/blondegeek/e3nn_tutorial/blob/master/simple_tasks_and_symmetry.ipynb) // [html](https://blondegeek.github.io/e3nn_tutorial/simple_tasks_and_symmetry.html) )
* Nuts and Bolts of `se3cnn`: A step by step walkthrough of how to set up a convolution and what is going on with all those `partial`s.
  * ( [notebook](https://github.com/blondegeek/e3nn_tutorial/blob/master/nuts_and_bolts_of_se3cnn.ipynb) )

#### Why notebook AND html?
For the notebooks that use `plotly` the notebooks are distributed without cells executed because the plots are large (because Tess made them too high-resolution... oops.). If you download the HTML verison, you can interact with the plots without needing to execute the code.

#### Got feedback on the code tutorials?
Tess wants to hear all about it, so please, please, please write Tess an email at `tsmidt@lbl.gov` or `blondegeek@gmail.com`! The goal is to make these notebooks maximally useful to others. 
* * *

