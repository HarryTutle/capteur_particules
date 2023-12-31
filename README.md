# capteur_particules
un capteur de particules pm10 et pm25 autonome qui enregistre les données toutes les heures sur carte SD. 

Basé sur un microcontroleur arduino (nano), le capteur intègre dans un boitier les composants suivants:
- le capteur SDS011 de particules pm10/pm25.
- un capteur de température et humidité DHT22.
- un lecteur/enregistreur sur microsd pour arduino.
- une horloge externe DS3231.
- une diode et une résistance 220 ohm.
- un régulateur de charge 12/24 volts.
- une batterie 12 volts et 7,2 A/h.
- un panneau solaire 12 volts et 10W pour alimenter tout ça.

L'objectif du projet est de collecter des données sur une zone fortement industrialisée, et voir si il y a des liens de corrélation entre les variables temps, particules émises, température, humidité...Et autre comme les données météo.

Fonctionnement: Le système tourne avec une arduino nano configurée en mode sleep (basse conso). Toutes les heures, l'horloge externe réveille l'arduino via la broche 2, puis l'arduino active les capteurs SDS011 et DHT22. Elle allume également la diode mais seulement si il y a bien lecture du fichier dans la carte SD (contrôle si ça enregistre bien). Pendant deux minutes, les capteurs sont activés, puis la troisième minute les données sont enregistrées chaque seconde sur la carte SD. Après cette minute, l'arduino éteind la diode et les capteurs puis se remet en mode veille. L'enregistrement des données sur la carte SD ne commence pas directement car il faut laisser le temps au capteur SDS011 de se stabiliser (poussières non ventilées à l'intérieur notamment).

Axes de progression: 
- Monter se système dans une station météo complète.
- via un shield wifi, envoyer les données directement sur une adresse ip.
- installer éventuellement une antenne gps interne pour avoir une info de la localisation plus précise.

Librairies employées:
-SPI.h
-SD.h
-SDS011.h
-DHT.h
-DS3231.h
-Lowpower.h
-Wire.h

dans le téléchargement on trouve le schema fritzing de montage, le programme arduino, le script python pour traiter les données et afficher les courbes des variables, un exemple d affichage python, un échantillon de mes données en fichier csv. Il y a aussi deux photo du boitier (le design n'est pas trop optimisé mais bon).

