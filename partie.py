"""
Module de gestion des matchs
"""

import os
import random
from database import get_connection


def clear_screen():
    """Efface l'écran de la console"""
    os.system('cls' if os.name == 'nt' else 'clear')


def jouer_match():
    """
    Fonction principale pour jouer un match
    1. Choix de l'adversaire
    2. Vérifie que les joueurs blessés ne jouent pas
    3. Simule le match
    4. Demande le score final
    5. Met à jour les stats des joueurs présents
    6. Diminue la durée de blessure des joueurs absents
    """
    clear_screen()
    print("\n=== JOUER UN MATCH ===")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Récupération de l'ID de l'OL
    cursor.execute("SELECT id FROM Equipe WHERE nom = 'OL'")
    id_ol = cursor.fetchone()[0]
    
    # Choix de l'adversaire
    cursor.execute("SELECT nom FROM Equipe WHERE nom != 'OL'")
    equipes_adverses = [row['nom'] for row in cursor.fetchall()]
    
    print("\n📋 Choisissez votre adversaire :")
    for i, equipe in enumerate(equipes_adverses, 1):
        print(f"  {i}. {equipe}")
    
    choix = int(input("\nVotre choix : ").strip())
    adversaire = equipes_adverses[choix - 1]
    
    # Vérification des joueurs disponibles
    cursor.execute("""
        SELECT id, nom, poste, duree_blessure
        FROM Joueur
        WHERE id_equipe = ?
    """, (id_ol,))
    
    joueurs = cursor.fetchall()
    joueurs_disponibles = [j for j in joueurs if j['duree_blessure'] == 0]
    joueurs_blesses = [j for j in joueurs if j['duree_blessure'] > 0]
    
    print(f"\n📊 Effectif disponible : {len(joueurs_disponibles)} joueurs")
    
    if joueurs_blesses:
        print("\n🤕 Joueurs blessés (ne jouent pas) :")
        for joueur in joueurs_blesses:
            print(f"  - {joueur['nom']} ({joueur['poste']}) - encore {joueur['duree_blessure']} match(s)")
    
    if len(joueurs_disponibles) < 11:
        print(f"\n❌ Pas assez de joueurs disponibles pour jouer un match 11v11")
        print(f"   Joueurs disponibles : {len(joueurs_disponibles)}/11")
        conn.close()
        input("\nAppuyez sur Entrée pour revenir au menu...")
        return
    
    # Simulation du match
    print(f"\n⚽ Match en cours contre {adversaire}...")
    print("   ...")
    
    # Saisie du score final avec boucle jusqu'à obtenir des valeurs valides
    while True:
        try:
            score_ol = int(input("\nScore de l'OL : "))
            score_adversaire_input = int(input(f"Score de {adversaire} : "))
            break  # Si on arrive ici, les scores sont valides
        except:
            pass
    
    # Enregistrement du match
    cursor.execute("""
        INSERT INTO Rencontre (adversaire, score_mon_equipe, score_adversaire)
        VALUES (?, ?, ?)
    """, (adversaire, score_ol, score_adversaire_input))
    
    # Affichage du résultat
    if score_ol > score_adversaire_input:
        print(f"\n🎉 VICTOIRE ! {score_ol}-{score_adversaire_input}")
    elif score_ol < score_adversaire_input:
        print(f"\n😞 DÉFAITE... {score_ol}-{score_adversaire_input}")
    else:
        print(f"\n🤝 MATCH NUL {score_ol}-{score_adversaire_input}")
    
    # Évolution des joueurs ayant joué (bonus aléatoire sur une compétence)
    print("\n📈 Évolution des joueurs...")
    for joueur in joueurs_disponibles:
        # Choix aléatoire d'une compétence à améliorer
        competences = ['vitesse', 'endurance', 'force', 'technique']
        competence = random.choice(competences)
        bonus = random.randint(1, 3)
        
        cursor.execute(f"""
            UPDATE Joueur
            SET {competence} = MIN({competence} + ?, 100)
            WHERE id = ?
        """, (bonus, joueur['id']))
        
        print(f"  ✓ {joueur['nom']} : +{bonus} {competence}")
    
    # Blessures aléatoires pendant le match (15% de chance par joueur ayant joué)
    print("\n🏥 Bilan médical...")
    blessures_survenues = False
    for joueur in joueurs_disponibles:
        # 15% de chance de se blesser pendant le match
        if random.random() < 0.15:
            duree_blessure = random.randint(1, 4)  # Blessure de 1 à 4 matchs
            cursor.execute("""
                UPDATE Joueur
                SET duree_blessure = ?
                WHERE id = ?
            """, (duree_blessure, joueur['id']))
            
            print(f"  🤕 {joueur['nom']} s'est blessé ! (absent {duree_blessure} match{'s' if duree_blessure > 1 else ''})")
            blessures_survenues = True
    
    if not blessures_survenues:
        print("  ✓ Aucune blessure à signaler")
    
    # Diminution de la durée de blessure pour tous les joueurs blessés
    if joueurs_blesses:
        print("\n💊 Récupération des anciens blessés...")
        cursor.execute("""
            UPDATE Joueur
            SET duree_blessure = MAX(duree_blessure - 1, 0)
            WHERE id_equipe = ? AND duree_blessure > 0
        """, (id_ol,))
        
        for joueur in joueurs_blesses:
            nouvelle_duree = max(joueur['duree_blessure'] - 1, 0)
            if nouvelle_duree == 0:
                print(f"  ✓ {joueur['nom']} est rétabli !")
            else:
                print(f"  ⏳ {joueur['nom']} : encore {nouvelle_duree} match(s)")
    
    conn.commit()
    print("\n✓ Match enregistré avec succès")
    input("\nAppuyez sur Entrée pour revenir au menu...")
    
    conn.close()
