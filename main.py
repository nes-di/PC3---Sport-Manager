"""
Fichier principal de Sport Manager
Point d'entrée de l'application avec la boucle du menu
"""

from database import get_connection
from menu import afficher_menu
from equipes import afficher_mon_equipe, afficher_historique
from joueurs import ajouter_joueur
from partie import jouer_match


def main():
    """
    Fonction principale : Boucle du menu
    """
    print("\n🎮 Bienvenue dans SPORT MANAGER !")
    print("Gérez votre équipe de l'OL !\n")
    
    # Boucle principale du menu
    while True:
        afficher_menu()
        choix = input("\nVotre choix : ").strip()
        
        if choix == "1":
            afficher_mon_equipe()
        elif choix == "2":
            ajouter_joueur()
        elif choix == "3":
            jouer_match()
        elif choix == "4":
            afficher_historique()
        elif choix == "5":
            print("\n👋 Merci d'avoir joué à Sport Manager !")
            print("À bientôt !\n")
            break


if __name__ == "__main__":
    main()
