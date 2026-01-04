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
    
    # Insertion des joueurs de l'OL (Mon équipe) - 18 joueurs (11 titulaires + 7 remplaçants)
    joueurs_ol = [
        # === TITULAIRES (11) ===
        # Gardien
        ("Lopes", "Anthony", "Gardien", 15, 50, 70, 45),
        # Défenseurs
        ("Lukeba", "Castello", "Défenseur Central", 25, 55, 65, 35),
        ("Tagliafico", "Nicolas", "Défenseur Central", 20, 60, 70, 40),
        ("Gusto", "Malo", "Défenseur Latéral Droit", 60, 55, 45, 50),
        ("Henrique", "Alex", "Défenseur Latéral Gauche", 55, 60, 50, 45),
        # Milieux
        ("Thuram", "Khéphren", "Milieu Défensif", 40, 70, 55, 60),
        ("Caqueret", "Maxence", "Milieu Central", 45, 65, 40, 70),
        ("Tolisso", "Corentin", "Milieu Offensif", 35, 60, 50, 75),
        # Attaquants
        ("Cherki", "Rayan", "Ailier Gauche", 70, 50, 30, 80),
        ("Fofana", "Malick", "Ailier Droit", 75, 55, 35, 70),
        ("Lacazette", "Alexandre", "Attaquant Centre", 40, 60, 60, 85),
        
        # === REMPLAÇANTS (7) ===
        ("Perri", "Lucas", "Gardien", 10, 45, 65, 35),
        ("Mata", "Clinton", "Défenseur", 30, 50, 55, 30),
        ("Diomandé", "Sinaly", "Défenseur", 25, 45, 60, 25),
        ("Lepenant", "Johann", "Milieu", 30, 55, 40, 50),
        ("Maitland-Niles", "Ainsley", "Milieu", 50, 50, 35, 55),
        ("Nuamah", "Ernest", "Attaquant", 65, 40, 25, 60),
        ("Mikautadze", "Georges", "Attaquant", 35, 45, 50, 65)
    ]
    
    for nom, prenom, poste, vitesse, endurance, force, technique in joueurs_ol:
        cursor.execute("""
            INSERT INTO Joueur (id_equipe, nom, prenom, poste, vitesse, endurance, force, technique, duree_blessure)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (id_ol, nom, prenom, poste, vitesse, endurance, force, technique))
    
    # Insertion des joueurs du PSG (Équipe adverse) - 18 joueurs (11 titulaires + 7 remplaçants)
    joueurs_psg = [
        # === TITULAIRES (11) ===
        # Gardien
        ("Donnarumma", "Gianluigi", "Gardien", 20, 55, 75, 50),
        # Défenseurs
        ("Marquinhos", "Marcos", "Défenseur Central", 25, 65, 75, 55),
        ("Skriniar", "Milan", "Défenseur Central", 20, 60, 80, 50),
        ("Hakimi", "Achraf", "Défenseur Latéral Droit", 85, 60, 50, 65),
        ("Mendes", "Nuno", "Défenseur Latéral Gauche", 60, 65, 55, 50),
        # Milieux
        ("Vitinha", "Vítor", "Milieu Défensif", 45, 75, 45, 75),
        ("Zaïre-Emery", "Warren", "Milieu Central", 50, 70, 40, 80),
        ("Ruiz", "Fabián", "Milieu Offensif", 40, 65, 50, 85),
        # Attaquants
        ("Dembélé", "Ousmane", "Ailier Gauche", 90, 60, 40, 85),
        ("Barcola", "Bradley", "Ailier Droit", 85, 65, 45, 75),
        ("Gonçalo Ramos", "Gonçalo", "Attaquant Centre", 50, 65, 70, 80),
        
        # === REMPLAÇANTS (7) ===
        ("Navas", "Keylor", "Gardien", 15, 50, 70, 45),
        ("Mukiele", "Nordi", "Défenseur", 55, 60, 60, 40),
        ("Beraldo", "Lucas", "Défenseur", 30, 55, 65, 35),
        ("Ugarte", "Manuel", "Milieu", 40, 70, 60, 60),
        ("Soler", "Carlos", "Milieu", 35, 60, 45, 70),
        ("Asensio", "Marco", "Attaquant", 55, 55, 40, 80),
        ("Kolo Muani", "Randal", "Attaquant", 65, 60, 65, 70)
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
