from ussd import USSDSimulator

def main():
    
    print("Tapez *111# pour commencer")
    input_sim = input("> ")

    if input_sim.strip() == "*111#":
        app = USSDSimulator()
        app.demarer()
    else:
        print("UNKNOWN APPLICATION")

if __name__ == "__main__":
    main()