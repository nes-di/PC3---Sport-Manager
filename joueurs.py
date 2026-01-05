"""
Module de gestion des joueurs
"""

import os
import random
from database import get_connection


def clear_screen():
    """Efface l'écran de la console"""
    os.system('cls' if os.name == 'nt' else 'clear')


def ajouter_joueur():
    """
    Fonction CRUD : Permet d'ajouter un nouveau joueur à l'équipe OL
    Demande à l'utilisateur les informations du joueur (nom, poste, stats)
    """
    clear_screen()
    print("\n=== AJOUTER UN NOUVEAU JOUEUR ===")
    
    # Saisie des informations
    nom = input("Nom du joueur : ").strip()
    poste = input("Poste (Attaquant/Milieu/Défenseur/Gardien/Ailier) : ").strip()
    
    try:
        vitesse = int(input("Vitesse (0-100) : "))
        endurance = int(input("Endurance (0-100) : "))
        force = int(input("Force (0-100) : "))
        technique = int(input("Technique (0-100) : "))
        
        # Insertion dans la base de données
        conn = get_connection()
        cursor = conn.cursor()
        
        # Récupération de l'ID de l'OL
        cursor.execute("SELECT id FROM Equipe WHERE nom = 'OL'")
        id_ol = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO Joueur (id_equipe, nom, poste, vitesse, endurance, force, technique, duree_blessure)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0)
        """, (id_ol, nom, poste, vitesse, endurance, force, technique))
        
        conn.commit()
        conn.close()
        
        print(f"✓ {nom} a été ajouté à l'équipe !")
        input("\nAppuyez sur Entrée pour revenir au menu...")
        
    except:
        input("\nAppuyez sur Entrée pour revenir au menu...")
