# UE-AD-A1-MIXTE

Lien du projet : https://helene-coullon.fr/pages/ue-ad-fil-25-26/tp-mixte/

Lien du tutoriel GraphQL : https://helene-coullon.fr/pages/ue-ad-fil-25-26/tuto-graphql/

# Description

Ce projet est une petite application permettant de gérer une salle de cinéma, et les réservations des utilisateurs. Il s’agit d’une application jouet et peu réaliste.

Cette application est composée de 4 micro-services :

**Movie** est le micro-service responsable de la gestion des films du cinéma. Il contient et gère une petite base de données json contenant la liste des films disponibles avec quelques informations sur les films.

**Schedule** est le micro-service responsable des jours de passage des films dans le cinéma. Il contient et gère une petite base de données json contenant la liste des dates avec l’ensemble des films disponibles à cette date.

**Booking** est le micro-service responsable de la réservation des films par les utilisateurs. Il contient et gère une petite base de données json contenant une entrée par utilisateur avec la liste des dates et films réservés. Booking fait appel à Schedule pour connaître et vérifier que les créneaux réservés existent bien puisqu’il ne connait pas lui-même les créneaux des films.

**User** est le micro-service est le micro-service qui servirait typiquement à authentifier les utilisateurs. Il contient et gère une petite base de données json avec la liste des utilisateurs.

# Appels API

Les services utilisent les ports suivants :

| Service  | URL locale              |
| -------- | ----------------------- |
| Movie    | `http://localhost:3201` |
| Schedule | `http://localhost:3202` |
| Booking  | `http://localhost:3203` |
| User     | `http://localhost:3204` |

Toutes les données sont échangées au format JSON, sauf la page d'accueil des services qui retourne du HTML.

## User

## Movie

Récupérer la liste de tous les films
Récupérer un film par son identifiant
Créer un film
Mettre à jour la notation d'un film
Mettre à jour le titre d'un film
Mettre à jour le directeur d'un film
Supprimer un film avec son identifiant

## Schedule

## Booking

# Aide

## Windows

```bash
python3 -m venv venv
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
cd .\movie\
pymon movie.py
```
