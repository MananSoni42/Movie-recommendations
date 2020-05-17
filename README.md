# Movie Recommendations
* This is a basic movie recommendation engine. 
* It uses item-item collaborative filtering 

> Update: I recently created a live website that runs on this algorithm.  
Check it out at [http://movie42-app.herokuapp.com/](http://movie42-app.herokuapp.com/)

### Requirements
* python3+
``` sudo apt-get install python3```
* pip
``` sudo apt-get install python3-pip```
* numpy
```pip3 install numpy```

### Usage
* Ensure that you have downloaded the correct dataset from [here](https://grouplens.org/datasets/movielens/1m/)
* place this folder in Movie-recommendations/dataset
* run ```python3 data_manip.py``` to generate the relevant pickle files
* use the recommendation engine: ```./movie.py```
