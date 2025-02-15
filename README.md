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

Les dépendances Python requises sont :

asgiref==3.8.1 Django==5.1.3 pillow==11.0.0 sqlparse==0.5.2 tzdata==2024.2

### 2. Cloner le projet

Ouvrez un terminal et exécutez :

```sh
git clone https://github.com/Jeremuller/OCS_Projet_8.git
```

### 3. Création et activation de l’environnement virtuel

L'utilisation d'un environnement virtuel permet d'isoler les dépendances du projet des autres installations Python sur votre machine.

### Sur Windows :

#### Création de l'environnement virtuel:

```sh
cd OCS_Projet_8
python -m venv env
```

#### Activation de l'environnement virtuel: 

- Si vous utilisez **cmd** : 
```sh
env\Scripts\activate
```

- Si vous utilisez **PowerShell** : 

```sh
env\Scripts\Activate.ps1
```

**Si PowerShell affiche une erreur concernant les permissions (execution policy), exécutez la commande suivante avant d’activer l’environnement** :

```sh
Set-ExecutionPolicy Unrestricted -Scope Process
```

### Sur macOS/Linux :

#### Création de l'environnement virtuel:

```sh
cd OCS_Projet_8
python3 -m venv env
```

#### Activation de l'environnement virtuel: 

- Si vous utilisez **cmd** : 
```sh
source env/bin/activate
```

Une fois activé, vous verrez (env) s’afficher avant le chemin dans votre terminal, indiquant que l’environnement est bien actif.

### 4. Installation des dépendances

Installez les packages requis via **pip** :

```sh
pip install -r requirements.txt
```

### 5. Configuration de la base de données

Avant d’exécuter les migrations, assurez-vous que toutes les migrations nécessaires ont été générées :

```sh
python manage.py makemigrations
```

Ensuite, appliquez-les avec:

```sh
python manage.py migrate
```

Ensuite, appliquez-les avec:

```sh
python manage.py migrate
```

Vous pouvez également créer un super-utilisateur pour accéder à l’administration :

```sh
python manage.py createsuperuser
```

### 6. Lancement du serveur

Une fois la base de données configurée, vous pouvez démarrer le serveur Django avec la commande suivante :

```sh
python manage.py runserver
```

Cliquez sur le lien pour accéder à l'application.

