"""
Module de gestion de la base de données SQLite pour Sport Manager
Contient les fonctions de connexion et de création des tables
"""

import sqlite3


def get_connection():
    """
    Crée et retourne une connexion à la base de données SQLite
    """
    conn = sqlite3.connect('sport_manager.db')
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par leur nom
    return conn


def create_tables():
    """
    Crée toutes les tables nécessaires pour l'application selon le MCD
    Tables principales : Equipe, Joueurs, Poste, Competence, Rencontre, Blessure
    Tables de liaison : Joueur_rencontre, Rencontre_equipe, Joueur_competence, Poste_competence
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table Equipe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Equipe (
            id_equipe INTEGER PRIMARY KEY AUTOINCREMENT,
            nom VARCHAR(100) NOT NULL,
            effectif_principal SMALLINT,
            nom_coach VARCHAR(100),
            prenom_coach VARCHAR(60)
        )
    """)
    
    # Table Poste
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Poste (
            id_poste INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_poste VARCHAR(100) NOT NULL
        )
    """)
    
    # Table Competence
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Competence (
            id_competence INTEGER PRIMARY KEY AUTOINCREMENT,
            nom VARCHAR(255) NOT NULL
        )
    """)
    
    # Table Joueurs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Joueurs (
            id_joueur INTEGER PRIMARY KEY AUTOINCREMENT,
            id_equipe INTEGER NOT NULL,
            nom VARCHAR(100) NOT NULL,
            prenom VARCHAR(50),
            id_poste INTEGER NOT NULL,
            statut TEXT CHECK(statut IN ('présent', 'absent')) DEFAULT 'présent',
            FOREIGN KEY (id_equipe) REFERENCES Equipe(id_equipe),
            FOREIGN KEY (id_poste) REFERENCES Poste(id_poste)
        )
    """)
    
    # Table Rencontre
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Rencontre (
            id_rencontre INTEGER PRIMARY KEY AUTOINCREMENT,
            date_match DATETIME,
            lieu VARCHAR(255),
            commentaires TEXT
        )
    """)
    
    # Table Blessure
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Blessure (
            id_blessure INTEGER PRIMARY KEY AUTOINCREMENT,
            id_joueur INTEGER NOT NULL,
            matchs_restants INTEGER DEFAULT 0,
            notes_description TEXT,
            FOREIGN KEY (id_joueur) REFERENCES Joueurs(id_joueur)
        )
    """)
    
    # Table de liaison : Joueur_rencontre
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Joueur_rencontre (
            id_rencontre INTEGER NOT NULL,
            id_joueur INTEGER NOT NULL,
            note_performance INTEGER,
            PRIMARY KEY (id_rencontre, id_joueur),
            FOREIGN KEY (id_rencontre) REFERENCES Rencontre(id_rencontre),
            FOREIGN KEY (id_joueur) REFERENCES Joueurs(id_joueur)
        )
    """)
    
    # Table de liaison : Rencontre_equipe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Rencontre_equipe (
            id_rencontre INTEGER NOT NULL,
            id_equipe INTEGER NOT NULL,
            score SMALLINT,
            PRIMARY KEY (id_rencontre, id_equipe),
            FOREIGN KEY (id_rencontre) REFERENCES Rencontre(id_rencontre),
            FOREIGN KEY (id_equipe) REFERENCES Equipe(id_equipe)
        )
    """)
    
    # Table de liaison : Joueur_competence
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Joueur_competence (
            id_joueur INTEGER NOT NULL,
            id_competence INTEGER NOT NULL,
            niveau SMALLINT CHECK(niveau >= 0 AND niveau <= 100),
            PRIMARY KEY (id_joueur, id_competence),
            FOREIGN KEY (id_joueur) REFERENCES Joueurs(id_joueur),
            FOREIGN KEY (id_competence) REFERENCES Competence(id_competence)
        )
    """)
    
    # Table de liaison : Poste_competence
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Poste_competence (
            id_poste INTEGER NOT NULL,
            id_competence INTEGER NOT NULL,
            niveau_requis SMALLINT,
            PRIMARY KEY (id_poste, id_competence),
            FOREIGN KEY (id_poste) REFERENCES Poste(id_poste),
            FOREIGN KEY (id_competence) REFERENCES Competence(id_competence)
        )
    """)
    
    conn.commit()
    conn.close()
