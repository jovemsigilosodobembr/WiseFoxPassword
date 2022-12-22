#!/usr/bin/python3

import argparse
import configparser
import csv
import functools
import gzip
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import time

__author__ = "Mebus"
__license__ = "GPL"
__version__ = "3.3.0"

CONFIG = {}


def read_config(filename):
    """Read the given configuration file and update global variables to reflect
    changes (CONFIG)."""

    if os.path.isfile(filename):

        # global CONFIG

        # Reading configuration file
        config = configparser.ConfigParser()
        config.read(filename)

        CONFIG["global"] = {
            "years": config.get("years", "years").split(","),
            "chars": config.get("specialchars", "chars").split(","),
            "numfrom": config.getint("nums", "from"),
            "numto": config.getint("nums", "to"),
            "wcfrom": config.getint("nums", "wcfrom"),
            "wcto": config.getint("nums", "wcto"),
            "threshold": config.getint("nums", "threshold"),
            "alectourl": config.get("alecto", "alectourl"),
            "dicturl": config.get("downloader", "dicturl"),
        }

        # 1337 mode configs, well you can add more lines if you add it to the
        # config file too.
        leet = functools.partial(config.get, "leet")
        leetc = {}
        letters = {"a", "i", "e", "t", "o", "s", "g", "z"}

        for letter in letters:
            leetc[letter] = config.get("leet", letter)

        CONFIG["LEET"] = leetc

        return True

    else:
        print("Configuration file " + filename + " not found!")
        sys.exit("Exiting.")

        return False


def make_leet(x):
    """convert string to leet"""
    for letter, leetletter in CONFIG["LEET"].items():
        x = x.replace(letter, leetletter)
    return x


# for concatenations...
def concats(seq, start, stop):
    for mystr in seq:
        for num in range(start, stop):
            yield mystr + str(num)


# for sorting and making combinations...
def komb(seq, start, special=""):
    for mystr in seq:
        for mystr1 in start:
            yield mystr + special + mystr1


# print list to file counting words


def print_to_file(filename, unique_list_finished):
    f = open(filename, "w")
    unique_list_finished.sort()
    f.write(os.linesep.join(unique_list_finished))
    f.close()
    f = open(filename, "r")
    lines = 0
    for line in f:
        lines += 1
    f.close()
    print(
        "[+] Saving dictionary to \033[1;31m"
        + filename
        + "\033[1;m, counting \033[1;31m"
        + str(lines)
        + " words.\033[1;m"
    )
    inspect = input("> Ver Senha Ao Vivo? (Y) : ").lower()
    if inspect == "y":
        try:
            with open(filename, "r+") as wlist:
                data = wlist.readlines()
                for line in data:
                    print("\033[1;32m[" + filename + "] \033[1;33m" + line)
                  
                    os.system("clear")
        except Exception as e:
            print("[ERROR]: " + str(e))
    else:
        pass

    print(
        "[+] Criando Nova Wordlist \033[1;31m"
        + filename
        + "\033[1;m Wordlist criada com sucesso!"
    )


def print_cow():
    print(" ___________ ")
    print(" \033[07m  WiseFox.py! \033[27m# \033[07mGilmarScript \033[27mBR")
    print("                        \033[07mU\033[27mBR")
    print("                    \033[07mP\033[27mSENHA")
    print(28 * " " + "[ Mebus | https://github.com/gilmarscript/]\r\n")


def version():
    """Display version"""

    print("\r\n	\033[1;31m[ WiseFox.py ]  " + __version__ + "\033[1;m\r\n")
    print("	* Hacked up by j0rgan - j0rgan@remote-exploit.org")
    print("	* http://www.remote-exploit.org\r\n")
    print("	Take a look ./README.md file for more info about the program\r\n")


def improve_dictionary(file_to_open):
    """Implementation of the -w option. Improve a dictionary by
    interactively questioning the user."""

    kombinacija = {}
    komb_unique = {}

    if not os.path.isfile(file_to_open):
        exit("Error: file " + file_to_open + " does not exist.")

    chars = CONFIG["global"]["chars"]
    years = CONFIG["global"]["years"]
    numfrom = CONFIG["global"]["numfrom"]
    numto = CONFIG["global"]["numto"]

    fajl = open(file_to_open, "r")
    listic = fajl.readlines()
    listica = []
    for x in listic:
        listica += x.split()

    print("\r\n      *************************************************")
    print("      *                    \033[1;31mWARNING!!!\033[1;m                 *")
    print("      *         Using large wordlists in some         *")
    print("      *       options bellow is NOT recommended!      *")
    print("      *************************************************\r\n")

    conts = input(
        "> Do you want to concatenate all words from wordlist? Y/[N]: "
    ).lower()

    if conts == "y" and len(listic) > CONFIG["global"]["threshold"]:
        print(
            "\r\n[-] Maximum number of words for concatenation is "
            + str(CONFIG["global"]["threshold"])
        )
        print("[-] Check configuration file for increasing this number.\r\n")
        conts = input(
            "> Do you want to concatenate all words from wordlist? Y/[N]: "
        ).lower()

    cont = [""]
    if conts == "y":
        for cont1 in listica:
            for cont2 in listica:
                if listica.index(cont1) != listica.index(cont2):
                    cont.append(cont1 + cont2)

    spechars = [""]
    spechars1 = input(
        "> Do you want to add special chars at the end of words? Y/[N]: "
    ).lower()
    if spechars1 == "y":
        for spec1 in chars:
            spechars.append(spec1)
            for spec2 in chars:
                spechars.append(spec1 + spec2)
                for spec3 in chars:
                    spechars.append(spec1 + spec2 + spec3)

    randnum = input(
        "> Você quer adicionar alguns números aleatórios no final das palavras? Y/[N]:"
    ).lower()
    leetmode = input("> modo Leet? (i.e. leet = 1337) Y/[N]: ").lower()

    # init
    for i in range(6):
        kombinacija[i] = [""]

    kombinacija[0] = list(komb(listica, years))
    if conts == "y":
        kombinacija[1] = list(komb(cont, years))
    if spechars1 == "y":
        kombinacija[2] = list(komb(listica, spechars))
        if conts == "y":
            kombinacija[3] = list(komb(cont, spechars))
    if randnum == "y":
        kombinacija[4] = list(concats(listica, numfrom, numto))
        if conts == "y":
            kombinacija[5] = list(concats(cont, numfrom, numto))

    print("\r\n[+] Now making a dictionary...")

    print("[+] Sorting list and removing duplicates...")

    for i in range(6):
        komb_unique[i] = list(dict.fromkeys(kombinacija[i]).keys())

    komb_unique[6] = list(dict.fromkeys(listica).keys())
    komb_unique[7] = list(dict.fromkeys(cont).keys())

    # join the lists
    uniqlist = []
    for i in range(8):
        uniqlist += komb_unique[i]

    unique_lista = list(dict.fromkeys(uniqlist).keys())
    unique_leet = []
    if leetmode == "y":
        for (
            x
        ) in (
            unique_lista
        ):  # se você quiser adicionar mais leet chars, você precisará adicionar mais linhas em cupp.cfg também...
            x = make_leet(x)  # converter para let
            unique_leet.append(x)

    unique_list = unique_lista + unique_leet

    unique_list_finished = []

    unique_list_finished = [
        x
        for x in unique_list
        if len(x) > CONFIG["global"]["wcfrom"] and len(x) < CONFIG["global"]["wcto"]
    ]

    print_to_file(file_to_open + ".cupp.txt", unique_list_finished)

    fajl.close()


def interactive():
    """Implementação da opção -i. Questione interativamente o usuário e
    crie um arquivo de dicionário de senhas com base na resposta."""

    print("\r\n[+] Insira as informações sobre a vítima para fazer um dicionário")
    print("[+] Se você não souber todas as informações, basta pressionar enter quando solicitado! ;)\r\n")

    # Precisamos de algumas informações primeiro!

    profile = {}

    name = input("> Primeiro nome: ").lower()
    while len(name) == 0 or name == " " or name == "  " or name == "   ":
        print("\r\n[-] você deve digitar um nome pelo menos!")
        name = input("> Nome: ").lower()
    profile["name"] = str(name)

    profile["surname"] = input("> Sobrenome: ").lower()
    profile["nick"] = input("> Apelido: ").lower()
    birthdate = input("> Data de nascimento (DDMMYYYY): ")
    while len(birthdate) != 0 and len(birthdate) != 8:
        print("\r\n[-] Você deve inserir 8 dígitos para aniversário!")
        birthdate = input("> Data de nascimento (DDMMYYYY): ")
    profile["birthdate"] = str(birthdate)

    print("\r\n")

    profile["wife"] = input("> nome) nome: ").lower()
    profile["wifen"] = input("> apelido) apelido: ").lower()
    wifeb = input("> Partners) data de nascimento (DDMMYYYY): ")
    while len(wifeb) != 0 and len(wifeb) != 8:
        print("\r\n[-] Você deve inserir 8 dígitos para aniversário!")
        wifeb = input("> data de nascimento dos parceiros (DDMMYYYY): ")
    profile["wifeb"] = str(wifeb)
    print("\r\n")

    profile["kid"] = input("> nome da criança: ").lower()
    profile["kidn"] = input("> Apelido da criança: ").lower()
    kidb = input("> data de nascimento da criança (DDMMYYYY): ")
    while len(kidb) != 0 and len(kidb) != 8:
        print("\r\n[-] Você deve inserir 8 dígitos para aniversário!")
        kidb = input("> data de nascimento da criança (DDMMYYYY): ")
    profile["kidb"] = str(kidb)
    print("\r\n")

    profile["pet"] = input("> Nome do animal de estimação: ").lower()
    profile["company"] = input("> Nome da empresa: ").lower()
    print("\r\n")

    profile["words"] = [""]
    words1 = input(
        "> Deseja adicionar algumas palavras-chave sobre a vítima? Y/[N]: "
    ).lower()
    words2 = ""
    if words1 == "y":
        words2 = input(
            "> Por favor, digite as palavras, separadas por vírgula. [i.e. hacker,juice,black], espaços serão removidos: "
        ).replace(" ", "")
    profile["words"] = words2.split(",")

    profile["spechars1"] = input(
        "> Deseja adicionar caracteres especiais no final das palavras? Y/[N]: "
    ).lower()

    profile["randnum"] = input(
        ">Você deseja adicionar alguns números aleatórios no final das palavras? Y/[N]:"
    ).lower()
    profile["leetmode"] = input("> Leet mode? (i.e. leet = 1337) Y/[N]: ").lower()

    generate_wordlist_from_profile(profile)  # generate the wordlist


def generate_wordlist_from_profile(profile):
    """ Generates a wordlist from a given profile """

    chars = CONFIG["global"]["chars"]
    years = CONFIG["global"]["years"]
    numfrom = CONFIG["global"]["numfrom"]
    numto = CONFIG["global"]["numto"]

    profile["spechars"] = []

    if profile["spechars1"] == "y":
        for spec1 in chars:
            profile["spechars"].append(spec1)
            for spec2 in chars:
                profile["spechars"].append(spec1 + spec2)
                for spec3 in chars:
                    profile["spechars"].append(spec1 + spec2 + spec3)

    print("\r\n[+] Now making a dictionary...")

    # Now me must do some string modifications...

    # Birthdays first

    birthdate_yy = profile["birthdate"][-2:]
    birthdate_yyy = profile["birthdate"][-3:]
    birthdate_yyyy = profile["birthdate"][-4:]
    birthdate_xd = profile["birthdate"][1:2]
    birthdate_xm = profile["birthdate"][3:4]
    birthdate_dd = profile["birthdate"][:2]
    birthdate_mm = profile["birthdate"][2:4]

    wifeb_yy = profile["wifeb"][-2:]
    wifeb_yyy = profile["wifeb"][-3:]
    wifeb_yyyy = profile["wifeb"][-4:]
    wifeb_xd = profile["wifeb"][1:2]
    wifeb_xm = profile["wifeb"][3:4]
    wifeb_dd = profile["wifeb"][:2]
    wifeb_mm = profile["wifeb"][2:4]

    kidb_yy = profile["kidb"][-2:]
    kidb_yyy = profile["kidb"][-3:]
    kidb_yyyy = profile["kidb"][-4:]
    kidb_xd = profile["kidb"][1:2]
    kidb_xm = profile["kidb"][3:4]
    kidb_dd = profile["kidb"][:2]
    kidb_mm = profile["kidb"][2:4]

    # Convert first letters to uppercase...

    nameup = profile["name"].title()
    surnameup = profile["surname"].title()
    nickup = profile["nick"].title()
    wifeup = profile["wife"].title()
    wifenup = profile["wifen"].title()
    kidup = profile["kid"].title()
    kidnup = profile["kidn"].title()
    petup = profile["pet"].title()
    companyup = profile["company"].title()

    wordsup = []
    wordsup = list(map(str.title, profile["words"]))

    word = profile["words"] + wordsup

    # reverse a name

    rev_name = profile["name"][::-1]
    rev_nameup = nameup[::-1]
    rev_nick = profile["nick"][::-1]
    rev_nickup = nickup[::-1]
    rev_wife = profile["wife"][::-1]
    rev_wifeup = wifeup[::-1]
    rev_kid = profile["kid"][::-1]
    rev_kidup = kidup[::-1]

    reverse = [
        rev_name,
        rev_nameup,
        rev_nick,
        rev_nickup,
        rev_wife,
        rev_wifeup,
        rev_kid,
        rev_kidup,
    ]
    rev_n = [rev_name, rev_nameup, rev_nick, rev_nickup]
    rev_w = [rev_wife, rev_wifeup]
    rev_k = [rev_kid, rev_kidup]
    # Let's do some serious work! This will be a mess of code, but... who cares? :)

    # Birthdays combinations

    bds = [
        birthdate_yy,
        birthdate_yyy,
        birthdate_yyyy,
        birthdate_xd,
        birthdate_xm,
        birthdate_dd,
        birthdate_mm,
    ]

    bdss = []

    for bds1 in bds:
        bdss.append(bds1)
        for bds2 in bds:
            if bds.index(bds1) != bds.index(bds2):
                bdss.append(bds1 + bds2)
                for bds3 in bds:
                    if (
                        bds.index(bds1) != bds.index(bds2)
                        and bds.index(bds2) != bds.index(bds3)
                        and bds.index(bds1) != bds.index(bds3)
                    ):
                        bdss.append(bds1 + bds2 + bds3)

                # For a woman...
    wbds = [wifeb_yy, wifeb_yyy, wifeb_yyyy, wifeb_xd, wifeb_xm, wifeb_dd, wifeb_mm]

    wbdss = []

    for wbds1 in wbds:
        wbdss.append(wbds1)
        for wbds2 in wbds:
            if wbds.index(wbds1) != wbds.index(wbds2):
                wbdss.append(wbds1 + wbds2)
                for wbds3 in wbds:
                    if (
                        wbds.index(wbds1) != wbds.index(wbds2)
                        and wbds.index(wbds2) != wbds.index(wbds3)
                        and wbds.index(wbds1) != wbds.index(wbds3)
                    ):
                        wbdss.append(wbds1 + wbds2 + wbds3)

                # and a child...
    kbds = [kidb_yy, kidb_yyy, kidb_yyyy, kidb_xd, kidb_xm, kidb_dd, kidb_mm]

    kbdss = []

    for kbds1 in kbds:
        kbdss.append(kbds1)
        for kbds2 in kbds:
            if kbds.index(kbds1) != kbds.index(kbds2):
                kbdss.append(kbds1 + kbds2)
                for kbds3 in kbds:
                    if (
                        kbds.index(kbds1) != kbds.index(kbds2)
                        and kbds.index(kbds2) != kbds.index(kbds3)
                        and kbds.index(kbds1) != kbds.index(kbds3)
                    ):
                        kbdss.append(kbds1 + kbds2 + kbds3)

                # string combinations....

    kombinaac = [profile["pet"], petup, profile["company"], companyup]

    kombina = [
        profile["name"],
        profile["surname"],
        profile["nick"],
        nameup,
        surnameup,
        nickup,
    ]

    kombinaw = [
        profile["wife"],
        profile["wifen"],
        wifeup,
        wifenup,
        profile["surname"],
        surnameup,
    ]

    kombinak = [
        profile["kid"],
        profile["kidn"],
        kidup,
        kidnup,
        profile["surname"],
        surnameup,
    ]

    kombinaa = []
    for kombina1 in kombina:
        kombinaa.append(kombina1)
        for kombina2 in kombina:
            if kombina.index(kombina1) != kombina.index(kombina2) and kombina.index(
                kombina1.title()
            ) != kombina.index(kombina2.title()):
                kombinaa.append(kombina1 + kombina2)

    kombinaaw = []
    for kombina1 in kombinaw:
        kombinaaw.append(kombina1)
        for kombina2 in kombinaw:
            if kombinaw.index(kombina1) != kombinaw.index(kombina2) and kombinaw.index(
                kombina1.title()
            ) != kombinaw.index(kombina2.title()):
                kombinaaw.append(kombina1 + kombina2)

    kombinaak = []
    for kombina1 in kombinak:
        kombinaak.append(kombina1)
        for kombina2 in kombinak:
            if kombinak.index(kombina1) != kombinak.index(kombina2) and kombinak.index(
                kombina1.title()
            ) != kombinak.index(kombina2.title()):
                kombinaak.append(kombina1 + kombina2)

    kombi = {}
    kombi[1] = list(komb(kombinaa, bdss))
    kombi[1] += list(komb(kombinaa, bdss, "_"))
    kombi[2] = list(komb(kombinaaw, wbdss))
    kombi[2] += list(komb(kombinaaw, wbdss, "_"))
    kombi[3] = list(komb(kombinaak, kbdss))
    kombi[3] += list(komb(kombinaak, kbdss, "_"))
    kombi[4] = list(komb(kombinaa, years))
    kombi[4] += list(komb(kombinaa, years, "_"))
    kombi[5] = list(komb(kombinaac, years))
    kombi[5] += list(komb(kombinaac, years, "_"))
    kombi[6] = list(komb(kombinaaw, years))
    kombi[6] += list(komb(kombinaaw, years, "_"))
    kombi[7] = list(komb(kombinaak, years))
    kombi[7] += list(komb(kombinaak, years, "_"))
    kombi[8] = list(komb(word, bdss))
    kombi[8] += list(komb(word, bdss, "_"))
    kombi[9] = list(komb(word, wbdss))
    kombi[9] += list(komb(word, wbdss, "_"))
    kombi[10] = list(komb(word, kbdss))
    kombi[10] += list(komb(word, kbdss, "_"))
    kombi[11] = list(komb(word, years))
    kombi[11] += list(komb(word, years, "_"))
    kombi[12] = [""]
    kombi[13] = [""]
    kombi[14] = [""]
    kombi[15] = [""]
    kombi[16] = [""]
    kombi[21] = [""]
    if profile["randnum"] == "y":
        kombi[12] = list(concats(word, numfrom, numto))
        kombi[13] = list(concats(kombinaa, numfrom, numto))
        kombi[14] = list(concats(kombinaac, numfrom, numto))
        kombi[15] = list(concats(kombinaaw, numfrom, numto))
        kombi[16] = list(concats(kombinaak, numfrom, numto))
        kombi[21] = list(concats(reverse, numfrom, numto))
    kombi[17] = list(komb(reverse, years))
    kombi[17] += list(komb(reverse, years, "_"))
    kombi[18] = list(komb(rev_w, wbdss))
    kombi[18] += list(komb(rev_w, wbdss, "_"))
    kombi[19] = list(komb(rev_k, kbdss))
    kombi[19] += list(komb(rev_k, kbdss, "_"))
    kombi[20] = list(komb(rev_n, bdss))
    kombi[20] += list(komb(rev_n, bdss, "_"))
    komb001 = [""]
    komb002 = [""]
    komb003 = [""]
    komb004 = [""]
    komb005 = [""]
    komb006 = [""]
    if len(profile["spechars"]) > 0:
        komb001 = list(komb(kombinaa, profile["spechars"]))
        komb002 = list(komb(kombinaac, profile["spechars"]))
        komb003 = list(komb(kombinaaw, profile["spechars"]))
        komb004 = list(komb(kombinaak, profile["spechars"]))
        komb005 = list(komb(word, profile["spechars"]))
        komb006 = list(komb(reverse, profile["spechars"]))

    print("[+] Sorting list and removing duplicates...")

    komb_unique = {}
    for i in range(1, 22):
        komb_unique[i] = list(dict.fromkeys(kombi[i]).keys())

    komb_unique01 = list(dict.fromkeys(kombinaa).keys())
    komb_unique02 = list(dict.fromkeys(kombinaac).keys())
    komb_unique03 = list(dict.fromkeys(kombinaaw).keys())
    komb_unique04 = list(dict.fromkeys(kombinaak).keys())
    komb_unique05 = list(dict.fromkeys(word).keys())
    komb_unique07 = list(dict.fromkeys(komb001).keys())
    komb_unique08 = list(dict.fromkeys(komb002).keys())
    komb_unique09 = list(dict.fromkeys(komb003).keys())
    komb_unique010 = list(dict.fromkeys(komb004).keys())
    komb_unique011 = list(dict.fromkeys(komb005).keys())
    komb_unique012 = list(dict.fromkeys(komb006).keys())

    uniqlist = (
        bdss
        + wbdss
        + kbdss
        + reverse
        + komb_unique01
        + komb_unique02
        + komb_unique03
        + komb_unique04
        + komb_unique05
    )

    for i in range(1, 21):
        uniqlist += komb_unique[i]

    uniqlist += (
        komb_unique07
        + komb_unique08
        + komb_unique09
        + komb_unique010
        + komb_unique011
        + komb_unique012
    )
    unique_lista = list(dict.fromkeys(uniqlist).keys())
    unique_leet = []
    if profile["leetmode"] == "y":
        for (
            x
        ) in (
            unique_lista
        ):  # if you want to add more leet chars, you will need to add more lines in cupp.cfg too...

            x = make_leet(x)  # convert to leet
            unique_leet.append(x)

    unique_list = unique_lista + unique_leet

    unique_list_finished = []
    unique_list_finished = [
        x
        for x in unique_list
        if len(x) < CONFIG["global"]["wcto"] and len(x) > CONFIG["global"]["wcfrom"]
    ]

    print_to_file(profile["name"] + ".txt", unique_list_finished)
        
    }

    # download the files

    intfiledown = int(filedown)

    if intfiledown in arguments:

        dire = "dictionaries/" + arguments[intfiledown][0] + "/"
        mkdir_if_not_exists(dire)
        files_to_download = arguments[intfiledown][1]

        for fi in files_to_download:
            url = CONFIG["global"]["dicturl"] + arguments[intfiledown][0] + "/" + fi
            tgt = dire + fi
            download_http(url, tgt)

        print("[+] files saved to " + dire)

    else:
        print("[-] leaving.")


# create the directory if it doesn't exist
def mkdir_if_not_exists(dire):
    if not os.path.isdir(dire):
        os.mkdir(dire)


# the main function
def main():
    """Interface de linha de comando para o utilitário wisefox"""

    read_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), "cupp.cfg"))

    parser = get_parser()
    args = parser.parse_args()

    if not args.quiet:
        print_cow()

    if args.version:
        version()
    elif args.interactive:
        interactive()
    elif args.download_wordlist:
        download_wordlist()
    elif args.alecto:
        alectodb_download()
    elif args.improve:
        improve_dictionary(args.improve)
    else:
        parser.print_help()


# Separate into a function for testing purposes
def get_parser():
    """Crie e retorne um analisador (instância argparse.ArgumentParser) para main()
    usar"""
    parser = argparse.ArgumentParser(description="Common User Passwords Profiler")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-p",
        "--interactive",
        action="store_true",
        help="Perguntas interativas para criação de perfil de senha de usuário",
    )
    group.add_argument(
        "-w",
        dest="improve",
        metavar="FILENAME",
        help="Use this option to improve existing dictionary,"
        " or WyD.pl output to make some pwnsauce",
   )
  

    return parser


if __name__ == "__main__":
    main()
