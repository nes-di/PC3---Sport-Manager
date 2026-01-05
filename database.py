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
    Crée toutes les tables nécessaires pour l'application
    - Equipe : stocke les équipes (OL, PSG, etc.)
    - Joueur : stocke les joueurs avec leurs stats et leur état de blessure
    - Rencontre : stocke l'historique des matchs
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table Equipe : id, nom, coach
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Equipe (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            coach TEXT
        )
    """)
    
    # Table Joueur : id, id_equipe, nom, poste, stats, duree_blessure
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Joueur (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_equipe INTEGER NOT NULL,
            nom TEXT NOT NULL,
            poste TEXT NOT NULL,
            vitesse INTEGER DEFAULT 0,
            endurance INTEGER DEFAULT 0,
            force INTEGER DEFAULT 0,
            technique INTEGER DEFAULT 0,
            duree_blessure INTEGER DEFAULT 0,
            FOREIGN KEY (id_equipe) REFERENCES Equipe(id)
        )
    """)
    
    # Table Rencontre : id, adversaire, scores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Rencontre (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            adversaire TEXT NOT NULL,
            score_mon_equipe INTEGER NOT NULL,
            score_adversaire INTEGER NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    print("✓ Tables créées avec succès")
