# Model-Insight

Description
============

Model-insight is a Python third-party library that loads commonly used mathematical modeling data sets and performs modeling processing (such as evaluation problems, simulation problems, etc.).
At the same time, we can also learn the related knowledge of mathematical modeling.

Installing
============

Use  `pip`

    >>>pip install model-insight==0.4.2

Load Datasets
=============
    >>>from model_insight.load_datasets import load_#
    
Several datasets are availiable:
- Evaluation
    - Battery
    - Roller coaster
    - Aircraft
- Optimization
    - oil
    - swim
    - portfolio
- Change
    - Population of U.S.
    - Shanghai COVID cases
- Prediction
    - Restaurant sales
    - Mead lake
    - Titanic
- Explaination
    - Adult salary

Multi-criteria Decision Making
==============================
Model-Insight provides some functions to preprocess data, give weights, and do comprehensive evaluation.
For example,

    >>>from model_insight.mcdm_functions import ahp
    >>>judgement_matrix = np.array([[1,2,3],[1/2,1,4],[1/3,1/4,1]])
    >>>ahp_weights = ahp(judgement_matrix)
    >>>ahp_weights
    >>>The Max Eigenvalue is  (3.1078473338549757+0j)
    array([0.51713362+0.j, 0.35856042+0.j, 0.12430596+0.j])

Welcome to cooperation
======================
If you are interested in this project, you can contact me via learningmm@163.com.
