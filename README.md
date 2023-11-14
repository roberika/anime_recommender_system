# Anime Recommender System

Machine Learning assignment about making an app that recommends anime using KNN principles

## Pitch

So, your a new anime fan, eh? Or you're an oldie that's just returning? Or a recent vet that wanted to explore the deep end? Anyway, this is the app to help you discover new old anime. This app is made based on a Machine Learning algorithm that checks how close the audience is from one anime to another. Its goal is to help you finding new apps that might catch your fancy based on the anime you've watched. Like Bleach? How about Naruto and similiar classic Shonen. More touching cinematographies like Kimi No Nawa? How about Makoto Shinkai's other works, or even the similiarly touching Koe no Katachi. Cool right?

## Algorithm

The ARS uses Collaborative Filtering based on K-Nearest Neighbor algorithm that measures distance with Cosine Similiarity. This distance is then stored as the model and used to measures how similiar the audience between two anime are.

## Limitations

The data this algortihm is trained on is from 2020, so it doesn't include anime from after that year. This escpecially means it doesn't consider Isekai, the major genre that only became major after the year 2020. It also doesn't include ratings from after that year, and that means no ratings from the lockdown period where people are most likely to watch anime, and it also before the boom of anime becoming mainstream. All this to say, yeah I need a better database because this one is severly outdated.

## Setup Guide

For the editing software, I personally just used IDLE that comes prepackage with python. That said, IDLE is very primitive and you should probably either use Jupyter Notebook or VSCode. I've never used those for python though so you'll have to learn them through tutorials.

First, before anything else, install the latest version of Python. After the first step, run **module_install.bat** to install relevant packages for this algorithm. Then run **main.py**. That program will filter the data and clean it before feeding it to the algorithm. After that, run **knn.py** that would actually train the file.

If you want to preview the data, **DO NOT** do it through the .csv file. It's way to unreadable for the human eye. Instead, uncomment the lines where it says **write_[type]_data**. Those lines will call the function to write the data into txt files, which you can then read in **Notepad++**. No, normal Notepad can't handle those files either.





