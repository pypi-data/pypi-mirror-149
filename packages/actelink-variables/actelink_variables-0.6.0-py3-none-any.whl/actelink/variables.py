#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Le module actelink.variables permet de facilement interroger votre moteur de variables Actelink.

Une variable peut avoir trois types :

* d0 : une clé / valeur 
    Exemple pour une variable *intercept* : intercept=0.8

* d1 : un vecteur de clé / valeur
    Exemple pour une variable *niveau* : low=0.1, medium=0.24, high=0.3

* d2 : une matrice à deux dimensions de clé / valeur
    Exemple pour une variable *situation* : [homme, marié]=0.2, [homme, célibataire]=0.1 [femme, marié]=0.3, [femme, célibataire]=0.2

Une fois initialisé, ce module va se connecter à votre moteur de variables Actelink en utilisant les paramètres de connexion spécifiés.
"""

import requests
import urllib.parse
import warnings

class VarHelpers:
    """ Classe principale du module.

    Pour l'utiliser :

    Installez le module :

    >>> python -m pip install actelink-variables

    Puis importez le dans votre code :

    >>> import actelink.variables as av

    Définir les paramètres de connexion à votre serveur Actelink, par exemple :

    >>> url = "https://prod.actelink.tech:7109"
    >>> key = "6ae2f8cac845f08a"

    Initialiser l'objet VarHelpers :

    >>> vh = av.VarHelpers(url, key)

    Afficher les stores disponibles :

    >>> print(vh.stores)
    ('millesime2021', 'millesime2022')

    # Récupérer la valeur d'une variable :

    >>> intercept = vh.get_variable('millesime2022', 'intercept')
    >>> print(intercept)
    0.893
    """

    __STORES_URI        = '/api/v1/stores'
    __VARIABLES_URI     = '/api/v1/stores/:storeId/variables/:label'
    _stores             = dict()

    def __init__(self, url: str, key: str):
        self.__CUSTOMER_KEY       = key
        self.__BASE_URL           = url
        self.__VARIABLES_ENDPOINT = urllib.parse.urljoin(self.__BASE_URL, self.__VARIABLES_URI)
        # retrieve the list of stores for this customer
        try:
            response = requests.get(urllib.parse.urljoin(self.__BASE_URL, self.__STORES_URI), headers={'api-key': self.__CUSTOMER_KEY})
        except requests.exceptions.ConnectionError as error:
            print(f"CONNECTION FAILED!\n\n{error})")
            raise
        # check response is valid
        if response.status_code != 200:
            raise requests.exceptions.ConnectionError(f'Connection to server failed, reason: {response.reason}')
        elif response.json() is None:
            warnings.warn('Warning: no stores found')
        else:
            for s in response.json():
                self._stores[s['name']] = s['id']
                print(f"found store {s['name']} (id {s['id']})")

    @property
    def stores(self) -> tuple:
        """Retourne les stores existants sous forme d'un tuple."""
        return tuple(self._stores)

    def get_variable(self, context: dict, var_label: str, var_keys: list|str = None) -> float:
        """Retourne la valeur d'une variable dans un contexte donné.

        :param str store_name: Le nom du store dans lequel se trouve la variable.
        :param str var_label: Le nom de la variable à retourner.
        :param str var_keys: La ou les clés à spécifier pour cette variable (None par défaut).
        :type var_keys: str or list or None

        :returns: La valeur de la variable *var_label* pour la/les clé(s) donnée(s) si spécifiée(s).
        :rtype: float
        :raises NameError: si le store donné n'existe pas.

        Exemples d'utilisation :

        * Cas d'une variable d0

        >>> intercept = vh.get_variable('millesime2022', 'intercept')
        >>> print(intercept)
        0.893

        * Cas d'une variable d1
        
        >>> niveau = vh.get_variable('millesime2022', 'niveau', 'medium')
        >>> print(niveau)
        0.24

        * Cas d'une variable d2
        
        >>> situation = vh.get_variable('millesime2022', 'situation', 'homme,celibataire')
        >>> print(situation)
        0.893

        .. NOTE:: Dans le cas d'une variable de type d2, où deux clés doivent être spécifiées, celles ci peuvent être passées en paramètre sous la forme d'une string ou d'une liste :
        
        >>> situation = vh.get_variable('millesime2022', 'situation', 'homme,celibataire')

        est équivalent à :

        >>> situation = vh.get_variable('millesime2022', 'situation', ['homme', 'celibataire'])
        """
        store_name = ".".join(f'{v}' for v in context.values())
        if store_name not in self._stores:
            raise NameError(f'store {store_name} not found')

        print (f'get_variable {var_label} on store {store_name}, requested key: {var_keys}')
        # build url
        url = self.__VARIABLES_ENDPOINT.replace(':storeId', self._stores[store_name]).replace(':label', var_label)
        # var_keys can be passed as a string or array of strings
        var_keys = ','.join(k.strip() for k in var_keys) if isinstance(var_keys, list) else var_keys
        response = requests.get(url, headers={'api-key': self.__CUSTOMER_KEY}, params={'key': var_keys})
        if response.status_code != 200:
            warnings.warn(f'get_variable {var_label} failed, reason: {response.reason}')
            return None
        return float(response.json())
