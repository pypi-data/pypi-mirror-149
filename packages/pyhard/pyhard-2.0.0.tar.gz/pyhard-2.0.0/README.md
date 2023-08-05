<!--
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/ita-ml%2Finstance-hardness/binder?filepath=notebooks%2F)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://en.wikipedia.org/wiki/MIT_License)
-->

# PyHard

Instance Hardness analysis in Python, with a two-fold objective: insights on data quality issues; 
and better understanding of the weaknesses and strengths of different algorithms.

* Documentation: https://ita-ml.gitlab.io/pyhard/
* Source code: https://gitlab.com/ita-ml/pyhard
* Bug reports: https://gitlab.com/ita-ml/pyhard/-/issues

## Getting Started

PyHard employes a methodology known as [_Instance Space Analysis_](https://github.com/andremun/InstanceSpace) (ISA) to analyse performance at the instance level rather than at dataset level. The result is an alternative for visualizing algorithm performance for each instance within a dataset, by relating predictive performance to estimated instance hardness measures extracted from the data. This analysis reveals regions of strengths and weaknesses of predictors (aka _footprints_), and highlights individual instances within a  dataset that warrant further investigation, either due to their unique properties or potential data quality issues.


### Installation
Although the original ISA toolkit has been written in Matlab, we provide a lighter version in Python, with less tools, but enough for the instance hardness analysis purposes. You may find the implementation in the separate package [PyISpace](https://gitlab.com/ita-ml/pyispace). Notwithstanding, the choice of the ISA engine is left up to the user, which can be set in the configuration file. Below, we present the standard installation, and also the the additional steps to configure the Matlab engine (optional).

_For users_

```
pip install pyhard
```

_For developers_

Alternatively, if you are a developer and want to contribute, the following installation is better suited for testing new features:
```
git clone https://gitlab.com/ita-ml/pyhard.git
cd pyhard
pip install -e .
```

#### Anaconda environment

Use the file [environment.yml](./environment.yml) to create a conda env with all required dependencies:

```
conda env create --file environment.yml
```


### Usage

First, make sure that the configuration files are placed within the current directory and the settings are the desired ones. To generate those files, run

```
pyhard init
```

This will create both `config.yaml` and `options.json` in the current directory.

The file `config.yaml` is used to configurate steps 1-4 below. Through it, options for file paths, measures, classifiers, feature selection and hyper-parameter optimization can be set. More instructions can be found in the comments within the file.

At least the field `datafile` (in section 'general') should be set in `config.yaml`. It specifies the path (absolute or relative) of the input dataset. Leaving the field `rootdir` as `'.'` (default), the output files will be saved in the current folder along with the configuration files (recommended).

Once everything is configured, run the analysis:

```
pyhard run
```

By default, the following steps shall be taken:

1. Calculate the _hardness measures_;

2. Evaluate classification performance at instance level for each algorithm;

3. Select the most relevant hardness measures with respect to the instance classification error;

4. Join the outputs of steps 1, 2 and 3 to build the _metadata_ file (`metadata.csv`);

5. Run __ISA__ (_Instance Space Analysis_), which generates the _Instance Space_ (IS) representation and the _footprint_ areas;

Steps 1 to 4 comprise the metadata construction, and step 5 the ISA itself. To curb any of these two major stages, use the options with command `run`:

* `--no-meta`: does not attempt to build the metadata file

* `--no-isa`: prevents the Instance Space Analysis

Finally, to explore the results, launch the app:  

```
pyhard app
```

To see all CLI commands, run `pyhard --help`, or `pyhard run --help` to get the options for this command.


### Guidelines for input dataset

Please follow the recommendations below:

* Only `csv` files are accepted

* The dataset should be in the format `(n_instances, n_features)`

* It cannot contains NaNs or missing values

* **Do not** include any index column. Instances will be indexed in order, starting from **1**

* **The last column** should contain the target variable (`y`). Otherwise, the name of the target column must be declared in the field `target_col` (config file)

* Categorical features should be handled previously


### Demo mode

A simple demo can also be launched for a first contact with the tool, requiring no initial setup:

```
pyhard demo
```


## Citation

If you're using PyHard in your research or application, please cite our [paper](https://datacentricai.org/papers/30_CameraReady_DCAI_2021_camera_ready.pdf):

> Paiva, P.Y.A., Smith-Miles, K., Valeriano, M.G., & Lorena, A.C. PyHard: a novel tool for generating hardness embeddings to support data-centric analysis. In 1st NeurIPS Workshop on Data Centric AI (DCAI'21), 2021.

```
@inproceedings{
      paiva2021pyhard,
      title={PyHard: a novel tool for generating hardness embeddings to 
      support data-centric analysis}, 
      author={Pedro Yuri Arbs Paiva and Kate Smith-Miles and Maria Gabriela 
      Valeriano and Ana Carolina Lorena},
      year={2021},
      maintitle={Thirty-fifth Conference on Neural Information Processing Systems},
      booktitle = {Workshop on Data Centric AI (DCAI'21)},
}
```


## References

_Base_

1. Michael R. Smith, Tony Martinez, and Christophe Giraud-Carrier. 2014. __An instance level analysis of data complexity__. Mach. Learn. 95, 2 (May 2014), 225–256.

2. Ana C. Lorena, Luís P. F. Garcia, Jens Lehmann, Marcilio C. P. Souto, and Tin Kam Ho. 2019. __How Complex Is Your Classification Problem? A Survey on Measuring Classification Complexity__. ACM Comput. Surv. 52, 5, Article 107 (October 2019), 34 pages.

3. Mario A. Muñoz, Laura Villanova, Davaatseren Baatar, and Kate Smith-Miles. 2018. __Instance spaces for machine learning classification__. Mach. Learn. 107, 1 (January   2018), 109–147.

_Feature selection_

4. Luiz H. Lorena, André C. Carvalho, and Ana C. Lorena. 2015. __Filter Feature Selection for One-Class Classification__. Journal of Intelligent and Robotic Systems 80, 1 (October   2015), 227–243.

5. Goldberger, J., Hinton, G., Roweis, S., Salakhutdinov, R. (2005). __Neighbourhood Components Analysis__. Advances in Neural Information Processing Systems. 17, 513-520.

6. Yang, W., Wang, K., & Zuo, W. (2012). __Neighborhood component feature selection for high-dimensional data__. J. Comput., 7(1), 161-168.

7. Amankwaa-Kyeremeh, B., Greet, C., Zanin, M., Skinner, W. and Asamoah, R. K., (2020), __Selecting key predictor parameters for regression analysis using modified Neighbourhood Component Analysis (NCA) Algorithm__. Proceedings of 6th UMaT Biennial International Mining and Mineral Conference, Tarkwa, Ghana, pp. 320-325.

8. Artur J. Ferreira and Mário A. T. Figueiredo. 2012. __Efficient feature selection filters for high-dimensional data__. Pattern Recognition Letters 33, 13 (October, 2012), 1794–1804.

9. Jundong Li, Kewei Cheng, Suhang Wang, Fred Morstatter, Robert P. Trevino, Jiliang Tang, and Huan Liu. 2017. __Feature Selection: A Data Perspective__. ACM Comput. Surv. 50, 6, Article 94 (January 2018), 45 pages.

10. Shuyang Gao, Greg Ver Steeg, and Aram Galstyan. __Efficient Estimation of Mutual Information for Strongly Dependent Variables__. Available in http://arxiv.org/abs/1411.2003. AISTATS, 2015.

_Hyper parameter optimization_

11. James Bergstra, Rémi Bardenet, Yoshua Bengio, and Balázs Kégl. 2011. __Algorithms for hyper-parameter optimization__. In Proceedings of the 24th International Conference on Neural Information Processing Systems (NIPS’11). Curran Associates Inc., Red Hook, NY, USA, 2546–2554.

12. Jasper Snoek, Hugo Larochelle, and Ryan P. Adams. 2012. __Practical Bayesian optimization of machine learning algorithms__. In Proceedings of the 25th International Conference on Neural Information Processing Systems - Volume 2 (NIPS’12). Curran Associates Inc., Red Hook, NY, USA, 2951–2959.
  
13. J. Bergstra, D. Yamins, and D. D. Cox. 2013. __Making a science of model search: hyperparameter optimization in hundreds of dimensions for vision architectures__. In Proceedings of the 30th International Conference on International Conference on Machine Learning - Volume 28 (ICML’13). JMLR.org, I–115–I–123.
  
