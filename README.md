# gisFYP
My final Year Project for Threat Evaluation and Weapons Assignment system with a simulator based visualization based on geodjango, postgis, leaflet and QGIS
## Project Description
The project is about Threat Evaluation and Weapons Asssignment. The basic modules of the project include:<br/>
1- Threat Evaluation Module<br/>
2- Threat Weapons and Defended assests Visulaization<br/>
3- Simulator<br/>
Threat Evaluation and Weapons Assignment system is the one that evaluates threats present near the terrotiry of Defended Assests and assign weapons to them based on some logic.
### Threat Evaluation Module
Threat Evaluation Module uses a mathematical model to evaluate threats based on multiple parameters such as <br/>
1- Speed of threat <br/>
2- Angle of threat <br/>
3- Latitude and Longitude of threat <br/>
4- Range of threat <br/>
5- Altitude of threat <br/>
6- Distance between threat and Defended Asset<br/>
7- Vitality of Defended Asset <br/>
8- Carried Ammuniation by threat <br/>
### Threat and Defended Assests Visualization<br/>
Visualization is based on two modules working in parallel i.e. Threat Simulator and Threat Evaluator. It is a django, geodjango and Leaflet based app which visualizes the scenarios generated by
the threat simulator.
### Threat Simulator
A simulator which generates the scenarios in which the Threat Evaluation is done. 
### Implementation Details
Simulator and Threat Evaluation module is written in python and integrated in django and geodjango app. Database used is postgis and data is integrated using QGIS.
