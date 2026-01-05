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
    Demande à l'utilisateur les informations du joueur (nom, prénom, poste, stats)
    """
    clear_screen()
    print("\n=== AJOUTER UN NOUVEAU JOUEUR ===")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Récupération de l'ID de l'OL
        cursor.execute("SELECT id_equipe FROM Equipe WHERE nom = 'OL'")
        result = cursor.fetchone()
        if not result:
            print("❌ Équipe OL non trouvée")
            conn.close()
            input("\nAppuyez sur Entrée pour revenir au menu...")
            return
        
        id_ol = result['id_equipe']
        
        # Saisie des informations
        prenom = input("Prénom du joueur : ").strip()
        nom = input("Nom du joueur : ").strip()
        
        # Affichage des postes disponibles
        cursor.execute("SELECT id_poste, nom_poste FROM Poste")
        postes = cursor.fetchall()
        
        print("\nPostes disponibles :")
        for i, poste in enumerate(postes, 1):
            print(f"  {i}. {poste['nom_poste']}")
        
        choix_poste = int(input("\nChoisissez le poste (numéro) : "))
        id_poste = postes[choix_poste - 1]['id_poste']
        
        # Saisie des compétences
        print("\nCompétences (0-100) :")
        vitesse = int(input("Vitesse : "))
        endurance = int(input("Endurance : "))
        force = int(input("Force : "))
        technique = int(input("Technique : "))
        
        # Insertion du joueur
        cursor.execute("""
            INSERT INTO Joueurs (id_equipe, nom, prenom, id_poste, statut)
            VALUES (?, ?, ?, ?, 'présent')
        """, (id_ol, nom, prenom, id_poste))
        
        id_joueur = cursor.lastrowid
        
        # Récupération des IDs des compétences
        cursor.execute("SELECT id_competence, nom FROM Competence")
        competences = {row['nom']: row['id_competence'] for row in cursor.fetchall()}
        
        # Insertion des compétences du joueur
        cursor.execute("""
            INSERT INTO Joueur_competence (id_joueur, id_competence, niveau)
            VALUES (?, ?, ?)
        """, (id_joueur, competences['Vitesse'], min(max(vitesse, 0), 100)))
        
        cursor.execute("""
            INSERT INTO Joueur_competence (id_joueur, id_competence, niveau)
            VALUES (?, ?, ?)
        """, (id_joueur, competences['Endurance'], min(max(endurance, 0), 100)))
        
        cursor.execute("""
            INSERT INTO Joueur_competence (id_joueur, id_competence, niveau)
            VALUES (?, ?, ?)
        """, (id_joueur, competences['Force'], min(max(force, 0), 100)))
        
        cursor.execute("""
            INSERT INTO Joueur_competence (id_joueur, id_competence, niveau)
            VALUES (?, ?, ?)
        """, (id_joueur, competences['Technique'], min(max(technique, 0), 100)))
        
        conn.commit()
        
        print(f"\n✓ {prenom} {nom} a été ajouté à l'équipe !")
        input("\nAppuyez sur Entrée pour revenir au menu...")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'ajout du joueur : {e}")
        input("\nAppuyez sur Entrée pour revenir au menu...")
    finally:
        conn.close()
