# Project By: Jason Yi, Richy Chen, Abel Leulseged, Tony Jiang, Susan Xiao

# Market Modeling

## 1. Background
The goal of this project is to use deep learning to predict the prices/rates of eight financial assets. We use Tensorflow to develop both LSTM and ESN RNN models and compare the models. Then, we use the better model in our web application, which is built on Flask. The web application allows any user to use our model to predict up to eight of the financial assets' prices/rates for however many days and measured using either the prices/rates or growth rates.

## 2. Deliverables
Our project has multiple deliverables that show our journey and the successes and failures of our project.

### 2.1 Web Application
Our web application is at [Market Modeling](https://market-modeling.herokuapp.com). This is the most visual and easiest way of viewing our project. We used Chartist.js to make our graphs. The graphs do not show good results for our neural network, as our model does not do a good job of predicting the actual values of the financial assets.

### 2.2 Testing
We tested both our web application and our models. See the results [here](./test/).

### 2.3 Research Report
We have written a short research report on our results [here](https://www.cs.hmc.edu/~rchen/Markets_NN_Final_Report.pdf). This summarizes our methodology and results in a research-style report.

## 3. Structure of Repository

### 3.1 Neural Networks
We developed LSTM and ESN RNN models to predict financial asset price movements. The jupyter notebook for those can be found [here (LSTM)](./lstm/) and [here (ESN)](./esn/).

### 3.2 Flask
We used Flask to quickly develop a web application that showcases our model. The HTML files are in the [templates folder](./templates/), while the other resources are in the [static folder](./static/). These other resources include Javascript files, CSS files, images, data, and our saved models. To complete the app, we have an app.py file in the current directory, along with a predict.py module that helps with using the saved models.

### 3.3 Coding Style Guide
Our coding style documents can be found [here](./style/).

### 3.4 Other
To manage Python versions for this project, we used Pipenv, which explains the Pipfile and Pipfile.lock files.
