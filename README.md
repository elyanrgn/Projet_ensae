# Projet DataScience ENSAE Paris

## Résumé du projet

Notre projet a pour objectif de prédire le résultat d'un championnat de football grâce aux matchs des saisons précédentes. Pour ce faire, nous utiliserons des méthodes de scraping afin de récupérer les données du championnat. Après avoir mis en forme les données collectées, nous afficherons une partie de notre base de données. Par la suite, grâce à une méthode de machine learning, nous essaierons de prédire le championnat en cours.

## I - Le scraping

### 1 - Le choix du site à scraper

Pour nous simplifier cette étape, nous avons choisi le championnat anglais *Premier League*. Ce dernier étant le plus réputé, c'est aussi le championnat avec le plus de statistiques.

De nombreux sites proposent des statistiques sur le football. Cependant, peu sont gratuits. De plus, parmi les quelques sites avec des données en libre accès, ces dernières ne sont pas «scrapables» facilement (i.e. avec *bs4*) car elles chargent dynamiquement les données.

Nous avons cependant trouvé un site répondant à nos demandes : [https://fbref.com/fr/](https://fbref.com/fr/)

### 2 - Le choix des données à scraper

Nous avons décidé de scraper, dans un premier temps, les calendriers du championnat depuis la saison 2016-2017 afin d'obtenir beaucoup de données, dans le but d'entraîner un modèle de ML.

Pour ce faire, nous utilisons le module Python *BeautifulSoup*, et nous récupérons le tableau présent sur la page :  
[https://fbref.com/fr/comps/9/2016/calendrier/Calendrier-et-resultats-2016-Premier-League](https://fbref.com/fr/comps/9/2016/calendrier/Calendrier-et-resultats-2016-Premier-League)

## II - Traitement des données récupérées

### 1 - Le choix de notre format de données

Le choix du format de nos données a été l’une des questions cruciales de notre projet. En effet, comme nous avons pour objectif d'entraîner un algorithme de ML, ce choix est primordial !

Nous avons beaucoup hésité, mais finalement, après quelques recherches pour faire le bon choix, nous sommes partis sur le format suivant : un *dataframe* indexé par le temps, afin de pouvoir dégager des tendances temporelles (cette partie n'a que très peu été exploitée par souci de temps). Nous aurons trois *features* principales (nous en développerons d’autres plus tard) : l’équipe à domicile, l’équipe à l’extérieur et le gagnant (1 si domicile, 0 si nul, -1 si extérieur). Ces colonnes seront respectivement nommées **Domicile**, **Extérieur** et **winner**.

### 2 - Traitement des données collectées

Malheureusement, les données que nous récupérons par scraping sont bien différentes du format que nous souhaitons. En effet, il y a des lignes vides à supprimer et des valeurs manquantes à compléter.

Une fois cela fait, nous pouvons travailler notre jeu de données afin de n'avoir que ce que nous voulons. Nous supprimons donc la colonne **Tribune**, car elle est redondante avec la colonne indiquant l’équipe à domicile. Nous supprimons la colonne **Arbitre**, car nous supposons qu’il n’influence pas la rencontre (et nous excluons l’hypothèse de la triche). Nous supprimons les colonnes **Affluence**, **Notes**, **xG**, **xG.1**, car on ne peut les connaître qu’une fois le match joué, ce qui ne nous intéresse pas. Nous créons ensuite la colonne **winner** à partir de la colonne **score**, puis nous supprimons cette dernière.

### 3 - Visualisation des données

Voici nos données collectées et traitées. Nous avons environ 3200 lignes. Nous cherchons donc à les afficher afin de déceler d’éventuelles tendances.

Pour ce faire, nous affichons d'abord les résultats de chaque club à domicile et à l'extérieur durant toutes les saisons. Nous calculons ensuite la probabilité qu'une équipe gagne, perde ou fasse un nul à domicile et à l'extérieur pour chaque club.

Enfin, nous affichons, pour chaque saison, la répartition des victoires à domicile entre tous les clubs.

Ces visualisations montrent, comme on pouvait s’y attendre, que certains clubs dominent tandis que d'autres essuient de nombreuses défaites.

## III - Entraînement du modèle de ML

### 1 - Création de nouvelles features

Il paraît difficile de prédire quoi que ce soit avec seulement ces trois colonnes. En effet, nous obtenons une accuracy de 0.52 lors de l'entraînement de notre modèle sur ce jeu de données minimal.

Nous devons donc créer de nouvelles *features* afin d'améliorer notre modèle. Pour ce faire, nous souhaitons d'abord faire apparaître cet aspect de domination de certains clubs, en créant une variable représentant le nombre de points d'un club à chaque instant de la saison. Nous créons donc deux colonnes : **Cumul_Points_Dom** et **Cumul_Points_Ext**, qui indiquent le nombre de points de l'équipe à domicile et à l'extérieur.

Nous décidons ensuite d'ajouter une sorte de *moving average*, afin de capter la forme d’une équipe. Pour ce faire, nous récupérons le nombre de points gagnés sur les cinq derniers matchs.

Afin de pouvoir travailler avec des API, nous décidons de solliciter l’avis d’un LLM sur l’issue de chaque match et de nous donner un score entre -1 et 1 (-1 pour une victoire de l’équipe à l’extérieur, 0 pour un nul, 1 pour une victoire de l’équipe à domicile). Pour cela, nous utilisons *HuggingFace* et le modèle **mistralai/Mistral-7B-Instruct-v0.3**. Nous choisissons ce modèle de LLM car c’est le meilleur accessible gratuitement sur HuggingFace. Nous avons droit à 1000 requêtes par jour, nous divisons donc le travail en 4 fois.

### 2 - Choix et entraînement du modèle de ML

Nous ne disposons pas d'assez de données pour entraîner un LSTM. Nous avons donc le choix entre un **XGBoost** et un **RandomForest**. Comme le modèle XGBoost est généralement plus performant (selon les compétitions Kaggle), nous choisissons le premier.

Pour l’hyper-tuning du modèle, nous utilisons le module *optuna*. Grâce à toutes ces nouvelles *features*, nous obtenons une précision (*accuracy*) de 0.69 sur l'entraînement, ce qui est nettement mieux que le résultat initial.

## IV - Améliorations futures

Par souci de temps, nous n'avons pas pu explorer et implémenter toutes nos idées. Nous proposons ici quelques pistes d'amélioration de notre projet.

### 1 - Toujours plus de features !

On peut imaginer de nombreuses autres *features*. Par exemple, la valeur des clubs, la moyenne d'âge des joueurs ou encore le temps depuis lequel l'entraîneur est au club.

Ces données sont facilement accessibles à une date T, mais les récupérer pour chaque semaine de chaque saison est une tâche plus difficile.

### 2 - Tester d'autres modèles

Nous pourrions tester un modèle de *RandomForest*, ou collecter plus de données afin d’utiliser un LSTM.

### 3 - Backtester

Afin de vérifier la validité de notre modèle, nous pourrions le valider par *backtesting*, ce qui nous donnerait une approximation plus réaliste de l’efficacité de notre approche.

## V- Détails techniques.

Le projet est composé de 4 documents pythons. Le premier *Scraping_des_donnees* permet de récupérer les données sur internet, et crée tous les fichiers csv, sauf celui commençant par TRAIN

Le second *visualisation_donnees*, permet, comme son nom l'indique, de visualiser nos données collectées.

Le troisième *enrichissement_donnees* permet de créer les nouvelles features, et le csv TRAIN, qui a ces nouvelles features

Finalement le dernier *prediction* est l'entrainement de notre modèle XGBoost.


---

Merci de votre attention,

**Louis Duvail,  
Elyan Rougon**

Objectif du Projet
L'objectif de notre projet est de prédire les résultats d'un championnat de football, en particulier la Premier League anglaise, à partir des données historiques des matchs des saisons précédentes. Pour cela, nous avons adopté une approche méthodologique structurée incluant le scraping de données, le traitement et l’enrichissement des données, la visualisation, et enfin l’entraînement d’un modèle de machine learning (ML).

⚙️ I - Le Scraping des Données
1. Choix du site à scraper
Le choix de la Premier League anglaise s’est imposé naturellement en raison de sa popularité mondiale, de la richesse de ses statistiques, et de la disponibilité des données historiques.

Après une analyse comparative de plusieurs plateformes, nous avons retenu FBref, un site gratuit, fiable et suffisamment structuré pour permettre un scraping efficace avec BeautifulSoup.

2. Collecte des données des matchs
Nous avons ciblé les calendriers des matchs depuis la saison 2016-2017 jusqu'à la saison actuelle. Les informations principales récupérées incluent :

Équipe à domicile
Équipe à l’extérieur
Résultat final du match
Les données ont été extraites via le module Python BeautifulSoup et sauvegardées sous forme de fichiers CSV pour faciliter leur exploitation future.

🛠️ II - Traitement des Données Récupérées
1. Structuration des données
Pour préparer les données à l’entraînement d’un modèle de machine learning, nous avons structuré nos fichiers CSV en un DataFrame indexé par le temps. Chaque ligne représente un match et inclut :

Domicile : Nom de l'équipe jouant à domicile
Extérieur : Nom de l'équipe jouant à l’extérieur
Winner : Variable cible (1 = victoire domicile, 0 = nul, -1 = victoire extérieur)
Ce format permet d’analyser les tendances temporelles, bien que cette dimension temporelle n'ait pas été pleinement exploitée par manque de temps.

2. Nettoyage et transformation des données
Les données brutes présentaient plusieurs anomalies :

Lignes vides et valeurs manquantes : Supprimées ou imputées lorsque cela était possible.
Colonnes non pertinentes : Suppression des colonnes telles que Tribune, Arbitre, Affluence, Notes, xG, car elles ne sont pas disponibles avant un match et ne contribuent pas à la prédiction.
Création de la colonne Winner : À partir du score du match, nous avons dérivé une variable binaire représentant le résultat du match.
3. Visualisation des données
Nous avons utilisé des graphiques pour mieux comprendre les tendances :

Performances domicile/extérieur : Probabilité qu'une équipe gagne, perde ou fasse match nul selon le lieu du match.
Analyse par saison : Répartition des victoires à domicile entre tous les clubs.
Ces visualisations ont confirmé des tendances évidentes, telles que la domination récurrente de certains clubs et les difficultés chroniques d’autres équipes.

🤖 III - Entraînement du Modèle de Machine Learning
1. Enrichissement des données : Création de nouvelles features
Pour améliorer la précision de notre modèle, nous avons ajouté plusieurs nouvelles features :

Cumul_Points_Dom & Cumul_Points_Ext : Nombre de points accumulés par chaque équipe à domicile et à l'extérieur au fil de la saison.
Forme actuelle (Moving Average) : Moyenne mobile des points gagnés sur les 5 derniers matchs.
Score prédictif LLM : Utilisation du modèle Mistral-7B-Instruct-v0.3 via l’API HuggingFace pour prédire un score subjectif de -1 à 1 pour chaque match.
Ces variables supplémentaires ont permis d'apporter un contexte plus riche et pertinent à notre modèle.

2. Choix et entraînement du modèle
Compte tenu de la taille relativement modeste de notre jeu de données, un modèle LSTM (Long Short-Term Memory) n’était pas adapté. Nous avons comparé :

RandomForest
XGBoost
Le modèle XGBoost a été retenu en raison de ses performances robustes et sa capacité à gérer des données hétérogènes.

Hyperparameter Tuning
Nous avons optimisé les hyperparamètres du modèle à l'aide de Optuna, un framework puissant pour le tuning automatique.

3. Résultats du modèle
Après entraînement, le modèle XGBoost a atteint une accuracy de 0.69, une nette amélioration par rapport aux 0.52 initiaux obtenus avec les features basiques.

🚀 IV - Pistes d’Amélioration Futures
1. Création de nouvelles features
Intégration de la valeur marchande des équipes.
Analyse de la moyenne d'âge des joueurs.
Inclusion du temps passé par l'entraîneur au club.
Ces données, bien que disponibles, nécessitent un travail supplémentaire pour être alignées temporellement.

2. Exploration d'autres modèles
Tester des modèles comme RandomForest avec une optimisation plus poussée.
Collecter plus de données pour permettre l’utilisation d’un LSTM.
3. Backtesting
Un backtesting rigoureux permettrait de valider la robustesse du modèle dans des conditions réelles et de mieux comprendre ses performances.

💻 V - Détails Techniques du Projet
Le projet est structuré autour de 4 scripts Python principaux :

Scraping_des_donnees.py : Collecte les données brutes via web scraping et crée les fichiers CSV nécessaires.
Visualisation_donnees.py : Affiche les tendances et statistiques clés à partir des données collectées.
Enrichissement_donnees.py : Crée de nouvelles features et génère un fichier TRAIN.csv enrichi.
Prediction.py : Entraîne le modèle XGBoost et réalise les prédictions finales.
🏁 Conclusion
Ce projet démontre l’efficacité d’une approche méthodologique structurée alliant scraping web, traitement de données avancé et machine learning pour prédire les résultats d'un championnat. Bien que perfectible, notre modèle offre des perspectives prometteuses pour une prédiction de plus en plus précise.

N’hésitez pas à poser des questions ou proposer des suggestions pour améliorer notre approche ! 🚀⚽
