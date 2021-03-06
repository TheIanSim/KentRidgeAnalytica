# KentRidgeAnalytica

1. This project runs on Python, please ensure you have it installed (download link [here](https://www.python.org/downloads/)).
2. Clone this repo and run `pip install -r requirements.txt` to install the necessary packages/modules.

### Original Scenario

* In `main.py`(line 6), ensure that the variable `SCENARIO` = `0`.
* Run `main.py`: `python main.py`.
* The output file will appear in the `outputs` folder as `gephi_output_main.csv`.
* By importing this file into Gephi, you can create the animation showing how the fake news would spread in the network.

![How fake news spread in the network](img/spread_original.gif)


### What-If Scenario #1: Removal of Central Nodes

* In `main.py`(line 6), ensure that the variable `SCENARIO` = `1`.
* Run `main.py`: `python main.py`.
* The output file will appear in the `outputs` folder as `gephi_output_central_nodes_removed.csv`.
* By importing this file into Gephi, you can create the animation showing how the fake news would spread in the network.


### What-If Scenario #2: Addition of Edges (via Enforcement of Triadic Closure property)

* In `main.py`(line 6), ensure that the variable `SCENARIO` = `2`.
* Run `main.py`: `python main.py`.
* The output file will appear in the `outputs` folder as `gephi_output_triadic_closure.csv`.
* By importing this file into Gephi, you can create the animation showing how the fake news would spread in the network.
