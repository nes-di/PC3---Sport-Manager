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
        ("Olivier", "Olivier", "Gardien", 15, 5, 70, 10),
        ("Mehdi", "Mehdi", "Défenseur Central", 10, 40, 40, 10),
        ("Paul", "Paul", "Défenseur Central", 10, 40, 40, 10),
        ("Ousmane", "Ousmane", "Arrière Droit", 40, 50, 5, 5),
        ("Rayan", "Rayan", "Arrière Gauche", 40, 50, 5, 5),
        ("Ilyes", "Ilyes", "Milieu Défensif", 10, 40, 40, 10),
        ("Abdel", "Abdel", "Milieu Central", 5, 50, 10, 35),
        ("Kilyan", "Kilyan", "Milieu Central", 5, 50, 10, 35),
        ("Evann", "Evann", "Ailier Gauche", 65, 5, 5, 25),
        ("Süleyman", "Süleyman", "Ailier Droit", 65, 5, 5, 25),
        ("Emre", "Emre", "Attaquant", 10, 10, 30, 50),
        
        # === REMPLAÇANTS (7) ===
        ("Martin", "Martin", "Remplaçant", 10, 70, 10, 10),
        ("Mike", "Mike", "Remplaçant", 10, 50, 10, 30),
        ("Wu", "Wu", "Remplaçant", 60, 10, 25, 5),
        ("Georges", "Georges", "Remplaçant", 10, 5, 75, 10),
        ("Thomas", "Thomas", "Remplaçant", 10, 40, 40, 10),
        ("Matthieu", "Matthieu", "Remplaçant", 55, 30, 5, 20),
        ("Cristiano", "Cristiano", "Remplaçant", 30, 15, 15, 40)
    ]
    
    for nom, prenom, poste, vitesse, endurance, force, technique in joueurs_ol:
        cursor.execute("""
            INSERT INTO Joueur (id_equipe, nom, prenom, poste, vitesse, endurance, force, technique, duree_blessure)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (id_ol, nom, prenom, poste, vitesse, endurance, force, technique))
    
    # ÉQUIPE 2 : PSG - 18 joueurs (11 titulaires + 7 remplaçants)
    joueurs_psg = [
        # === TITULAIRES (11) ===
        ("Victor", "Victor", "Gardien", 15, 5, 70, 10),
        ("Yanis", "Yanis", "Défenseur Central", 10, 40, 40, 10),
        ("Hugo", "Hugo", "Défenseur Central", 10, 40, 40, 10),
        ("Ibrahim", "Ibrahim", "Arrière Droit", 40, 50, 5, 5),
        ("Samy", "Samy", "Arrière Gauche", 40, 50, 5, 5),
        ("Kamel", "Kamel", "Milieu Défensif", 10, 40, 40, 10),
        ("Nassim", "Nassim", "Milieu Central", 5, 50, 10, 35),
        ("Adem", "Adem", "Milieu Central", 5, 50, 10, 35),
        ("Noah", "Noah", "Ailier Gauche", 65, 5, 5, 25),
        ("Amir", "Amir", "Ailier Droit", 65, 5, 5, 25),
        ("Lucas", "Lucas", "Attaquant", 10, 10, 30, 50),
        
        # === REMPLAÇANTS (7) ===
        ("Julien", "Julien", "Remplaçant", 10, 70, 10, 10),
        ("Alex", "Alex", "Remplaçant", 10, 50, 10, 30),
        ("Léo", "Léo", "Remplaçant", 60, 10, 25, 5),
        ("Bruno", "Bruno", "Remplaçant", 10, 5, 75, 10),
        ("Maxime", "Maxime", "Remplaçant", 10, 40, 40, 10),
        ("Enzo", "Enzo", "Remplaçant", 55, 30, 5, 20),
        ("Raphaël", "Raphaël", "Remplaçant", 30, 15, 15, 40)
    ]
    
    # ÉQUIPE 3 : OM - 18 joueurs (11 titulaires + 7 remplaçants)
    joueurs_om = [
        # === TITULAIRES (11) ===
        ("Clément", "Clément", "Gardien", 15, 5, 70, 10),
        ("Bilal", "Bilal", "Défenseur Central", 10, 40, 40, 10),
        ("Romain", "Romain", "Défenseur Central", 10, 40, 40, 10),
        ("Moussa", "Moussa", "Arrière Droit", 40, 50, 5, 5),
        ("Anis", "Anis", "Arrière Gauche", 40, 50, 5, 5),
        ("Walid", "Walid", "Milieu Défensif", 10, 40, 40, 10),
        ("Youssef", "Youssef", "Milieu Central", 5, 50, 10, 35),
        ("Ismaël", "Ismaël", "Milieu Central", 5, 50, 10, 35),
        ("Ethan", "Ethan", "Ailier Gauche", 65, 5, 5, 25),
        ("Farid", "Farid", "Ailier Droit", 65, 5, 5, 25),
        ("Adam", "Adam", "Attaquant", 10, 10, 30, 50),
        
        # === REMPLAÇANTS (7) ===
        ("Antoine", "Antoine", "Remplaçant", 10, 70, 10, 10),
        ("Nicolas", "Nicolas", "Remplaçant", 10, 50, 10, 30),
        ("Kévin", "Kévin", "Remplaçant", 60, 10, 25, 5),
        ("Patrick", "Patrick", "Remplaçant", 10, 5, 75, 10),
        ("Sébastien", "Sébastien", "Remplaçant", 10, 40, 40, 10),
        ("Mathis", "Mathis", "Remplaçant", 55, 30, 5, 20),
        ("Damien", "Damien", "Remplaçant", 30, 15, 15, 40)
    ]
    
    # ÉQUIPE 4 : RACING - 18 joueurs (11 titulaires + 7 remplaçants)
    joueurs_racing = [
        # === TITULAIRES (11) ===
        ("Benjamin", "Benjamin", "Gardien", 15, 5, 70, 10),
        ("Rachid", "Rachid", "Défenseur Central", 10, 40, 40, 10),
        ("Florian", "Florian", "Défenseur Central", 10, 40, 40, 10),
        ("Hamza", "Hamza", "Arrière Droit", 40, 50, 5, 5),
        ("Yacine", "Yacine", "Arrière Gauche", 40, 50, 5, 5),
        ("Mehmet", "Mehmet", "Milieu Défensif", 10, 40, 40, 10),
        ("Karim", "Karim", "Milieu Central", 5, 50, 10, 35),
        ("Ali", "Ali", "Milieu Central", 5, 50, 10, 35),
        ("Mathéo", "Mathéo", "Ailier Gauche", 65, 5, 5, 25),
        ("Sofiane", "Sofiane", "Ailier Droit", 65, 5, 5, 25),
        ("Nolan", "Nolan", "Attaquant", 10, 10, 30, 50),
        
        # === REMPLAÇANTS (7) ===
        ("Louis", "Louis", "Remplaçant", 10, 70, 10, 10),
        ("Pierre", "Pierre", "Remplaçant", 10, 50, 10, 30),
        ("Théo", "Théo", "Remplaçant", 60, 10, 25, 5),
        ("Henri", "Henri", "Remplaçant", 10, 5, 75, 10),
        ("Quentin", "Quentin", "Remplaçant", 10, 40, 40, 10),
        ("Baptiste", "Baptiste", "Remplaçant", 55, 30, 5, 20),
        ("Adrien", "Adrien", "Remplaçant", 30, 15, 15, 40)
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
