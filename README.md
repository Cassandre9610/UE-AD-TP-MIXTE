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
| Movie    | `http://localhost:3001` |
| Schedule | `http://localhost:3002` |
| Booking  | `http://localhost:3003` |
| User     | `http://localhost:3004` |

Toutes les données sont échangées au format JSON, sauf la page d'accueil des services qui retourne du HTML.

## User — port 3004

Ce service nécessite un **token d'identification**

| Méthode  | Route                            | Description                                 | Permissions nécessaires    |
| -------- | -------------------------------- | ------------------------------------------- | -------------------------- |
| `GET`    | `/json`                          | Retourne tous les utilisateurs              | admin                      |
| `GET`    | `/user/{userid}`                 | Retourne un utilisateur par son identifiant | utilisateur concerné/admin |
| `GET`    | `/user/name/{username}`          | Retourne un utilisateur par son nom exact   | utilisateur concerné/admin |
| `PUT`    | `/user/{userid}/name/{new_name}` | Modifie le nom d'un utilisateur             | utilisateur concerné/admin |
| `POST`   | `/user/{userid}`                 | Crée un utilisateur                         | publique                   |
| `DELETE` | `/user/{userid}`                 | Supprime un utilisateur                     | utilisateur concerné/admin |
| `POST`   | `/login`                         | Renvoie un token d'identification           | publique                   |

Objet utilisateur :

```json
{
  "id": "chris_rivers",
  "name": "Chris Rivers",
  "last_active": 1360031010
}
```

Exemples :

```bash
curl http://localhost:3004/json
curl http://localhost:3004/user/chris_rivers
curl -X DELETE http://localhost:3004/user/chris_rivers
curl -X POST http://localhost:3004/login --data '{"id": "chris_rivers"}'
```

## Movie — port 3001

Service GraphQL

**Endpoint :** `POST` `/graphql`

### Types

**Actor :**

```json
{
    "id": "actor3",
        "firstname": "Alain",
        "lastname": "Chabat",
        "birthyear": 1958,
        "films": [
            "96798c08-d19b-4986-a05d-7da856efb697",
            ...
        ]
}
```

**Movie :**

```json
{
    "id": "96798c08-d19b-4986-a05d-7da856efb697",
    "title": "Test",
    "director": "Someone",
    "rating": 1.2,
    "actors": [
        {
            "id": "actor3",
            ...
        },
        ...
    ]
}
```

**DeleteResponse :**

```json
{
  "success": true,
  "message": "Movie removed successfully"
}
```

### Requêtes

| Type     | Requête                                                            | Retour         |
| -------- | ------------------------------------------------------------------ | -------------- |
| query    | movies                                                             | \[Movie\]      |
| query    | movie_with_id(\_id: String!)                                       | Movie          |
| query    | movie_with_title(\_title: String!)                                 | Movie          |
| query    | actor_with_id(\_id: String!)                                       | Actor          |
| mutation | add_movie(\_title: String!, \_director: String!, \_rating: Float!) | Movie          |
| mutation | update_movie_rate(\_id: String!, \_rate: Float!)                   | Movie          |
| mutation | update_movie_title(\_id: String!, \_title: String!)                | Movie          |
| mutation | update_movie_director(\_id: String!, \_director: String!)          | Movie          |
| mutation | delete_movie(\_id: String!)                                        | DeleteResponse |

## Schedule — port 3002

Service gRPC

### Types

**Date :**

```json
{
  "date": "20151130"
}
```

**Dates :**

```json
{
    "date": [
        "20151130",
        ...
    ]
}
```

**NewSchedule :**

```json
{
  "date": "20151130",
  "movie": "720d006c-3a57-4b6a-b18f-9b713b073f3c"
}
```

**MovieID :**

```json
{
  "id": "720d006c-3a57-4b6a-b18f-9b713b073f3c"
}
```

**Day :**

```json
{
    "date": "20151130",
    "movies": [
        "720d006c-3a57-4b6a-b18f-9b713b073f3c",
        ...
    ]
}
```

**Schedules :**

```json
{
    "date": "20151130",
    "movies": [
        Day
    ]
}
```

### Requêtes

| Requête                          | Réponse   |
| -------------------------------- | --------- |
| GetSchedule()                    | Schedules |
| CreateSchedule(NewSchedule)      | Day       |
| GetScheduleByDate(Date)          | Day       |
| GetDatesByMovieId(MovieID)       | Dates     |
| DeleteScheduleByDate(Date)       | Schedules |
| DeleteMovieFromDate(NewSchedule) | Day       |

Lors de la création d'un emploi du temps, Schedule vérifie auprès du service Movie que l'identifiant du film existe.

## Booking — port 3003

Service GraphQL

**Endpoint :** `POST` `/graphql`

### Types

**Booking :**

```json
{
  "userid": "chris_rivers",
  "dates": [
    {
      "date": "20151201",
      "movies": [
        "267eedb8-0f5d-42d5-8f43-72426b9fb3e6",
        ...
      ]
    }
  ]
}
```

**Schedule :**

```json
{
  "date": "20151201",
  "movies": [
    "267eedb8-0f5d-42d5-8f43-72426b9fb3e6",
    ...
  ]
}
```

### Requêtes

| Type     | Requête                                                                        | Retour      |
| -------- | ------------------------------------------------------------------------------ | ----------- |
| query    | `booking_with_userid(_userid: String!)`                                        | `Booking`   |
| query    | `booking_with_date(_date: String!)`                                            | `[Booking]` |
| query    | `booking_with_movie(_movie_id: String!)`                                       | `[Booking]` |
| query    | `movies_with_userid_and_date(_user_id: String!, _date: String!)`               | `[String]`  |
| mutation | `add_booking(_userid: String!, _date: String!, _movie_id: String!)`            | `Booking`   |
| mutation | `delete_movie_from_date(_userid: String!, _date: String!, _movie_id: String!)` | `Booking`   |
| mutation | `delete_user_from_booking(_userid: String!)`                                   | `Booking`   |

Lors de l'ajout d'une réservation, Booking vérifie auprès du service Schedule que le film est bien prévu à la date demandée.

## Formats et erreurs

### REST

Les erreurs sont retournées sous cette forme :

```json
{
  "error": "User ID not found"
}
```

### GraphQL

Le type DeleteResponse est utilisé, sinon une erreur GraphQLError est levée

### gRPC

Utilisation des erreurs gRPC avec les codes correspondants (NOT_FOUND, INVALID_ARGUMENT...)

# Aide

## Windows

```bash
python3 -m venv venv
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
cd .\movie\
pymon movie.py
```
