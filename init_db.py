"""
Script d'initialisation de la base de données
À lancer une seule fois pour vider les tables et insérer les données de test
"""

from database import get_connection, create_tables


def reset_database():
    """
    Supprime toutes les données existantes et recrée les tables
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Suppression des tables existantes
    cursor.execute("DROP TABLE IF EXISTS Rencontre")
    cursor.execute("DROP TABLE IF EXISTS Joueur")
    cursor.execute("DROP TABLE IF EXISTS Equipe")
    
    conn.commit()
    conn.close()
    
    # Recréation des tables
    create_tables()
    print("✓ Base de données réinitialisée")


def insert_seed_data():
    """
    Insère les données de départ (équipes et joueurs)
    - OL : Mon équipe avec tous les joueurs
    - PSG : Équipe adverse avec quelques joueurs
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Insertion des équipes
    cursor.execute("INSERT INTO Equipe (nom, coach) VALUES (?, ?)", ("OL", "Coach OL"))
    cursor.execute("INSERT INTO Equipe (nom, coach) VALUES (?, ?)", ("PSG", "Coach PSG"))
    
    # Récupération des IDs des équipes
    cursor.execute("SELECT id FROM Equipe WHERE nom = 'OL'")
    id_ol = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM Equipe WHERE nom = 'PSG'")
    id_psg = cursor.fetchone()[0]
    
    # Insertion des joueurs de l'OL (Mon équipe) - 11 joueurs
    joueurs_ol = [
        # Gardien
        ("Olivier", "Olivier", "Gardien", 15, 5, 70, 10),
        # Défenseurs
        ("Mehdi", "Mehdi", "Défenseur Central", 10, 40, 40, 10),
        ("Paul", "Paul", "Défenseur Central", 10, 40, 40, 10),
        ("Thomas", "Thomas", "Défenseur Latéral Droit", 45, 35, 25, 15),
        ("Kevin", "Kevin", "Défenseur Latéral Gauche", 40, 40, 30, 10),
        # Milieux
        ("Abdel", "Abdel", "Milieu Défensif", 5, 50, 10, 35),
        ("Antoine", "Antoine", "Milieu Central", 20, 45, 15, 40),
        ("Maxime", "Maxime", "Milieu Offensif", 30, 30, 10, 50),
        # Attaquants
        ("Evann", "Evann", "Ailier Gauche", 65, 5, 5, 25),
        ("Rayan", "Rayan", "Ailier Droit", 60, 10, 10, 30),
        ("Emre", "Emre", "Attaquant Centre", 10, 10, 30, 50)
    ]
    
    for nom, prenom, poste, vitesse, endurance, force, technique in joueurs_ol:
        cursor.execute("""
            INSERT INTO Joueur (id_equipe, nom, prenom, poste, vitesse, endurance, force, technique, duree_blessure)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (id_ol, nom, prenom, poste, vitesse, endurance, force, technique))
    
    # Insertion des joueurs du PSG (Équipe adverse) - 11 joueurs
    joueurs_psg = [
        # Gardien
        ("Victor", "Victor", "Gardien", 15, 5, 70, 10),
        # Défenseurs
        ("Sergio", "Sergio", "Défenseur Central", 15, 45, 45, 15),
        ("Marquinhos", "Marquinhos", "Défenseur Central", 20, 40, 40, 20),
        ("Achraf", "Achraf", "Défenseur Latéral Droit", 70, 30, 20, 20),
        ("Nuno", "Nuno", "Défenseur Latéral Gauche", 50, 35, 25, 10),
        # Milieux
        ("Marco", "Marco", "Milieu Défensif", 10, 50, 20, 40),
        ("Vitinha", "Vitinha", "Milieu Central", 25, 40, 10, 50),
        ("Warren", "Warren", "Milieu Offensif", 35, 25, 15, 55),
        # Attaquants
        ("Noah", "Noah", "Ailier Gauche", 65, 5, 5, 25),
        ("Ousmane", "Ousmane", "Ailier Droit", 80, 20, 10, 40),
        ("Lucas", "Lucas", "Attaquant Centre", 10, 10, 30, 50)
    ]
    
    for nom, prenom, poste, vitesse, endurance, force, technique in joueurs_psg:
        cursor.execute("""
            INSERT INTO Joueur (id_equipe, nom, prenom, poste, vitesse, endurance, force, technique, duree_blessure)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (id_psg, nom, prenom, poste, vitesse, endurance, force, technique))
    
    conn.commit()
    conn.close()
    print("✓ Données de test insérées avec succès")
    print(f"  - {len(joueurs_ol)} joueurs OL")
    print(f"  - {len(joueurs_psg)} joueurs PSG")


if __name__ == "__main__":
    print("=== Initialisation de la base de données ===")
    reset_database()
    insert_seed_data()
    print("=== Initialisation terminée ===")
