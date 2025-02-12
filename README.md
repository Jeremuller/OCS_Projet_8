# LITRevu - Plateforme de Critiques Littéraires

LITRevu est une plateforme permettant aux utilisateurs de publier des demandes de critiques littéraires (tickets) et de rédiger des critiques sur des livres. Chaque utilisateur peut également suivre d'autres membres pour voir leurs publications et critiques.

---

## Fonctionnalités

- **Création de tickets** : Demandez une critique sur un livre en publiant un ticket.
- **Publication de critiques** : Rédigez des critiques sur des livres ou répondez aux tickets d'autres utilisateurs.
- **Suivi d’utilisateurs** : Abonnez-vous à d’autres membres pour voir leurs publications.
- **Fil d’actualités** : Consultez les critiques et tickets des utilisateurs que vous suivez.
- **Gestion de profil** : Inscrivez-vous, connectez-vous et gérez vos abonnements.

---

## Installation et Lancement en Local

### 1. Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.8+** : [Télécharger ici](https://www.python.org/downloads/)
- **Git** : [Télécharger ici](https://git-scm.com/)
- **Virtualenv** (optionnel mais recommandé)

Les dépendances Python requises sont :

asgiref==3.8.1 Django==5.1.3 pillow==11.0.0 sqlparse==0.5.2 tzdata==2024.2

### 2. Cloner le projet

Ouvrez un terminal et exécutez :

```sh
git clone https://github.com/Jeremuller/OCS_Projet_8.git
cd OCS_Projet_8
```

### 3. Création et activation de l’environnement virtuel

#### Sur Windows :

```sh
python -m venv env
env\Scripts\activate
```

### 4. Installation des dépendances

Installez les packages requis via **pip** :

```sh
pip install -r requirements.txt
```

### 5. Configuration de la base de données

Appliquez les migrations Django pour configurer la base de données :

```sh
python manage.py migrate
```

### 6. Lancement du serveur

Une fois la base de données configurée, vous pouvez démarrer le serveur Django avec la commande suivante :

```sh
python manage.py runserver
```

Cliquez sur le lien pour accéder à l'application.

