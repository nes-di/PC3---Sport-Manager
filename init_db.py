"""
Script d'initialisation de la base de données
"""

from database import get_connection, create_tables


def insert_seed_data():
    """
    Insère les données de départ (postes, compétences, équipes et joueurs)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # ========== DONNÉES DE RÉFÉRENCE ==========
    
    # Insertion des Postes
    postes = [
        "Gardien",
        "Défenseur Central",
        "Arrière Droit",
        "Arrière Gauche",
        "Milieu Défensif",
        "Milieu Central",
        "Ailier Gauche",
        "Ailier Droit",
        "Attaquant",
        "Remplaçant"
    ]
    
    for poste in postes:
        cursor.execute("INSERT INTO Poste (nom_poste) VALUES (?)", (poste,))
    
    # Insertion des Compétences
    competences = ["Vitesse", "Endurance", "Force", "Technique"]
    
    for competence in competences:
        cursor.execute("INSERT INTO Competence (nom) VALUES (?)", (competence,))
    
    # Récupération des IDs des postes et compétences
    cursor.execute("SELECT id_poste, nom_poste FROM Poste")
    postes_dict = {row['nom_poste']: row['id_poste'] for row in cursor.fetchall()}
    
    cursor.execute("SELECT id_competence, nom FROM Competence")
    competences_dict = {row['nom']: row['id_competence'] for row in cursor.fetchall()}
    
    # ========== ÉQUIPES ==========
    
    equipes_data = [
        ("OL", 11, "Coach", "OL"),
        ("PSG", 11, "Coach", "PSG"),
        ("OM", 11, "Coach", "OM"),
        ("RACING", 11, "Coach", "RACING")
    ]
    
    for nom, effectif, nom_coach, prenom_coach in equipes_data:
        cursor.execute("""
            INSERT INTO Equipe (nom, effectif_principal, nom_coach, prenom_coach)
            VALUES (?, ?, ?, ?)
        """, (nom, effectif, nom_coach, prenom_coach))
    
    # Récupération des IDs des équipes
    cursor.execute("SELECT id_equipe, nom FROM Equipe")
    equipes_dict = {row['nom']: row['id_equipe'] for row in cursor.fetchall()}
    
    # ========== JOUEURS ==========
    
    # ÉQUIPE OL - 18 joueurs
    joueurs_ol = [
        # (prénom, nom, poste, vitesse, endurance, force, technique)
        ("Olivier", "Dubois", "Gardien", 15, 5, 70, 10),
        ("Mehdi", "Martin", "Défenseur Central", 10, 40, 40, 10),
        ("Paul", "Bernard", "Défenseur Central", 10, 40, 40, 10),
        ("Ousmane", "Petit", "Arrière Droit", 40, 50, 5, 5),
        ("Rayan", "Robert", "Arrière Gauche", 40, 50, 5, 5),
        ("Ilyes", "Richard", "Milieu Défensif", 10, 40, 40, 10),
        ("Abdel", "Durand", "Milieu Central", 5, 50, 10, 35),
        ("Kilyan", "Moreau", "Milieu Central", 5, 50, 10, 35),
        ("Evann", "Simon", "Ailier Gauche", 65, 5, 5, 25),
        ("Süleyman", "Laurent", "Ailier Droit", 65, 5, 5, 25),
        ("Emre", "Lefebvre", "Attaquant", 10, 10, 30, 50),
        ("Martin", "Michel", "Remplaçant", 10, 70, 10, 10),
        ("Mike", "Garcia", "Remplaçant", 10, 50, 10, 30),
        ("Wu", "David", "Remplaçant", 60, 10, 25, 5),
        ("Georges", "Bertrand", "Remplaçant", 10, 5, 75, 10),
        ("Thomas", "Roux", "Remplaçant", 10, 40, 40, 10),
        ("Matthieu", "Vincent", "Remplaçant", 55, 30, 5, 20),
        ("Cristiano", "Fournier", "Remplaçant", 30, 15, 15, 40)
    ]
    
    # ÉQUIPE PSG - 18 joueurs
    joueurs_psg = [
        ("Victor", "Girard", "Gardien", 15, 5, 70, 10),
        ("Yanis", "Bonnet", "Défenseur Central", 10, 40, 40, 10),
        ("Hugo", "Dupont", "Défenseur Central", 10, 40, 40, 10),
        ("Ibrahim", "Lambert", "Arrière Droit", 40, 50, 5, 5),
        ("Samy", "Fontaine", "Arrière Gauche", 40, 50, 5, 5),
        ("Kamel", "Rousseau", "Milieu Défensif", 10, 40, 40, 10),
        ("Nassim", "Vincent", "Milieu Central", 5, 50, 10, 35),
        ("Adem", "Muller", "Milieu Central", 5, 50, 10, 35),
        ("Noah", "Leroy", "Ailier Gauche", 65, 5, 5, 25),
        ("Amir", "Garnier", "Ailier Droit", 65, 5, 5, 25),
        ("Lucas", "Faure", "Attaquant", 10, 10, 30, 50),
        ("Julien", "Andre", "Remplaçant", 10, 70, 10, 10),
        ("Alex", "Mercier", "Remplaçant", 10, 50, 10, 30),
        ("Léo", "Blanc", "Remplaçant", 60, 10, 25, 5),
        ("Bruno", "Guerin", "Remplaçant", 10, 5, 75, 10),
        ("Maxime", "Boyer", "Remplaçant", 10, 40, 40, 10),
        ("Enzo", "Chevalier", "Remplaçant", 55, 30, 5, 20),
        ("Raphaël", "Clement", "Remplaçant", 30, 15, 15, 40)
    ]
    
    # ÉQUIPE OM - 18 joueurs
    joueurs_om = [
        ("Clément", "Legrand", "Gardien", 15, 5, 70, 10),
        ("Bilal", "Gauthier", "Défenseur Central", 10, 40, 40, 10),
        ("Romain", "Lopez", "Défenseur Central", 10, 40, 40, 10),
        ("Moussa", "Perrin", "Arrière Droit", 40, 50, 5, 5),
        ("Anis", "Morel", "Arrière Gauche", 40, 50, 5, 5),
        ("Walid", "Giraud", "Milieu Défensif", 10, 40, 40, 10),
        ("Youssef", "Denis", "Milieu Central", 5, 50, 10, 35),
        ("Ismaël", "Lemaire", "Milieu Central", 5, 50, 10, 35),
        ("Ethan", "Dumont", "Ailier Gauche", 65, 5, 5, 25),
        ("Farid", "Marie", "Ailier Droit", 65, 5, 5, 25),
        ("Adam", "Barbier", "Attaquant", 10, 10, 30, 50),
        ("Antoine", "Brun", "Remplaçant", 10, 70, 10, 10),
        ("Nicolas", "Dumas", "Remplaçant", 10, 50, 10, 30),
        ("Kévin", "Colin", "Remplaçant", 60, 10, 25, 5),
        ("Patrick", "Caron", "Remplaçant", 10, 5, 75, 10),
        ("Sébastien", "Renard", "Remplaçant", 10, 40, 40, 10),
        ("Mathis", "Arnaud", "Remplaçant", 55, 30, 5, 20),
        ("Damien", "Marty", "Remplaçant", 30, 15, 15, 40)
    ]
    
    # ÉQUIPE RACING - 18 joueurs
    joueurs_racing = [
        ("Benjamin", "Noel", "Gardien", 15, 5, 70, 10),
        ("Rachid", "Picard", "Défenseur Central", 10, 40, 40, 10),
        ("Florian", "Roger", "Défenseur Central", 10, 40, 40, 10),
        ("Hamza", "Vidal", "Arrière Droit", 40, 50, 5, 5),
        ("Yacine", "Bouvier", "Arrière Gauche", 40, 50, 5, 5),
        ("Mehmet", "Marchal", "Milieu Défensif", 10, 40, 40, 10),
        ("Karim", "Olivier", "Milieu Central", 5, 50, 10, 35),
        ("Ali", "Charles", "Milieu Central", 5, 50, 10, 35),
        ("Mathéo", "Sanchez", "Ailier Gauche", 65, 5, 5, 25),
        ("Sofiane", "Dupuis", "Ailier Droit", 65, 5, 5, 25),
        ("Nolan", "Moulin", "Attaquant", 10, 10, 30, 50),
        ("Louis", "Brunet", "Remplaçant", 10, 70, 10, 10),
        ("Pierre", "Maire", "Remplaçant", 10, 50, 10, 30),
        ("Théo", "Henry", "Remplaçant", 60, 10, 25, 5),
        ("Henri", "Guillot", "Remplaçant", 10, 5, 75, 10),
        ("Quentin", "Fernandez", "Remplaçant", 10, 40, 40, 10),
        ("Baptiste", "Schneider", "Remplaçant", 55, 30, 5, 20),
        ("Adrien", "Gerard", "Remplaçant", 30, 15, 15, 40)
    ]
    
    # Insertion de tous les joueurs
    for equipe_nom, joueurs_list in [
        ("OL", joueurs_ol),
        ("PSG", joueurs_psg),
        ("OM", joueurs_om),
        ("RACING", joueurs_racing)
    ]:
        id_equipe = equipes_dict[equipe_nom]
        
        for prenom, nom, nom_poste, vitesse, endurance, force, technique in joueurs_list:
            id_poste = postes_dict[nom_poste]
            
            # Insertion du joueur
            cursor.execute("""
                INSERT INTO Joueurs (id_equipe, nom, prenom, id_poste, statut)
                VALUES (?, ?, ?, ?, 'présent')
            """, (id_equipe, nom, prenom, id_poste))
            
            id_joueur = cursor.lastrowid
            
            # Insertion des compétences du joueur
            cursor.execute("""
                INSERT INTO Joueur_competence (id_joueur, id_competence, niveau)
                VALUES (?, ?, ?)
            """, (id_joueur, competences_dict["Vitesse"], vitesse))
            
            cursor.execute("""
                INSERT INTO Joueur_competence (id_joueur, id_competence, niveau)
                VALUES (?, ?, ?)
            """, (id_joueur, competences_dict["Endurance"], endurance))
            
            cursor.execute("""
                INSERT INTO Joueur_competence (id_joueur, id_competence, niveau)
                VALUES (?, ?, ?)
            """, (id_joueur, competences_dict["Force"], force))
            
            cursor.execute("""
                INSERT INTO Joueur_competence (id_joueur, id_competence, niveau)
                VALUES (?, ?, ?)
            """, (id_joueur, competences_dict["Technique"], technique))
    
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    insert_seed_data()
