Ce module Python a été construit dans le cadre du projet Actelink. Il est à destination des clients d'Actelink et doit leur permettre d'interroger leur [moteur de variables](https://github.com/fasst/fasst_variable_store) au sein de leurs programmes Python de calcul de tarification.

Le module est très simple, il expose uniquement une méthode `get_variable` permettant de récupérer la valeur d'une variable donnée au sein du moteur. Le but de ce module est uniquement de cacher la logique REST inhérente à la communication avec le moteur de variables.

## Utilisation du module

### Mise en place de l'environnement
Pour tester ce module Python vous aurez besoin de faire tourner un MongoDB sur votre machine. Vous pouvez installer un client GUI tel que [Compass](https://www.mongodb.com/try/download/compass).

Vous aurez également besoin du moteur de variables écrit en Go :
* Installer [Go](https://go.dev/dl/) dans votre environnement 
* Cloner le repo du [moteur](https://github.com/fasst/fasst_variable_store)
* Suivez les indications fournies dans le README du moteur pour configurer le service
* Placer vous à la racine du moteur et tapez `go run main.go`

Et enfin, Python :
* Installer [Python](https://www.python.org/downloads/) dans votre environnement
* Cloner ce repo
* Assurez vous que pip, le gestionnaire de paquets Python, est à jour : `python -m pip install --upgrade pip`
* Installer les packages de tests avec `pip install pytest` et `pip install pytest-runner`
### Configuration
* Dans le fichier *tests/python/server.cfg*, indiquez l'url à laquelle le moteur de variables est accessible, en reprenant la valeur du `SERVICE_HOST` définie dans le fichier *.env* du moteur de variables.
* Vérifiez également que la clé définie dans *tests/python/server.cfg* correspond bien à l'*apikey* définie pour le *customer1* dans *tests/python/data.json*

### Lancer les tests
Pour lancer la suite de test : `pytest`

Le programme de test *tests/python/test_suite.py* va alimenter la base de données *actelink_var_engine* avec le jeu de données décrit dans *tests/python/data.json* en effectuant une série de requêtes POST au moteur de variables.
Vous pouvez vérifier le résultant en consultant la base de données *actelink_var_engine* via MongoDB Compass.

## Générer la documentation du module
* Installer l'outil Sphinx `pip install sphinx`
* Créer un répertoire dédié à la documentation `mkdir doc`
* Placer vous dans ce répertoire et exécutez la commande `sphinx-quickstart`
* Répondez aux questions de configuration de sphinx : *y*, *actelink.variables*, *ACTELINK* puis indiquez la version du projet et indiquez *fr* comme langue de documentation
* Le thème par défaut utilisé par sphinx est assez sommaire, installez le thème *sphinx-rtd-theme* : `pip install sphinx-rtd-theme`
* Dans *doc/source/conf.py*, renseignez la configuration suivante :

```
extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.autodoc'
]
html_theme = 'sphinx_rtd_theme'
```
* Remplacez le contenu de  *doc/source/index.rst*, avec la configuration suivante :

```
Librairie Actelink
==============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


actelink.variables
==================
.. automodule:: actelink.variables
   :members:
```

* Générez la documentation : `./make.bat html` sous Windows, ou `make html` ailleurs
La documentation est générée ici : *doc/build/html/index.html*