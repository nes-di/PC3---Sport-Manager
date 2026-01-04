"""
Module de gestion des équipes
"""

import os
from database import get_connection


def clear_screen():
    """Efface l'écran de la console"""
    os.system('cls' if os.name == 'nt' else 'clear')


def afficher_mon_equipe():
    """
    Affiche tous les joueurs de mon équipe (OL) avec leur état
    État : "Disponible" ou "Blessé (reste X matchs)"
    """
    clear_screen()
    conn = get_connection()
    cursor = conn.cursor()
    
    # Récupération de l'ID de l'OL
    cursor.execute("SELECT id FROM Equipe WHERE nom = 'OL'")
    id_ol = cursor.fetchone()[0]
    
    # Récupération de tous les joueurs de l'OL
    cursor.execute("""
        SELECT nom, prenom, poste, vitesse, endurance, force, technique, duree_blessure
        FROM Joueur
        WHERE id_equipe = ?
        ORDER BY poste, nom
    """, (id_ol,))
    
    joueurs = cursor.fetchall()
    conn.close()
    
    print("\n=== MON ÉQUIPE (OL) ===")
    print(f"{'Nom':<15} {'Poste':<20} {'Vit':<5} {'End':<5} {'For':<5} {'Tech':<5} {'État':<25}")
    print("-" * 90)
    
    for joueur in joueurs:
        nom = f"{joueur['prenom']} {joueur['nom']}"
        poste = joueur['poste']
        vit = joueur['vitesse']
        end = joueur['endurance']
        force = joueur['force']
        tech = joueur['technique']
        duree = joueur['duree_blessure']
        
        # Détermination de l'état du joueur
        if duree > 0:
            etat = f"🤕 Blessé (reste {duree} match{'s' if duree > 1 else ''})"
        else:
            etat = "✓ Disponible"
        
        print(f"{nom:<15} {poste:<20} {vit:<5} {end:<5} {force:<5} {tech:<5} {etat:<25}")
    
    print()
    input("\nAppuyez sur Entrée pour revenir au menu...")


def afficher_historique():
    """
    Affiche l'historique de tous les matchs joués
    """
    clear_screen()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT adversaire, score_mon_equipe, score_adversaire
        FROM Rencontre
        ORDER BY id DESC
    """)
    
    matchs = cursor.fetchall()
    conn.close()
    
    if not matchs:
        print("\n📋 Aucun match joué pour le moment")
        input("\nAppuyez sur Entrée pour revenir au menu...")
        return
    
    print("\n=== HISTORIQUE DES MATCHS ===")
    print(f"{'Adversaire':<15} {'Score':<15} {'Résultat':<15}")
    print("-" * 45)
    
    for match in matchs:
        adversaire = match['adversaire']
        score = f"{match['score_mon_equipe']} - {match['score_adversaire']}"
        
        if match['score_mon_equipe'] > match['score_adversaire']:
            resultat = "✓ Victoire"
        elif match['score_mon_equipe'] < match['score_adversaire']:
            resultat = "✗ Défaite"
        else:
            resultat = "= Nul"
        
        print(f"{adversaire:<15} {score:<15} {resultat:<15}")
    
    print()
    input("\nAppuyez sur Entrée pour revenir au menu...")
