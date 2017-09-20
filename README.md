# Na Czas
![Logo](https://raw.githubusercontent.com/pawelaugustyn/django/master/MainLogo.png)

## Introduction
This project was made as a part of "Python in the Enterprise" course run at AGH University of Science & Technology at the Faculty of Physics and Applied Computer Science.

The aim of the project was to use Warsaw's Public Transport online data. We managed to make it much more user-friendly and useful in daily routine.


## Installation
- Needed python version: 2.7.13
- All of needed dependencies: listed in [requirements.txt](requirements.txt) file.
- File needed for parsers: [Click here](http://bit.ly/2hgWuUh)

All of the needed files are currently present in the repo. File provided in link above was used to create all of the used data.
We didn't attach it to the repo because of it's size, which exceeds maximum size per file GitHub's policy.

## Detailed description
### Project targets
Our aim was to use [Warsaw's Public Transport API](http://api.um.warszawa.pl) alongside [ZTM Scheduling data](http://ztm.waw.pl/?c=628).
Main target was to display all of the running trams on the map in the corresponding positions. Trams positions are indicated by black tram icon.
Then using Machine Learning we wanted to predict the arrival times on chosen stops.
That project is the first to combine these two features (considering only portals that uses data provided by Warsaw Public Transport).
It gives people possibility to be always on time regardless of traffic jams. Standard schedules don't provide that functionality.

### Main difficulties
The biggest obstacle we've encountered was file provided by ZTM. It's size is over 200MB+ and it contains approximately 5 million lines.
If we wanted to have our data up to date, we would need a lot of free disk space to store it. It's enormously big.
We did our best to decrease the filesize as much as possible. Most of the time we spent on that project was to parse that file.

### Main technologies we used:
- Python (obviously)
- Django framework
- Machine Learning (scikit-learn library)
- jQuery (for managing maps)

### UI Presentation
![UI](https://raw.githubusercontent.com/pawelaugustyn/django/master/MainPageDesc.png)

### Contributors
- [Katarzyna Latos](http://github.com/katarzynalatos)
- [Pawel Augustyn](http://github.com/pawelaugustyn)
- [Piotr Janus](http://github.com/piotrjanus)
- [Jakub Kremer](http://github.com/j-kremer)
- [Mateusz Lis](http://github.com/grizzlymati)

### Supervisors
- dr. hab. inż. Tomasz Szumlak
- mgr. inż. Adam Dendek

### Live Demo
Live Demo of that project is available [here](http://pitedjango.herokuapp.com).
