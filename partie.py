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
    5. Enregistre le match avec les tables Rencontre et Rencontre_equipe
    6. Enregistre la participation des joueurs dans Joueur_rencontre
    7. Met à jour les compétences des joueurs présents
    8. Gère les blessures via la table Blessure
    """
    clear_screen()
    print("\n=== JOUER UN MATCH ===")
    
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
        
        # Choix de l'adversaire
        cursor.execute("SELECT id_equipe, nom FROM Equipe WHERE nom != 'OL'")
        equipes_adverses = cursor.fetchall()
        
        print("\n📋 Choisissez votre adversaire :")
        for i, equipe in enumerate(equipes_adverses, 1):
            print(f"  {i}. {equipe['nom']}")
        
        choix = int(input("\nVotre choix : ").strip())
        equipe_adverse = equipes_adverses[choix - 1]
        id_adversaire = equipe_adverse['id_equipe']
        nom_adversaire = equipe_adverse['nom']
        
        # Vérification des joueurs disponibles (non blessés)
        cursor.execute("""
            SELECT 
                j.id_joueur,
                j.nom,
                j.prenom,
                p.nom_poste,
                b.matchs_restants
            FROM Joueurs j
            JOIN Poste p ON j.id_poste = p.id_poste
            LEFT JOIN Blessure b ON j.id_joueur = b.id_joueur 
                AND b.matchs_restants > 0
            WHERE j.id_equipe = ? AND j.statut = 'présent'
        """, (id_ol,))
        
        tous_joueurs = cursor.fetchall()
        joueurs_disponibles = [j for j in tous_joueurs if not j['matchs_restants']]
        joueurs_blesses = [j for j in tous_joueurs if j['matchs_restants']]
        
        print(f"\n📊 Effectif disponible : {len(joueurs_disponibles)} joueurs")
        
        if joueurs_blesses:
            print("\n🤕 Joueurs blessés (ne jouent pas) :")
            for joueur in joueurs_blesses:
                prenom = joueur['prenom'] or ""
                matchs = joueur['matchs_restants']
                print(f"  - {prenom} {joueur['nom']} ({joueur['nom_poste']}) - {matchs} match{'s' if matchs > 1 else ''}")
        
        if len(joueurs_disponibles) < 11:
            print(f"\n❌ Pas assez de joueurs disponibles pour jouer un match 11v11")
            print(f"   Joueurs disponibles : {len(joueurs_disponibles)}/11")
            conn.close()
            input("\nAppuyez sur Entrée pour revenir au menu...")
            return
        
        # Simulation du match
        print(f"\n⚽ Match en cours contre {nom_adversaire}...")
        print("   ...")
        
        # Saisie du score final
        while True:
            try:
                score_ol = int(input("\nScore de l'OL : "))
                score_adversaire = int(input(f"Score de {nom_adversaire} : "))
                break
            except:
                print("❌ Veuillez entrer des nombres valides")
        
        # Création de la rencontre
        cursor.execute("""
            INSERT INTO Rencontre (lieu, commentaires)
            VALUES (?, ?)
        """, ("Stade", ""))
        
        id_rencontre = cursor.lastrowid
        
        # Enregistrement des scores dans Rencontre_equipe
        cursor.execute("""
            INSERT INTO Rencontre_equipe (id_rencontre, id_equipe, score)
            VALUES (?, ?, ?)
        """, (id_rencontre, id_ol, score_ol))
        
        cursor.execute("""
            INSERT INTO Rencontre_equipe (id_rencontre, id_equipe, score)
            VALUES (?, ?, ?)
        """, (id_rencontre, id_adversaire, score_adversaire))
        
        # Affichage du résultat
        if score_ol > score_adversaire:
            print(f"\n🎉 VICTOIRE ! {score_ol}-{score_adversaire}")
        elif score_ol < score_adversaire:
            print(f"\n😞 DÉFAITE... {score_ol}-{score_adversaire}")
        else:
            print(f"\n🤝 MATCH NUL {score_ol}-{score_adversaire}")
        
        # Enregistrement de la participation des joueurs et évolution
        print("\n📈 Évolution des joueurs...")
        for joueur in joueurs_disponibles:
            # Enregistrement dans Joueur_rencontre
            note = random.randint(5, 10)  # Note de performance
            cursor.execute("""
                INSERT INTO Joueur_rencontre (id_rencontre, id_joueur, note_performance)
                VALUES (?, ?, ?)
            """, (id_rencontre, joueur['id_joueur'], note))
            
            # Amélioration aléatoire d'une compétence
            cursor.execute("""
                SELECT id_competence, nom 
                FROM Competence
            """)
            competences = cursor.fetchall()
            competence_choisie = random.choice(competences)
            bonus = random.randint(1, 3)
            
            # Mise à jour de la compétence
            cursor.execute("""
                UPDATE Joueur_competence
                SET niveau = MIN(niveau + ?, 100)
                WHERE id_joueur = ? AND id_competence = ?
            """, (bonus, joueur['id_joueur'], competence_choisie['id_competence']))
            
            prenom = joueur['prenom'] or ""
            print(f"  ✓ {prenom} {joueur['nom']} : +{bonus} {competence_choisie['nom']}")
        
        # Blessures aléatoires (7% de chance par joueur)
        print("\n🏥 Bilan médical...")
        blessures_survenues = False
        for joueur in joueurs_disponibles:
            if random.random() < 0.07:
                # Blessure de 1 à 3 matchs
                matchs_blessure = random.randint(1, 3)
                
                cursor.execute("""
                    INSERT INTO Blessure (id_joueur, matchs_restants, notes_description)
                    VALUES (?, ?, ?)
                """, (joueur['id_joueur'], matchs_blessure, "Blessure lors du match"))
                
                prenom = joueur['prenom'] or ""
                print(f"  🤕 {prenom} {joueur['nom']} s'est blessé ! (absent {matchs_blessure} match{'s' if matchs_blessure > 1 else ''})")
                blessures_survenues = True
        
        if not blessures_survenues:
            print("  ✓ Aucune blessure à signaler")
        
        # Mise à jour des anciennes blessures (décrémentation)
        if joueurs_blesses:
            print("\n💊 Récupération des anciens blessés...")
            for joueur in joueurs_blesses:
                # Décrémenter le compteur de matchs
                cursor.execute("""
                    UPDATE Blessure
                    SET matchs_restants = matchs_restants - 1
                    WHERE id_joueur = ? AND matchs_restants > 0
                """, (joueur['id_joueur'],))
                
                nouveau_compte = joueur['matchs_restants'] - 1
                prenom = joueur['prenom'] or ""
                if nouveau_compte == 0:
                    print(f"  ✓ {prenom} {joueur['nom']} est rétabli !")
                else:
                    print(f"  ⏳ {prenom} {joueur['nom']} : encore {nouveau_compte} match{'s' if nouveau_compte > 1 else ''}")
        
        conn.commit()
        print("\n✓ Match enregistré avec succès")
        input("\nAppuyez sur Entrée pour revenir au menu...")
    
    except Exception as e:
        print(f"\n❌ Erreur lors du match : {e}")
        conn.rollback()
        input("\nAppuyez sur Entrée pour revenir au menu...")
    finally:
        conn.close()
