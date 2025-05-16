"""Module principal pour l'application USSD."""


class USSDSimulator:

    def __init__(self):
        """Initialise le simulateur USSD avec les menus imbriqués."""
        self.menus = {
            "main": {
                "1": {
                    "text": "Acheter Credit ou Offre Yas",
                    "action": self.acheter_credit,
                    "menu": "achat"
                },
                "2": {
                    "text": "Transferer argent",
                    "action": self.transferer_argent,
                    "menu": "transfert"
                },
                "3": {
                    "text": "MVola Credit ou Epargne",
                    "action": self.mvola,
                    "menu": "mvola"
                },
                "4": {
                    "text": "Retrait d'argent",
                    "action": self.retrait_argent,
                    "menu": "retrait"
                }
            },
            "achat": {
                "1": {"text": "Acheter credit", "action": self.acheter_credit_simple},
                "2": {"text": "Acheter offre Yas", "action": self.acheter_offre_yas},
                "0": {"text": "Retour", "action": lambda: "main"}
            },
            "transfert": {
                "1": {"text": "Vers Airtel", "action": lambda: self.faire_transfert("Airtel")},
                "2": {"text": "Vers Telma", "action": lambda: self.faire_transfert("Telma")},
                "3": {"text": "Vers Orange", "action": lambda: self.faire_transfert("Orange")},
                "4": {"text": "Vers compte bancaire", "action": lambda: self.faire_transfert("banque")},
                "0": {"text": "Retour", "action": lambda: "main"}
            },
            "retrait": {
                "1": {"text": "Retrait agent", "action": lambda: self.faire_retrait("agent")},
                "2": {"text": "Retrait guichet", "action": lambda: self.faire_retrait("guichet")},
                "0": {"text": "Retour", "action": lambda: "main"}
            },
            "mvola": {
                "1": {"text": "MVola Credit", "action": self.consulter_mvola_credit},
                "2": {"text": "MVola Epargne", "action": self.consulter_mvola_epargne},
                "0": {"text": "Retour", "action": lambda: "main"}
            }
        }
        self.current_menu = "main"
        self.solde = 50000.0  # Solde initial en Ariary

    def afficher_menu(self, menu_name):

        menu = self.menus.get(menu_name, {})
        print()

        for key, option in menu.items():
            print(f"{key}. {option['text']}")

    def gerer_choix(self, choix):

        menu = self.menus.get(self.current_menu, {})
        option = menu.get(choix, None)

        if not option:
            print("\nOption invalide. Veuillez réessayer.")
            return self.current_menu

        if "action" in option:
            result = option["action"]()

            if isinstance(result, str):
                return result

            if "menu" in option:
                return option["menu"]

        return self.current_menu

    def valider_numero(self, numero):
        return numero.isdigit() and len(numero) == 10

    def valider_montant(self, montant):
        try:
            montant_float = float(montant)
            return montant_float > 0 and montant_float <= self.solde
        except ValueError:
            return False

    def acheter_credit(self):
        return "achat"

    def transferer_argent(self):
        return "transfert"

    def retrait_argent(self):
        return "retrait"

    def mvola(self):
        return "mvola"

    def acheter_credit_simple(self):
        montant = input("\nEntrez le montant: ")
        if not self.valider_montant(montant):
            print("\nMontant invalide ou solde insuffisant.")
            input("\nAppuyez sur Entrée pour continuer...")
            return self.current_menu

        montant_float = float(montant)
        self.solde -= montant_float
        print(f"\nAchat de {montant_float} Ar effectué.")
        print(f"Nouveau solde: {self.solde} Ar")
        input("\nAppuyez sur Entrée pour continuer...")
        return "main"

    def acheter_offre_yas(self):
        print("\nOffres Yas disponibles:")
        print("1. Yas 1000 - 1000 Ar")
        print("2. Yas 5000 - 5000 Ar")
        choix = input("\nChoisissez une offre: ")

        if choix == "1" and self.valider_montant("1000"):
            self.solde -= 1000
            print("\nOffre Yas 1000 achetée.")
        elif choix == "2" and self.valider_montant("5000"):
            self.solde -= 5000
            print("\nOffre Yas 5000 achetée.")
        else:
            print("\nOpération annulée ou solde insuffisant.")

        print(f"Nouveau solde: {self.solde} Ar")
        input("\nAppuyez sur Entrée pour continuer...")
        return "main"

    def faire_transfert(self, operateur):
        print(f"\nTransfert vers {operateur}")
        numero = input("Numéro bénéficiaire: ")

        if not self.valider_numero(numero):
            print("\nNuméro invalide (10 chiffres requis).")
            input("\nAppuyez sur Entrée pour continuer...")
            return self.current_menu

        montant = input("Montant à transférer (Ar): ")
        if not self.valider_montant(montant):
            print("\nMontant invalide ou solde insuffisant.")
            input("\nAppuyez sur Entrée pour continuer...")
            return self.current_menu

        montant_float = float(montant)
        frais = 200.0
        total = montant_float + frais

        if total > self.solde:
            print("\nSolde insuffisant pour couvrir les frais.")
            input("\nAppuyez sur Entrée pour continuer...")
            return self.current_menu

        print(f"\nConfirmer transfert de {montant_float} Ar")
        print(f"vers {numero} ({operateur})")
        print(f"Frais: {frais} Ar - Total: {total} Ar")
        confirmation = input("1 pour confirmer, 0 pour annuler: ")

        if confirmation == "1":
            self.solde -= total
            print("\nTransfert effectué avec succès!")
            print(f"Nouveau solde: {self.solde} Ar")
        else:
            print("\nTransfert annulé.")

        input("\nAppuyez sur Entrée pour continuer...")
        return "main"

    def faire_retrait(self, type_retrait):
        print(f"\nRetrait {type_retrait}")
        montant = input("Montant à retirer (Ar): ")

        if not self.valider_montant(montant):
            print("\nMontant invalide ou solde insuffisant.")
            input("\nAppuyez sur Entrée pour continuer...")
            return self.current_menu

        montant_float = float(montant)
        frais = 500.0 if type_retrait == "agent" else 300.0
        total = montant_float + frais

        if type_retrait == "agent":
            code_agent = input("Code agent (6 chiffres): ")
            if not (code_agent.isdigit() and len(code_agent) == 6):
                print("\nCode agent invalide.")
                input("\nAppuyez sur Entrée pour continuer...")
                return self.current_menu

        if total > self.solde:
            print("\nSolde insuffisant pour couvrir les frais.")
            input("\nAppuyez sur Entrée pour continuer...")
            return self.current_menu

        print(f"\nConfirmer retrait de {montant_float} Ar")
        print(f"Frais: {frais} Ar - Total: {total} Ar")
        confirmation = input("1 pour confirmer, 0 pour annuler: ")

        if confirmation == "1":
            self.solde -= total
            print("\nRetrait effectué avec succès!")
            print(f"Nouveau solde: {self.solde} Ar")
        else:
            print("\nRetrait annulé.")

        input("\nAppuyez sur Entrée pour continuer...")
        return "main"

    def consulter_mvola_credit(self):
        print(f"\nVotre solde MVola Credit: {self.solde} Ar")
        input("\nAppuyez sur Entrée pour continuer...")
        return "main"

    def consulter_mvola_epargne(self):
        solde_epargne = 100000.0  # Valeur simulée
        print(f"\nVotre solde MVola Epargne: {solde_epargne} Ar")
        input("\nAppuyez sur Entrée pour continuer...")
        return "main"

    def demarrer(self):
        print("\nBienvenue dans l'application USSD *111#")

        while True:
            self.afficher_menu(self.current_menu)
            choix = input("\nChoisissez une option (0 pour quitter): ")

            if choix == "0":
                if self.current_menu == "main":
                    print("\nMerci d'avoir utilisé notre service USSD.")
                    break
                self.current_menu = "main"
                continue

            self.current_menu = self.gerer_choix(choix)
