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

CONFIG = {}

def read_config(filename):
    """Leia o arquivo de configuração fornecido e atualize as variáveis ​​globais para refletir
    mudanças(CONFIG)."""
    
    
    if os.path.isfile(filename):
    
    # CONFIG global
    
    # Lendo o arquivo de configuração
    
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
        }
        
               # 1337 configurações do modo, bem, você pode adicionar mais linhas se adicioná-lo ao
        # arquivo de configuração também.
        
        
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
    """converter string para let"""
    for letter, leetletter in CONFIG["LEET"].items():
        x = x.replace(letter, leetletter)
    return x
  
  
  # para concatenações...
def concats(seq, start, stop):
    for mystr in seq:
        for num in range(start, stop):
            yield mystr + str(num)
            
            # para classificar e fazer combinações...
def komb(seq, start, special=""):
    for mystr in seq:
        for mystr1 in start:
            yield mystr + special + mystr1

            # lista de impressão para palavras de contagem de arquivos
            
            # imprimir lista para arquivo contando palavras

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
        "[+] Salvando dicionário para \033[1;31m"
        + filename
        + "\033[1;m, contando \033[1;31m"
        + str(lines)
        + " words.\033[1;m"
    )
    
        inspect = input(">Ver Senha Ao Vivo? (Y/N) : ").lower()
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
    print(28 * " " + "[ GILMAR SCRIPT | https://github.com/gilmarscript/]\r\n")
    
    
    conts = input(
        ">Deseja concatenar todas as palavras da lista de palavras? Y/[N]: "
    ).lower()

    
    if conts == "y" and len(listic) > CONFIG["global"]["threshold"]:
        print(
            "\r\n[-] O número máximo de palavras para concatenação é "
            + str(CONFIG["global"]["threshold"])
        )
        print("[-] Verifique o arquivo de configuração para aumentar este número.\r\n")
        conts = input(
            "> Deseja concatenar todas as palavras da lista de palavras? Y/[N]: "
        ).lower()

        
           cont = [""]
    if conts == "y":
        for cont1 in listica:
            for cont2 in listica:
                if listica.index(cont1) != listica.index(cont2):
                    cont.append(cont1 + cont2)
                    
                    
    spechars = [""]
    spechars1 = input(
        "> Deseja adicionar caracteres especiais no final das palavras? Y/[N]: "
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
            
            
            

    print("\r\n[+] Agora fazendo um dicionário...")

    print("[+] Lista de classificação e remoção de duplicatas...")
