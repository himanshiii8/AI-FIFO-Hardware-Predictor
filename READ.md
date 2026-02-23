\# AI-Driven Hardware Area Predictor (VLSI/FPGA)



\## 📌 Overview

This project establishes an AI-driven framework for predicting the hardware cost (Area/Logic Cells) of parameterized digital designs (FIFOs) instantly. It addresses the inefficiency of traditional Electronic Design Automation (EDA) synthesis tools, which can take minutes or hours to run. By replacing the traditional CAD workflow with a Machine Learning model, this tool reduces estimation time from minutes to milliseconds.



\## 🚀 Key Features \& Pipeline

1\. \*\*Automated Data Generation:\*\* Uses a custom Python script to drive the \*\*Yosys\*\* open-source synthesis tool, automatically generating over 5,000 unique synthetic FIFO designs by varying Bus Width (8–128 bits) and Depth (2–1024 words).

2\. \*\*Machine Learning Core:\*\* Trains a \*\*Random Forest Regressor\*\* to learn the complex, non-linear "step-function" behavior of FPGA mapping.

3\. \*\*Scientific Validation:\*\* Benchmarks the AI against traditional mathematical models (Linear Regression), proving that AI successfully captures hardware optimizations that simple math misses.

4\. \*\*The "Reverse Solver":\*\* A practical application tool where an engineer inputs a specific resource budget (e.g., "5000 cells"), and the AI instantly scans thousands of combinations to recommend the optimal design configuration.



\## 📊 Results \& Engineering Insights

\* \*\*High Accuracy:\*\* The Random Forest model achieved an accuracy of \*\*~98%\*\* on unseen test data.

\* \*\*Reliability (Unbiased Error):\*\* Residual analysis revealed a perfect Gaussian "Bell Curve" centered at zero, proving the model is highly reliable and does not systematically overestimate or underestimate area.

\* \*\*Hardware Insight (Width vs. Depth):\*\* Feature importance analysis proved that increasing a design's \*\*Width (0.53)\*\* is more expensive than increasing its \*\*Depth (0.47)\*\*. This is because width incurs a linear penalty in logic cells, while depth leverages highly optimized internal FPGA memory blocks (BRAMs/LUTRAMs).



\## 🛠️ Tech Stack

\* \*\*Language:\*\* Python, Verilog

\* \*\*Hardware Tools:\*\* Yosys Open SYnthesis Suite

\* \*\*AI/ML Libraries:\*\* Scikit-Learn, Pandas, NumPy

\* \*\*Visualization:\*\* Matplotlib, Seaborn



\## 📁 Project Structure

\* `step1\_generate.py` - Automates Yosys to generate the dataset.

\* `train.py` - Cleans data and trains the Random Forest model.

\* `compare.py` - Evaluates Random Forest vs. Linear Regression.

\* `step4\_reverse\_solver.py` - The interactive Design Explorer tool.

\* `step5\_error\_analysis.py` - Generates the Bell Curve error distribution.

\* `step6\_feature\_importance.py` - Analyzes the cost impact of Width vs. Depth.

\* `dataset\_clean.csv` - The raw generated hardware data.

\* `requirements.txt` - Library dependencies.



\## ⚙️ How to Run

1\. Install dependencies:

&nbsp;  ```bash

&nbsp;  pip install -r requirements.txt

