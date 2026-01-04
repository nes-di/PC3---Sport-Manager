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
    - OL, PSG, OM, RACING : 4 équipes avec 18 joueurs chacune
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Insertion des équipes
    cursor.execute("INSERT INTO Equipe (nom, coach) VALUES (?, ?)", ("OL", "Coach OL"))
    cursor.execute("INSERT INTO Equipe (nom, coach) VALUES (?, ?)", ("PSG", "Coach PSG"))
    cursor.execute("INSERT INTO Equipe (nom, coach) VALUES (?, ?)", ("OM", "Coach OM"))
    cursor.execute("INSERT INTO Equipe (nom, coach) VALUES (?, ?)", ("RACING", "Coach RACING"))
    
    # Récupération des IDs des équipes
    cursor.execute("SELECT id FROM Equipe WHERE nom = 'OL'")
    id_ol = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM Equipe WHERE nom = 'PSG'")
    id_psg = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM Equipe WHERE nom = 'OM'")
    id_om = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM Equipe WHERE nom = 'RACING'")
    id_racing = cursor.fetchone()[0]
    
    # ÉQUIPE 1 : OL - 18 joueurs (11 titulaires + 7 remplaçants)
    joueurs_ol = [
        # === TITULAIRES (11) ===
        ("", "Olivier", "Gardien", 15, 5, 70, 10),
        ("", "Mehdi", "Défenseur Central", 10, 40, 40, 10),
        ("", "Paul", "Défenseur Central", 10, 40, 40, 10),
        ("", "Ousmane", "Arrière Droit", 40, 50, 5, 5),
        ("", "Rayan", "Arrière Gauche", 40, 50, 5, 5),
        ("", "Ilyes", "Milieu Défensif", 10, 40, 40, 10),
        ("", "Abdel", "Milieu Central", 5, 50, 10, 35),
        ("", "Kilyan", "Milieu Central", 5, 50, 10, 35),
        ("", "Evann", "Ailier Gauche", 65, 5, 5, 25),
        ("", "Süleyman", "Ailier Droit", 65, 5, 5, 25),
        ("", "Emre", "Attaquant", 10, 10, 30, 50),
        
        # === REMPLAÇANTS (7) ===
        ("", "Martin", "Remplaçant", 10, 70, 10, 10),
        ("", "Mike", "Remplaçant", 10, 50, 10, 30),
        ("", "Wu", "Remplaçant", 60, 10, 25, 5),
        ("", "Georges", "Remplaçant", 10, 5, 75, 10),
        ("", "Thomas", "Remplaçant", 10, 40, 40, 10),
        ("", "Matthieu", "Remplaçant", 55, 30, 5, 20),
        ("", "Cristiano", "Remplaçant", 30, 15, 15, 40)
    ]
    
    for nom, prenom, poste, vitesse, endurance, force, technique in joueurs_ol:
        cursor.execute("""
            INSERT INTO Joueur (id_equipe, nom, prenom, poste, vitesse, endurance, force, technique, duree_blessure)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (id_ol, nom, prenom, poste, vitesse, endurance, force, technique))
    
    # ÉQUIPE 2 : PSG - 18 joueurs (11 titulaires + 7 remplaçants)
    joueurs_psg = [
        # === TITULAIRES (11) ===
        ("", "Victor", "Gardien", 15, 5, 70, 10),
        ("", "Yanis", "Défenseur Central", 10, 40, 40, 10),
        ("", "Hugo", "Défenseur Central", 10, 40, 40, 10),
        ("", "Ibrahim", "Arrière Droit", 40, 50, 5, 5),
        ("", "Samy", "Arrière Gauche", 40, 50, 5, 5),
        ("", "Kamel", "Milieu Défensif", 10, 40, 40, 10),
        ("", "Nassim", "Milieu Central", 5, 50, 10, 35),
        ("", "Adem", "Milieu Central", 5, 50, 10, 35),
        ("", "Noah", "Ailier Gauche", 65, 5, 5, 25),
        ("", "Amir", "Ailier Droit", 65, 5, 5, 25),
        ("", "Lucas", "Attaquant", 10, 10, 30, 50),
        
        # === REMPLAÇANTS (7) ===
        ("", "Julien", "Remplaçant", 10, 70, 10, 10),
        ("", "Alex", "Remplaçant", 10, 50, 10, 30),
        ("", "Léo", "Remplaçant", 60, 10, 25, 5),
        ("", "Bruno", "Remplaçant", 10, 5, 75, 10),
        ("", "Maxime", "Remplaçant", 10, 40, 40, 10),
        ("", "Enzo", "Remplaçant", 55, 30, 5, 20),
        ("", "Raphaël", "Remplaçant", 30, 15, 15, 40)
    ]
    
    # ÉQUIPE 3 : OM - 18 joueurs (11 titulaires + 7 remplaçants)
    joueurs_om = [
        # === TITULAIRES (11) ===
        ("", "Clément", "Gardien", 15, 5, 70, 10),
        ("", "Bilal", "Défenseur Central", 10, 40, 40, 10),
        ("", "Romain", "Défenseur Central", 10, 40, 40, 10),
        ("", "Moussa", "Arrière Droit", 40, 50, 5, 5),
        ("", "Anis", "Arrière Gauche", 40, 50, 5, 5),
        ("", "Walid", "Milieu Défensif", 10, 40, 40, 10),
        ("", "Youssef", "Milieu Central", 5, 50, 10, 35),
        ("", "Ismaël", "Milieu Central", 5, 50, 10, 35),
        ("", "Ethan", "Ailier Gauche", 65, 5, 5, 25),
        ("", "Farid", "Ailier Droit", 65, 5, 5, 25),
        ("", "Adam", "Attaquant", 10, 10, 30, 50),
        
        # === REMPLAÇANTS (7) ===
        ("", "Antoine", "Remplaçant", 10, 70, 10, 10),
        ("", "Nicolas", "Remplaçant", 10, 50, 10, 30),
        ("", "Kévin", "Remplaçant", 60, 10, 25, 5),
        ("", "Patrick", "Remplaçant", 10, 5, 75, 10),
        ("", "Sébastien", "Remplaçant", 10, 40, 40, 10),
        ("", "Mathis", "Remplaçant", 55, 30, 5, 20),
        ("", "Damien", "Remplaçant", 30, 15, 15, 40)
    ]
    
    # ÉQUIPE 4 : RACING - 18 joueurs (11 titulaires + 7 remplaçants)
    joueurs_racing = [
        # === TITULAIRES (11) ===
        ("", "Benjamin", "Gardien", 15, 5, 70, 10),
        ("", "Rachid", "Défenseur Central", 10, 40, 40, 10),
        ("", "Florian", "Défenseur Central", 10, 40, 40, 10),
        ("", "Hamza", "Arrière Droit", 40, 50, 5, 5),
        ("", "Yacine", "Arrière Gauche", 40, 50, 5, 5),
        ("", "Mehmet", "Milieu Défensif", 10, 40, 40, 10),
        ("", "Karim", "Milieu Central", 5, 50, 10, 35),
        ("", "Ali", "Milieu Central", 5, 50, 10, 35),
        ("", "Mathéo", "Ailier Gauche", 65, 5, 5, 25),
        ("", "Sofiane", "Ailier Droit", 65, 5, 5, 25),
        ("", "Nolan", "Attaquant", 10, 10, 30, 50),
        
        # === REMPLAÇANTS (7) ===
        ("", "Louis", "Remplaçant", 10, 70, 10, 10),
        ("", "Pierre", "Remplaçant", 10, 50, 10, 30),
        ("", "Théo", "Remplaçant", 60, 10, 25, 5),
        ("", "Henri", "Remplaçant", 10, 5, 75, 10),
        ("", "Quentin", "Remplaçant", 10, 40, 40, 10),
        ("", "Baptiste", "Remplaçant", 55, 30, 5, 20),
        ("", "Adrien", "Remplaçant", 30, 15, 15, 40)
    ]
    
    for nom, prenom, poste, vitesse, endurance, force, technique in joueurs_psg:
        cursor.execute("""
            INSERT INTO Joueur (id_equipe, nom, prenom, poste, vitesse, endurance, force, technique, duree_blessure)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (id_psg, nom, prenom, poste, vitesse, endurance, force, technique))
    
    for nom, prenom, poste, vitesse, endurance, force, technique in joueurs_om:
        cursor.execute("""
            INSERT INTO Joueur (id_equipe, nom, prenom, poste, vitesse, endurance, force, technique, duree_blessure)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (id_om, nom, prenom, poste, vitesse, endurance, force, technique))
    
    for nom, prenom, poste, vitesse, endurance, force, technique in joueurs_racing:
        cursor.execute("""
            INSERT INTO Joueur (id_equipe, nom, prenom, poste, vitesse, endurance, force, technique, duree_blessure)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (id_racing, nom, prenom, poste, vitesse, endurance, force, technique))
    
    conn.commit()
    conn.close()
    print("✓ Données de test insérées avec succès")
    print(f"  - {len(joueurs_ol)} joueurs OL")
    print(f"  - {len(joueurs_psg)} joueurs PSG")
    print(f"  - {len(joueurs_om)} joueurs OM")
    print(f"  - {len(joueurs_racing)} joueurs RACING")


if __name__ == "__main__":
    print("=== Initialisation de la base de données ===")
    reset_database()
    insert_seed_data()
    print("=== Initialisation terminée ===")
