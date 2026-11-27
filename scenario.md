# Scénario de démonstration — Administration et réservation

## 1. Connexion administrateur

Se connecter avec le compte administrateur fourni dans les données initiales.

**POST** `http://localhost:3004/login`

```json
{
  "id": "nestor_teissier"
}
```

Conserver le `access_token` renvoyé : il sera utilisé dans les appels au service User.

## 2. Vérifier les droits sur la liste des utilisateurs

Avec le token administrateur :

**GET** `http://localhost:3004/json`  
`Authorization: Bearer <TOKEN_ADMIN>`

La requête doit retourner la liste des utilisateurs.

## 3. Vérifier qu’un utilisateur normal ne peut pas lister les utilisateurs

Créer un compte de démonstration :

**POST** `http://localhost:3004/user/patrice_braud`  
`Authorization: Bearer <TOKEN_ADMIN>`

```json
{
  "id": "patrice_braud",
  "name": "Patrice Braud"
}
```

Se connecter avec ce compte :

**POST** `http://localhost:3004/login`

```json
{
  "id": "patrice_braud"
}
```

Avec le token obtenu, essayer de lister les utilisateurs :

**GET** `http://localhost:3004/json`  
`Authorization: Bearer <TOKEN_CLIENT>`

Résultat attendu : **401 Unauthorized**.

Le client peut toutefois consulter son propre profil :

**GET** `http://localhost:3004/user/patrice_braud`  
`Authorization: Bearer <TOKEN_CLIENT>`

## 4. Consulter les films et leurs acteurs

Lister le catalogue :

**POST** `http://localhost:3001/graphql`

```graphQL
query{
  movies {
    title
    rating
    actors{
      firstname
      lastname
      birthyear
    }
  }
}
```

Consulter un film et ses acteurs :

**POST** `http://localhost:3001/graphql`

```graphQL
query{
  movie_with_id(_id:"82347feb-58f0-4938-b651-a9dfaa04eefb") {
    title
    rating
    actors{
      firstname
      lastname
      birthyear
    }
  }
}
```

## 5. Ajouter, modifier puis supprimer un film de démonstration

Ajouter un film :

**POST** `http://localhost:3001/graphql`

```graphQL
mutation{
    add_movie(_title:"The Dark Knight", _director: "Christopher Nolan", _rating: 0.9){
		id
        title
        rating
		director
	}
}
```

Modifier sa note :

**POST** `http://localhost:3001/graphql`

```graphQL
mutation{
    update_movie_rate(_id:"MOVIE_ID", _rate: 9.1){
		id
        title
        rating
		director
	}
}
```

Supprimer le film de démonstration :

**POST** `http://localhost:3001/graphql`

```graphQL
mutation{
    delete_movie(_id:"MOVIE_ID"){
		success
        message
	}
}
```

## 6. Ajouter une séance à l’emploi du temps

`localhost:3002 Schedule/CreateSchedule`

```json
{
  "date": "20261127",
  "movie": "e1f3c8a2-4b5d-4c6e-9f1a-2b3c4d5e6f7g"
}
```

Vérifier l’emploi du temps de cette date :

`localhost:3002 Schedule/GetScheduleByDate`

```json
{
  "date": "20261127"
}
```

## 7. Réserver la séance comme client

**POST** `http://localhost:3003/graphql`

```graphQL
mutation AddBooking($userid: String!, $date: String!, $movie_id: String!) {
	add_booking(_userid: $userid, _date: $date, _movie_id: $movie_id) {
		userid dates {
			date
			movies
		}
	}
}
```

Variables :

```json
{
  "userid": "patrice_braud",
  "date": "20261128",
  "movie_id": "e1f3c8a2-4b5d-4c6e-9f1a-2b3c4d5e6f7g"
}
```

## 8. Vérifier la réservation

**POST** `http://localhost:3003/graphql`

```graphQL
{
	booking_with_userid(_userid: "patrice_braud"){
		userid,
  	    dates{
			date
            movies
		}
	}
}
```
