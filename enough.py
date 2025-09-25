from colorama import Fore, Style
from time import sleep
from os import system
from sms import SendSms
import threading
import pyfiglet  # <- Ekledik

# ASCII başlık
system("cls||clear")
ascii_art = pyfiglet.figlet_format("MAJCP", font="slant")
print(Fore.LIGHTCYAN_EX + ascii_art + Style.RESET_ALL)

# SendSms modülündeki tüm servisleri al
servisler_sms = []
for attribute in dir(SendSms):
    if callable(getattr(SendSms, attribute)) and not attribute.startswith('__'):
        servisler_sms.append(attribute)

while True:
    print(f"Sms: {len(servisler_sms)}           by {Fore.LIGHTRED_EX}@SERHAT_YGT{Style.RESET_ALL}\n")
    
    try:
        menu = int(input(Fore.LIGHTMAGENTA_EX + 
                         " 1- SMS Gönder (Normal)\n"
                         " 2- SMS Gönder (Turbo)\n"
                         " 3- Çıkış\n\n"
                         + Fore.LIGHTYELLOW_EX + " Seçim: "))
    except ValueError:
        system("cls||clear")
        print(Fore.LIGHTRED_EX + "Hatalı giriş yaptın. Tekrar deneyiniz.")
        sleep(3)
        continue

    if menu == 1:
        # Normal SMS Gönder
        system("cls||clear")
        print(Fore.LIGHTYELLOW_EX + 
              "Telefon numarasını başında '+90' olmadan yazınız (Birden çoksa 'enter' tuşuna basınız): " + 
              Fore.LIGHTGREEN_EX, end="")
        tel_no = input()
        tel_liste = []

        if tel_no == "":
            system("cls||clear")
            print(Fore.LIGHTYELLOW_EX + 
                  "Telefon numaralarının kayıtlı olduğu dosyanın dizinini yazınız: " + 
                  Fore.LIGHTGREEN_EX, end="")
            dizin = input()
            try:
                with open(dizin, "r", encoding="utf-8") as f:
                    for i in f.read().strip().split("\n"):
                        if len(i) == 10:
                            tel_liste.append(i)
                sonsuz = ""
            except FileNotFoundError:
                system("cls||clear")
                print(Fore.LIGHTRED_EX + "Hatalı dosya dizini. Tekrar deneyiniz.")
                sleep(3)
                continue
        else:
            try:
                int(tel_no)
                if len(tel_no) != 10:
                    raise ValueError
                tel_liste.append(tel_no)
                sonsuz = "(Sonsuz ise 'enter' tuşuna basınız)"
            except ValueError:
                system("cls||clear")
                print(Fore.LIGHTRED_EX + "Hatalı telefon numarası. Tekrar deneyiniz.") 
                sleep(3)
                continue

        # Mail adresi al
        system("cls||clear")
        try:
            print(Fore.LIGHTYELLOW_EX + 
                  "Mail adresi (Bilmiyorsanız 'enter' tuşuna basın): " + 
                  Fore.LIGHTGREEN_EX, end="")
            mail = input()
            if ("@" not in mail or ".com" not in mail) and mail != "":
                raise ValueError
        except:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Hatalı mail adresi. Tekrar deneyiniz.") 
            sleep(3)
            continue

        # Kaç adet SMS
        system("cls||clear")
        try:
            print(Fore.LIGHTYELLOW_EX + f"Kaç adet SMS göndermek istiyorsun {sonsuz}: " + Fore.LIGHTGREEN_EX, end="")
            kere = input()
            kere = int(kere) if kere else None
        except ValueError:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Hatalı giriş yaptın. Tekrar deneyiniz.") 
            sleep(3)
            continue

        # SMS aralığı
        system("cls||clear")
        try:
            print(Fore.LIGHTYELLOW_EX + "Kaç saniye aralıkla göndermek istiyorsun: " + Fore.LIGHTGREEN_EX, end="")
            aralik = int(input())
        except ValueError:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Hatalı giriş yaptın. Tekrar deneyiniz.") 
            sleep(3)
            continue

        system("cls||clear")
        if kere is None:
            # Sonsuz gönderim
            for num in tel_liste:
                sms = SendSms(num, mail)
                while True:
                    for fonk in servisler_sms:
                        getattr(sms, fonk)()
                        sleep(aralik)
        else:
            for num in tel_liste:
                sms = SendSms(num, mail)
                while sms.adet < kere:
                    for fonk in servisler_sms:
                        if sms.adet >= kere:
                            break
                        getattr(sms, fonk)()
                        sleep(aralik)

        print(Fore.LIGHTRED_EX + "\nMenüye dönmek için 'enter' tuşuna basınız..")
        input()

    elif menu == 2:
        # Turbo SMS Gönder
        system("cls||clear")
        print(Fore.LIGHTYELLOW_EX + "Telefon numarasını başında '+90' olmadan yazınız: "+ Fore.LIGHTGREEN_EX, end="")
        tel_no = input()
        try:
            int(tel_no)
            if len(tel_no) != 10:
                raise ValueError
        except ValueError:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Hatalı telefon numarası. Tekrar deneyiniz.") 
            sleep(3)
            continue

        # Mail adresi al
        system("cls||clear")
        try:
            print(Fore.LIGHTYELLOW_EX + "Mail adresi (Bilmiyorsanız 'enter' tuşuna basın): "+ Fore.LIGHTGREEN_EX, end="")
            mail = input()
            if ("@" not in mail or ".com" not in mail) and mail != "":
                raise ValueError
        except:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Hatalı mail adresi. Tekrar deneyiniz.") 
            sleep(3)
            continue

        # Turbo gönderim thread
        send_sms = SendSms(tel_no, mail)
        dur = threading.Event()
        def Turbo():
            while not dur.is_set():
                thread_list = []
                for fonk in servisler_sms:
                    t = threading.Thread(target=getattr(send_sms, fonk), daemon=True)
                    thread_list.append(t)
                    t.start()
                for t in thread_list:
                    t.join()

        try:
            Turbo()
        except KeyboardInterrupt:
            dur.set()
            system("cls||clear")
            print("\nCtrl+C tuş kombinasyonu algılandı. Menüye dönülüyor..")
            sleep(2)

    elif menu == 3:
        # Çıkış
        system("cls||clear")
        print(Fore.LIGHTRED_EX + "Çıkış yapılıyor...")
        break
