import os

def main():
    entrada = input("Id do Servidor: ")
    try:
        with open("thisChord.txt") as restart:
            ativo = True
            while ativo:
                linha = restart.readline().split(' ',8)
                if not linha[0]:
                    ativo = False
                    break           
                elif int(entrada) == int(linha[3]):
                    os.system("start /B start cmd.exe @cmd /k python server.py " + linha[0] + " " +linha[1]+ " " +linha[2]+ " " +linha[3]+ " " +linha[4]+ " " +linha[5]+ " " +linha[6]+ " " +linha[7]+ " " +linha[8].strip("\n"))
        restart.close()
    except:
        print("Erro ao abrir Servidor")
    

if __name__ == '__main__':
    main()