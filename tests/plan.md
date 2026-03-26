# Plan de test

## Fonctionnalités

### Administration des données (Django admin)

- Ajout d’un site
- Modification d’un site
- Suppression d’un site
- Ajout d’une mission
- Modification d’une mission
- Suppression d’une mission
- Ajout de waypoints
- Modification de waypoints
- Suppression de waypoints

### Consultation via l’application

- Affichage de la liste des sites
- Affichage de la liste des missions
- Affichage du détail d’une mission
- Affichage des waypoints associés à une mission

### Contrôle du drone (préparation Sprint 2)

- Déclenchement d’une mission
- Simulation de suivi de mission
- Affichage des logs de mission

----------------------------------------------------------

## Cas de test

### Administration des données (Django admin)

#### Cas usuels

- Ajouter un site avec des données valides
- Ajouter une mission liée à un site
- Ajouter des waypoints à une mission

#### Cas extrêmes

- Ajouter un site avec des champs très longs
- Ajouter un grand nombre de waypoints

#### Cas d’erreur

- Ajouter un site avec des champs obligatoires vides
- Ajouter une mission sans site associé

---

### Consultation via l’application

#### Cas usuels

- Accéder à la liste des sites
- Accéder à la liste des missions
- Accéder au détail d’une mission

#### Cas extrêmes

- Afficher une mission avec beaucoup de waypoints

#### Cas d’erreur

- Accéder à une mission inexistante
- Accéder à une URL incorrecte

-----------------------------------------------------------

### Contrôle du drone (préparation Sprint 2)

#### Cas usuels

- Déclencher une mission
- Consulter les logs d’une mission

#### Cas extrêmes

- Déclencher plusieurs missions successivement

#### Cas d’erreur

- Déclencher une mission inexistante
- Consulter des logs inexistants

## Déroulement des tests

### Ajouter un site

- Arrangement :
  Se connecter à l’interface admin Django.

- Action :
  Créer un site avec des données valides.

- Assertion :
  Le site est enregistré et visible dans la liste.

---

### Ajouter une mission

- Arrangement :
  Un site existe déjà.

- Action :
  Créer une mission associée à ce site.

- Assertion :
  La mission apparaît dans la liste des missions.

---

### Consulter une mission

- Arrangement :
  Une mission existe.

- Action :
  Accéder à la page de détail de la mission.

- Assertion :
  Les informations de la mission s’affichent correctement.

---

### Ajouter un waypoint

- Arrangement :
  Une mission existe.

- Action :
  Ajouter un waypoint à la mission.

- Assertion :
  Le waypoint est associé à la mission et affiché.

---

### Accéder à une mission inexistante

- Arrangement :
  Utiliser un identifiant invalide.

- Action :
  Accéder à l’URL correspondante.

- Assertion :
  Une erreur 404 est retournée.

---

### Déclencher une mission (simulation)

- Arrangement :
  Une mission existe.

- Action :
  Lancer la mission.

- Assertion :
  La mission passe à un état actif ou en cours.

---

### Consulter les logs

- Arrangement :
  Une mission a généré des logs.

- Action :
  Accéder aux logs.

- Assertion :
  Les logs sont affichés correctement.