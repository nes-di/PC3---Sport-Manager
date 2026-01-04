"""
Module de gestion des matchs
"""

import random
from database import get_connection


def jouer_match():
    """
    Fonction principale pour jouer un match contre le PSG
    1. Vérifie que les joueurs blessés ne jouent pas
    2. Simule le match
    3. Demande le score final
    4. Met à jour les stats des joueurs présents
    5. Diminue la durée de blessure des joueurs absents
    """
    print("\n=== JOUER UN MATCH ===")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Récupération de l'ID de l'OL
    cursor.execute("SELECT id FROM Equipe WHERE nom = 'OL'")
    id_ol = cursor.fetchone()[0]
    
    # Vérification des joueurs disponibles
    cursor.execute("""
        SELECT id, prenom, nom, poste, duree_blessure
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
            nom_complet = f"{joueur['prenom']} {joueur['nom']}"
            print(f"  - {nom_complet} ({joueur['poste']}) - encore {joueur['duree_blessure']} match(s)")
    
    if len(joueurs_disponibles) < 11:
        print(f"\n❌ Pas assez de joueurs disponibles pour jouer un match 11v11")
        print(f"   Joueurs disponibles : {len(joueurs_disponibles)}/11")
        conn.close()
        return
    
    # Simulation du match
    print("\n⚽ Match en cours contre le PSG...")
    print("   ...")
    
    # Saisie du score final
    try:
        score_ol = int(input("\nScore de l'OL : "))
        score_psg = int(input("Score du PSG : "))
        
        # Enregistrement du match
        cursor.execute("""
            INSERT INTO Rencontre (adversaire, score_mon_equipe, score_adversaire)
            VALUES (?, ?, ?)
        """, ("PSG", score_ol, score_psg))
        
        # Affichage du résultat
        if score_ol > score_psg:
            print(f"\n🎉 VICTOIRE ! {score_ol}-{score_psg}")
        elif score_ol < score_psg:
            print(f"\n😞 DÉFAITE... {score_ol}-{score_psg}")
        else:
            print(f"\n🤝 MATCH NUL {score_ol}-{score_psg}")
        
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
            
            nom_complet = f"{joueur['prenom']} {joueur['nom']}"
            print(f"  ✓ {nom_complet} : +{bonus} {competence}")
        
        # Diminution de la durée de blessure pour tous les joueurs blessés
        if joueurs_blesses:
            print("\n🏥 Récupération des blessés...")
            cursor.execute("""
                UPDATE Joueur
                SET duree_blessure = MAX(duree_blessure - 1, 0)
                WHERE id_equipe = ? AND duree_blessure > 0
            """, (id_ol,))
            
            for joueur in joueurs_blesses:
                nouvelle_duree = max(joueur['duree_blessure'] - 1, 0)
                nom_complet = f"{joueur['prenom']} {joueur['nom']}"
                if nouvelle_duree == 0:
                    print(f"  ✓ {nom_complet} est rétabli !")
                else:
                    print(f"  ⏳ {nom_complet} : encore {nouvelle_duree} match(s)")
        
        conn.commit()
        print("\n✓ Match enregistré avec succès")
        
    except ValueError:
        print("❌ Erreur : Veuillez entrer des scores valides")
    
    conn.close()
