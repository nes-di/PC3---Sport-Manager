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
    État : "Disponible" ou "Blessé (retour prévu le...)"
    """
    clear_screen()
    conn = get_connection()
    cursor = conn.cursor()
    
    # Récupération de l'ID de l'OL
    cursor.execute("SELECT id_equipe FROM Equipe WHERE nom = 'OL'")
    id_ol = cursor.fetchone()['id_equipe']
    
    # Récupération de tous les joueurs de l'OL avec leurs infos
    cursor.execute("""
        SELECT 
            j.id_joueur,
            j.nom,
            j.prenom,
            p.nom_poste,
            j.statut,
            b.matchs_restants
        FROM Joueurs j
        JOIN Poste p ON j.id_poste = p.id_poste
        LEFT JOIN Blessure b ON j.id_joueur = b.id_joueur 
            AND b.matchs_restants > 0
        WHERE j.id_equipe = ?
        ORDER BY p.nom_poste, j.nom
    """, (id_ol,))
    
    joueurs = cursor.fetchall()
    
    # Récupération des compétences pour chaque joueur
    print("\n=== MON ÉQUIPE (OL) ===")
    print(f"{'Prénom':<12} {'Nom':<15} {'Poste':<20} {'Vit':<5} {'End':<5} {'For':<5} {'Tech':<5} {'État':<25}")
    print("-" * 105)
    
    for joueur in joueurs:
        prenom = joueur['prenom'] or ""
        nom = joueur['nom']
        poste = joueur['nom_poste']
        
        # Récupération des compétences du joueur
        cursor.execute("""
            SELECT c.nom, jc.niveau
            FROM Joueur_competence jc
            JOIN Competence c ON jc.id_competence = c.id_competence
            WHERE jc.id_joueur = ?
        """, (joueur['id_joueur'],))
        
        competences = {row['nom']: row['niveau'] for row in cursor.fetchall()}
        vit = competences.get('Vitesse', 0)
        end = competences.get('Endurance', 0)
        force = competences.get('Force', 0)
        tech = competences.get('Technique', 0)
        
        # Détermination de l'état du joueur
        if joueur['matchs_restants'] and joueur['matchs_restants'] > 0:
            matchs = joueur['matchs_restants']
            etat = f"🤕 Blessé ({matchs} match{'s' if matchs > 1 else ''})"
        elif joueur['statut'] == 'absent':
            etat = "❌ Absent"
        else:
            etat = "✓ Disponible"
        
        print(f"{prenom:<12} {nom:<15} {poste:<20} {vit:<5} {end:<5} {force:<5} {tech:<5} {etat:<25}")
    
    conn.close()
    print()
    input("\nAppuyez sur Entrée pour revenir au menu...")


def afficher_historique():
    """
    Affiche l'historique de tous les matchs joués
    """
    clear_screen()
    conn = get_connection()
    cursor = conn.cursor()
    
    # Récupération de l'ID de l'OL
    cursor.execute("SELECT id_equipe FROM Equipe WHERE nom = 'OL'")
    id_ol = cursor.fetchone()['id_equipe']
    
    # Récupération de tous les matchs de l'OL
    cursor.execute("""
        SELECT 
            r.id_rencontre,
            re1.score as score_ol,
            re2.score as score_adversaire,
            e2.nom as adversaire
        FROM Rencontre r
        JOIN Rencontre_equipe re1 ON r.id_rencontre = re1.id_rencontre 
            AND re1.id_equipe = ?
        JOIN Rencontre_equipe re2 ON r.id_rencontre = re2.id_rencontre 
            AND re2.id_equipe != ?
        JOIN Equipe e2 ON re2.id_equipe = e2.id_equipe
        ORDER BY r.id_rencontre DESC
    """, (id_ol, id_ol))
    
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
        score = f"{match['score_ol']} - {match['score_adversaire']}"
        
        if match['score_ol'] > match['score_adversaire']:
            resultat = "✓ Victoire"
        elif match['score_ol'] < match['score_adversaire']:
            resultat = "✗ Défaite"
        else:
            resultat = "= Nul"
        
        print(f"{adversaire:<15} {score:<15} {resultat:<15}")
    
    print()
    input("\nAppuyez sur Entrée pour revenir au menu...")
