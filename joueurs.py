"""
Module de gestion des joueurs
"""

import random
from database import get_connection


def ajouter_joueur():
    """
    Fonction CRUD : Permet d'ajouter un nouveau joueur à l'équipe OL
    Demande à l'utilisateur les informations du joueur (nom, poste, stats)
    """
    print("\n=== AJOUTER UN NOUVEAU JOUEUR ===")
    
    # Saisie des informations
    prenom = input("Prénom du joueur : ").strip()
    nom = input("Nom du joueur : ").strip()
    poste = input("Poste (Attaquant/Milieu/Défenseur/Gardien/Ailier) : ").strip()
    
    try:
        vitesse = int(input("Vitesse (0-100) : "))
        endurance = int(input("Endurance (0-100) : "))
        force = int(input("Force (0-100) : "))
        technique = int(input("Technique (0-100) : "))
        
        # Validation des valeurs
        if not all(0 <= stat <= 100 for stat in [vitesse, endurance, force, technique]):
            print("❌ Erreur : Les stats doivent être entre 0 et 100")
            return
        
        # Insertion dans la base de données
        conn = get_connection()
        cursor = conn.cursor()
        
        # Récupération de l'ID de l'OL
        cursor.execute("SELECT id FROM Equipe WHERE nom = 'OL'")
        id_ol = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO Joueur (id_equipe, nom, prenom, poste, vitesse, endurance, force, technique, duree_blessure)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (id_ol, nom, prenom, poste, vitesse, endurance, force, technique))
        
        conn.commit()
        conn.close()
        
        print(f"✓ {prenom} {nom} a été ajouté à l'équipe !")
        
    except ValueError:
        print("❌ Erreur : Veuillez entrer des nombres valides pour les stats")


def provoquer_blessure():
    """
    Fonction de test : Blesse un joueur au hasard
    La blessure dure 3 matchs (duree_blessure = 3)
    """
    print("\n=== PROVOQUER UNE BLESSURE (TEST) ===")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Récupération de l'ID de l'OL
    cursor.execute("SELECT id FROM Equipe WHERE nom = 'OL'")
    id_ol = cursor.fetchone()[0]
    
    # Récupération des joueurs disponibles (non blessés)
    cursor.execute("""
        SELECT id, prenom, nom, poste
        FROM Joueur
        WHERE id_equipe = ? AND duree_blessure = 0
    """, (id_ol,))
    
    joueurs_disponibles = cursor.fetchall()
    
    if not joueurs_disponibles:
        print("❌ Aucun joueur disponible pour être blessé")
        conn.close()
        return
    
    # Sélection aléatoire d'un joueur
    joueur = random.choice(joueurs_disponibles)
    
    # Application de la blessure (3 matchs)
    cursor.execute("""
        UPDATE Joueur
        SET duree_blessure = 3
        WHERE id = ?
    """, (joueur['id'],))
    
    conn.commit()
    conn.close()
    
    nom_complet = f"{joueur['prenom']} {joueur['nom']}"
    print(f"🤕 {nom_complet} ({joueur['poste']}) est blessé pour 3 matchs")
