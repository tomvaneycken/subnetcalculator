import random
import sys

def ask_for_number_sequence():
    try:
        print("\n")

        #IP-geldigheid controleren
        while True:
            ip_address = input("Wat is het IP-adres?: ")

            #Octetten controleren
            a = ip_address.split('.')

            if (len(a) == 4) and (1 <= int(a[0]) <= 223) and (int(a[0]) != 127) and (int(a[0]) != 169 or int(a[1]) != 254) and (0 <= int(a[1]) <= 255 and 0 <= int(a[2]) <= 255 and 0 <= int(a[3]) <= 255):

                break

            else:
                print("\nIP-adres en/of subnetmasker is ongeldig!\n")
                continue

        masks = [255, 254, 252, 248, 240, 224, 192, 128, 0]

        #De geldigheid van het subnetmasker controleren
        while True:
            subnet_mask = input("Wat is het subnetmasker?: ")

            #octetten controleren
            b = subnet_mask.split('.')

            if (len(b) == 4) and (int(b[0]) == 255) and (int(b[1]) in masks) and (int(b[2]) in masks) and (int(b[3]) in masks) and (int(b[0]) >= int(b[1]) >= int(b[2]) >= int(b[3])):
                print("\nIP-adres en subnetmasker zijn geldig!\n")
                break

            else:
                print("\n IP-adres en/of subnetmasker is ongeldig! \n")
                continue

        #Algoritme voor subnetidentificatie, gebaseerd op IP en subnetmasker

        #Converteren van masker naar een binaire string
        mask_octets_padded = []
        mask_octets_decimal = subnet_mask.split(".")
        #Print mask_octets_decimal Printen van mask octeten in

        for octet_index in range(0, len(mask_octets_decimal)):

            #printen van bin(int(mask_octets_decimal[octet_index]))

            binary_octet = bin(int(mask_octets_decimal[octet_index])).split("b")[1]
            #printen van binary_octet

            if len(binary_octet) == 8:
                mask_octets_padded.append(binary_octet)

            elif len(binary_octet) < 8:
                binary_octet_padded = binary_octet.zfill(8)
                mask_octets_padded.append(binary_octet_padded)

        #Printen van mask_octets_padded

        decimal_mask = "".join(mask_octets_padded)
        #Psrinten van  decimal_mask   #Voorbeeld: for 255.255.255.0 => 11111111111111111111111100000000

        #Hostbits in het masker tellen en aantal hosts / subnet berekenen
        no_of_zeros = decimal_mask.count("0")
        no_of_ones = 32 - no_of_zeros
        no_of_hosts = abs(2 ** no_of_zeros - 2) #retourneer positieve waarde voor masker / 32

        #printen van no_of_zeros
        #printen van no_of_ones
        #printen van no_of_hosts

        #Wildcard-masker verkrijgen
        wildcard_octets = []
        for w_octet in mask_octets_decimal:
            wild_octet = 255 - int(w_octet)
            wildcard_octets.append(str(wild_octet))

        #printen van wildcard_octets

        wildcard_mask = ".".join(wildcard_octets)
        #printen van wildcard_mask

        #IP converteren naar binaire tekenreeks
        ip_octets_padded = []
        ip_octets_decimal = ip_address.split(".")

        for octet_index in range(0, len(ip_octets_decimal)):

            binary_octet = bin(int(ip_octets_decimal[octet_index])).split("b")[1]

            if len(binary_octet) < 8:
                binary_octet_padded = binary_octet.zfill(8)
                ip_octets_padded.append(binary_octet_padded)

            else:
                ip_octets_padded.append(binary_octet)

        #printen van ip_octets_padded

        binary_ip = "".join(ip_octets_padded)

        #printen binair_ip   #voorbeeld: for 192.168.2.100 => 11000000101010000000001001100100

        #Haal het netwerkadres en uitzendadres op uit de hierboven verkregen binaire tekenreeksen

        network_address_binary = binary_ip[:(no_of_ones)] + "0" * no_of_zeros
        #printen van network_address_binary

        broadcast_address_binary = binary_ip[:(no_of_ones)] + "1" * no_of_zeros
        #printen van broadcast_address_binary

        net_ip_octets = []
        for octet in range(0, len(network_address_binary), 8):
            net_ip_octet = network_address_binary[octet:octet+8]
            net_ip_octets.append(net_ip_octet)

        #printen van net_ip_octets

        net_ip_address = []
        for each_octet in net_ip_octets:
            net_ip_address.append(str(int(each_octet, 2)))

        #printen van net_ip_address

        network_address = ".".join(net_ip_address)
        #printen van network_address

        bst_ip_octets = []
        for octet in range(0, len(broadcast_address_binary), 8):
            bst_ip_octet = broadcast_address_binary[octet:octet+8]
            bst_ip_octets.append(bst_ip_octet)

        #printen van bst_ip_octets

        bst_ip_address = []
        for each_octet in bst_ip_octets:
            bst_ip_address.append(str(int(each_octet, 2)))

        #printen van bst_ip_address

        broadcast_address = ".".join(bst_ip_address)
        #printen van broadcast_address

        #Resultaten voor gselecteerde IP/mask
        print("\n")
        print("De lengte van het subnetmasker: %s" % no_of_ones)#Mask bits
        print("Het adres van het subnet is: %s" % network_address)
        print("Het wildcardmasker is: %s" % wildcard_mask)
        print("Het Broadcastadres is: %s" % broadcast_address)
        print("Maximaal aantal hosts op dit subnet is: %s" % no_of_hosts)
        print("\n")

        #Genereren van willekeurige IP in subnet
        while True:
            generate = input("Genereer een willekeurig IP-adres uit het subnet? (y/n)")

            if generate == "y":
                generated_ip = []

                #Verkrijg een beschikbaar IP-adres binnen bereik, gebaseerd op het verschil tussen octetten in uitzendadres en netwerkadres
                for indexb, oct_bst in enumerate(bst_ip_address):
                    #printen indexb, oct_bst
                    for indexn, oct_net in enumerate(net_ip_address):
                        #printen indexn, oct_net
                        if indexb == indexn:
                            if oct_bst == oct_net:
                                #Voeg identieke octetten toe aan de generated_ip list
                                generated_ip.append(oct_bst)
                            else:
                                #Genereer willekeurige nummer (s) binnen octetintervallen en voeg deze toe aan de lijst
                                generated_ip.append(str(random.randint(int(oct_net), int(oct_bst))))

                #IP-adres gegenereerd uit de subnetpool
                #print gegenereerd ip
                y_iaddr = ".".join(generated_ip)
                #print y_iaddr

                print("Het random IP adres is: %s" % y_iaddr)
                print("\n")
                continue

            else:
                print("Tot ziens !\n")
                break

    except KeyboardInterrupt:
        print("\n\nProgramma afgebroken door gebruiker. Tot ziens...\n")
        sys.exit()

#Oproepen van de functie
ask_for_number_sequence()
