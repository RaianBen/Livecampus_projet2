from Scan.Scanner import thread_scan, async_scan, display_open_ports, check_ip, choose_mode

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
