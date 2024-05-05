import socket  # Module pour la communication par sockets
import threading  # Module pour la programmation multithread
import asyncio  # Module pour la programmation asynchrone

# Fonction pour scanner un port
def scan_port(host, port):
    # Vérifier si le numéro de port est correct
    if 0 < port < 65536:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # Définir un temps pour la connexion
                result = s.connect_ex((host, port))  # Tenter de se connecter au port
                if result == 0:
                    return port, True  # Retourner le numéro du port et True si la connexion réussit
                else:
                    return port, False  # Retourner le numéro du port et False si la connexion échoue
        except socket.error:
            return port, False  # Retourner le numéro du port et False en cas d'erreur
    else:
        return port, False  # Retourner le numéro du port et False si le port est invalide

# Fonction pour scanner les ports en utilisant des threads
def thread_scan(host, ports):
    open_ports = []  # Liste pour stocker les ports ouverts
    for port in ports:
        thread = threading.Thread(target=lambda p: open_ports.append(scan_port(host, p)), args=(port,))
        thread.start()  # Démarrer le thread pour scanner le port
    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()  # Attendre la fin de tous les threads
    return open_ports  # Retourner la liste des ports ouverts

# Fonction asynchrone pour scanner un port
async def scan_port_async(host, port):
    # Vérifier si le numéro de port est valide
    if 0 < port < 65536:
        try:
            reader, writer = await asyncio.open_connection(host, port)  # Ouvrir une connexion au port
            writer.close()  # Fermer la connexion
            return port, True  # Retourner le numéro du port et True si la connexion réussit
        except (asyncio.TimeoutError, ConnectionRefusedError):
            return port, False  # Retourner le numéro du port et False si la connexion échoue
    else:
        return port, False  # Retourner le numéro du port et False si le port est invalide

# Fonction pour scanner les ports de manière asynchrone
async def async_scan(host, ports):
    open_ports = []  # Liste pour stocker les ports ouverts
    tasks = [asyncio.create_task(scan_port_async(host, port)) for port in ports]  # Créer les tâches asynchrones
    await asyncio.gather(*tasks)  # Attendre l'achèvement de toutes les tâches
    for task in tasks:
        result = task.result()  # Obtenir le résultat de la tâche
        if result[1]:
            open_ports.append(result)  # Ajouter le port ouvert à la liste
    return open_ports  # Retourner la liste des ports ouverts

# Fonction pour afficher les ports ouverts
def display_open_ports(ports):
    if ports:
        print("Ports ouverts :")
        for port in ports:
            print(f"Port {port[0]} : Ouvert")  # Afficher chaque port ouvert
    else:
        print("Aucun port ouvert trouvé.")

# Fonction pour choisir le mode de fonctionnement
def choose_mode():
    print("Choisissez le mode de fonctionnement :")
    print("1. Synchrone")
    print("2. Threads")
    print("3. Asynchrone")
    choice = input("Votre choix (1/2/3) : ")
    return choice

# Fonction pour vérifier si l'adresse IP est valide
def check_ip():
    while True:
        host = input("Entrez l'adresse IP à scanner (par exemple localhost) : ")
        try:
            socket.inet_aton(host)
            break
        except socket.error:
            print("L'adresse IP n'est pas valide. Veuillez entrer une adresse IP correcte.")
    return host

if __name__ == "__main__":
    host = check_ip()
    ports_to_scan = range(1, 1025)  # Ports de 1 à 1024

    while True:
        choice = choose_mode()
        if choice == '1':
            open_ports = thread_scan(host, ports_to_scan)  # Appel de la fonction pour scanner les ports synchrones
            display_open_ports(open_ports)  # Afficher les ports ouverts
            break
        elif choice == '2':
            open_ports = thread_scan(host, ports_to_scan)  # Appel de la fonction pour scanner les ports avec threads
            display_open_ports(open_ports)  # Afficher les ports ouverts
            break
        elif choice == '3':
            open_ports = asyncio.run(async_scan(host, ports_to_scan))  # Appel de la fonction pour scanner les ports asynchrones
            display_open_ports(open_ports)  # Afficher les ports ouverts
            break