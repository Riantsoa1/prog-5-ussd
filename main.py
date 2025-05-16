

from ussd import USSDSimulator


def main():
    print("Simulation USSD - Tapez *111# pour commencer")
    input_sim = input("> ")

    if input_sim.strip() == "*111#":
        app = USSDSimulator()
        app.demarrer()
    else:
        print("Commande USSD invalide. Veuillez taper *111#")


if __name__ == "__main__":
    main()
