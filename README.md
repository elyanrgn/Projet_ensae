# Projet_ensae

## Résumé du projet

Notre projet a pour objectif de prédire le résultat d'un championnat de football grâce aux matchs des saisons précédents. Pour ce faire
nous utiliserons des méthodes de scrapping afin de récupérer les données du championnat. Après avoir mis en forme les données collectés, nous afficherons une partie de notre base de données. Par la suite, grâce à une méthode de machine learning, nous esseyerons de prédire le championnat en cours.

## I- Le scrapping.

### 1- Le choix du site à scrapper.

Afin de nous simplifier cette étape, nous avons choisi le championnat anglais 'Premier League'. Ce dernier étant le plus réputé, c'est
aussi le championnat avec le plus de statistiques.

De nombreux sites proposent des statistiques sur le football. Cependant, peu sont gratuits. De plus, parmi les quelques sites avec des 
données en libre accès, ces dernières ne sont pas "scrappable" facilement (i.e avec bs4) car elles chargent dynamiquement les chiffres.

Nous avons cependant trouvé un site répondant à nos demandes : https://fbref.com/fr/

### 2- Le choix des données à scrapper

Nous décidons de scrapper, dans un premier temps, les calendriers du championnat depuis la saison 2016-2017 afin d'obtenir beaucoup de données, dans l'objectif d'entrainer un modèle de ML.

Pour ce faire nos utilisons le module python BeautifulSoup, et nous récupérons le tableau présent sur la page : https://fbref.com/fr/comps/9/2016/calendrier/Calendrier-et-resultats-2016-Premier-League

## II - Traitement des données récupérées.

### 1- Le choix de notre format de données.

Une des questions cruciales de notre projet a été le format de nos données. En effet, comme nous avons pour objectif d'entraîner un algorithme de ML, le choix du format est cruciale ! 

Nous avons beaucoup hésité, mais finalement après des recherches afin de faire le bon choix, nous sommes partis sur le format suivant : un dataframe indexé par le temps, afin de pouvoir dégager des tendances temporelles (cette partie n'a que très peu été exploitée par soucis de temps). Nous aurons trois features principales (nous en développeront d'autres plus tard). L'équipe à domicile, l'équipe à l'extérieur, et le gagnant (1 si domicile, 0 si nul, -1 si extérieur). Ces colonnes seront respectivement "Domicile", "Extérieur", et "winner"

### 2- Traitement des données collectées.

Malheuresement, nos données que nous scrappons sont bien différentes du format que nous volons. Déjà, nos données ont des lignes vides qu'il faut supprimer et des valeurs absentes qu'il faut remplir.

Une fois cela fait, nous pouvons travailler notre jeu de données afin de n'avoir que ce que nous voulons. Nous supprimons donc la colonne "Tribune", car nous avons déjà l'équipe à domicile. Nous supprimons la colonne "Arbitre", car nous supposons que l'arbitre n'influe pas la rencontre, et est identique pour chaque match (on exclue la triche). Nous supprimons les colonnes "Affluence","Notes", "xG", "xG.1", car on ne peut les connaître qu'une fois le match joué, ce qui ne nous intéresse pas. Nous créeons ensuite la colonne "winner" grâce à la colonne "score", puis on supprime cette dernière.

### 3- Visualisation des données.

Voilà nos données collectés et traités, nous avons environ 3200 lignes. Nous cherchons donc à les afficher afin de déterminer de potentielles tendances.

Pour ce faire, on affiche d'abord les résultats de chaque club à domicile et à l'extérieur durant toute les saisons. Nous calculons ensuite la probabilité qu'une équipe gagne, perde ou fasse un nul à domicile et à l'extérieur pour chaque club. 

Finalement, on affiche, pour chaque saison, la répartition des victoires à domicile entre tous les clubs.

Ces visualisations permettent, comme il est logique de le croire, de voir que certains club dominent tandis que d'autres accusent de nombreuses défaites.

## III - Entraînement du modèle de ML

### 1- Création de nouvelles features

Il paraît difficilement possible de prédire quoi que ce soit avec seulement ces trois colonnes. Et nous obtenons en effet une accuracy de 0.52 lors de l'entraînement de notre modèle sur ce jeu de données seul.

Nous devons donc créer de nouvelles features afin d'avoir un meilleur modèle. Pour ce faire nous souhaitons d'abord faire apparaître cet aspect de domination de certain club, en créant une feature représentant le nombre de point d'un club à chaque instant de la saison.Nous créeons donc deux colonnes : "Cumul_Points_Dom" et "Cumul_Points_Ext" qui indiquent le nombre de points de l'équipe à domicile et à l'extérieur.

Nous décidons ensuite d'ajouter une sorte de mooving average, afin de capter la forme d'une activité. Pour ce faire nous récupérons le nombre de points gagnés sur les 5 derniers matchs.

Afin de pouvoir travailler avec des API, nous décidons de demander un LLM son avis sur l'issue de chaque match et de nous donner un score entre -1 et 1 (-1 victoire de l'équipe à l'extérieur, 0 un nul, 1 une victoire de l'équipe à domicile). Pour ce faire nous utilisons huggingface, et le modèle "mistralai/Mistral-7B-Instruct-v0.3". Nous choisissons ce modèle de LLM car c'est le meilleur accessible gratuitement sur huggingface. Nous avons le droit à 1000 requêtes par jour, nous divisons donc le travail en 4 fois.

### 2- Choix et entraînement du modèle de ML

Nous avons trop peu de données pour entrainer un LSTM. Nous avons donc le choix entre un XGBoost ou RandomForest. Le modèle XGBoost étant en général plus performant que RandomForest (du moins sur les compétitions Kaggle), nous choisissons le premier.

Pour l'hyppertunning du modèle, nous utilisons le module optuna. Avec toutes ces nouvelles features, nous obtenons une accuracy de 0.69 sur l'entraînement, ce qui est largement mieux que le résultat initial.

## IV - Améliorations futures.

Par soucis de temps, nous n'avons pas pu explorer et implémenter toutes nos idées. On propose ici des pistes d'amélioration de notre projet.

### 1- Toujours plus de features !

On peut imaginer encore de très nombreuses features. Par exemple des features comme la valeur des clubs, la moyenne d'âge des joueurs ou le temps depuis lequel l'entraîneur est au club.

Ces données sont facilement accessibles à une date T, mais les récupérer pour chaque semaine, de chaque saison est une tâche plus difficile.

### 2- Tester d'autres modèles.

Nous pouvons tester un modèle de RandomForest, ou collecter plus de données afin d'utiliser un LSTM.

### 3- Backtester

Afin de vérifier la validité de notre modèle, nous pourrions le backtester afin d'obtenir une "vraie" approximation de l'efficacité de notre modèle


Merci de votre attention

Louis Duvail,
Elyan Rougon
