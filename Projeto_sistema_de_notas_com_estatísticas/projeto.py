import os
import json

def criar_pasta():
    if not os.path.exists("salas_de_aula"):
        os.makedirs("salas_de_aula")

def obter_caminho_sala(numero_sala):
    return os.path.join("salas_de_aula", f"sala_{numero_sala}.json")

def carregar_sala(numero_sala):
    caminho = obter_caminho_sala(numero_sala)
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return None

def salvar_sala(numero_sala, dados_sala):
    caminho = obter_caminho_sala(numero_sala)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados_sala, arquivo, indent=4, ensure_ascii=False)

def cadastrar_ou_editar_sala():
    numero_sala = input("Digite o número da sala: ").strip()
    if not numero_sala:
        print("Número da sala inválido.")
        return

    dados_sala = carregar_sala(numero_sala)
    
    if dados_sala is None:
        print(f"\nCriando cadastro para a Sala {numero_sala}.")
        dados_sala = {}
    else:
        print(f"\nEditando a Sala {numero_sala} existing.")
    
    while True:
        try:
            qtd_alunos = int(input("Quantos alunos deseja cadastrar/atualizar nesta sala? "))
            if qtd_alunos > 0:
                break
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")
    
    for _ in range(qtd_alunos):
        while True:
            nome = input("\nDigite o nome do aluno: ").strip()
            while not nome:
                nome = input("O nome não pode ser vazio. Digite o nome do aluno: ").strip()
            
            nome_existe = False
            for nome_existente in dados_sala.keys():
                if nome_existente.strip().lower() == nome.lower():
                    nome_existe = True
                    break
            
            if nome_existe:
                print("Erro: Este nome de aluno já está cadastrado nesta sala. Tente outro nome.")
            else:
                break
                
        notas = []
        for i in range(1, 7):
            while True:
                try:
                    nota = float(input(f"Digite a nota {i} de {nome} (0 a 10): "))
                    if 0 <= nota <= 10:
                        notas.append(nota)
                        break
                    print("Nota inválida! A nota deve ser entre 0 e 10.")
                except ValueError:
                    print("Entrada inválida! Digite um número (ex: 7.5).")
                    
        dados_sala[nome] = notas
        
    salvar_sala(numero_sala, dados_sala)
    print(f"\nDados da Sala {numero_sala} salvos com sucesso!")

def visualizar_desempenho_alunos():
    numero_sala = input("Digite o número da sala que deseja consultar: ").strip()
    dados_sala = carregar_sala(numero_sala)
    
    if dados_sala is None or not dados_sala:
        print("\nSala não encontrada ou sem alunos cadastrados!")
        return
        
    print(f"\n--- Relatório de Alunos - Sala {numero_sala} ---")
    for nome, notas in dados_sala.items():
        if not notas:
            print(f"Aluno(a): {nome} -> Sem notas cadastradas.")
            continue
            
        maior_nota = max(notas)
        menor_nota = min(notas)
        media = sum(notas) / len(notas)
        print(f"Aluno(a): {nome}")
        print(f"  > Maior Nota: {maior_nota}")
        print(f"  > Menor Nota: {menor_nota}")
        print(f"  > Média: {media:.2f}")
        print("-" * 30)

def visualizar_media_geral_turma():
    numero_sala = input("Digite o número da sala para ver a média geral: ").strip()
    dados_sala = carregar_sala(numero_sala)
    
    if dados_sala is None:
        print("\nSala não encontrada!")
        return
        
    soma_todas_notas = 0
    total_notas = 0
    
    for notas in dados_sala.values():
        soma_todas_notas += sum(notas)
        total_notas += len(notas)
        
    if total_notas == 0:
        print("\nEsta sala não possui notas cadastradas.")
        return
        
    media_geral = soma_todas_notas / total_notas
    print(f"\nA média geral da Sala {numero_sala} é: {media_geral:.2f}")

def excluir_aluno():
    numero_sala = input("Digite o número da sala onde o aluno está matriculado: ").strip()
    dados_sala = carregar_sala(numero_sala)
    
    if dados_sala is None:
        print("\nSala não encontrada!")
        return
        
    nome_aluno = input("Digite o nome do aluno que deseja excluir: ").strip().lower()
    
    aluno_encontrado = None
    for nome_original in dados_sala.keys():
        if nome_original.strip().lower() == nome_aluno:
            aluno_encontrado = nome_original
            break
            
    if aluno_encontrado:
        dados_sala.pop(aluno_encontrado)
        salvar_sala(numero_sala, dados_sala)
        print(f"\nAluno '{aluno_encontrado}' excluído com sucesso!")
    else:
        print(f"\nAluno não foi encontrado nesta sala. Verifique a grafia.")

def excluir_sala():
    numero_sala = input("Digite o número da sala que deseja excluir: ").strip()
    caminho = obter_caminho_sala(numero_sala)
    
    if os.path.exists(caminho):
        os.remove(caminho)
        print(f"Sala {numero_sala} excluída com sucesso!")
    else:
        print("\nSala não encontrada!")

def menu_principal():
    criar_pasta()
    while True:
        print("\n=== MENU DE GERENCIAMENTO DE SALAS ===")
        print("1. Cadastrar ou Editar uma Sala")
        print("2. Ver Notas, Médias, Maior e Menor por Aluno")
        print("3. Ver Média Geral de uma Turma")
        print("4. Excluir um Aluno específico")
        print("5. Excluir uma Sala inteira")
        print("6. Sair")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            cadastrar_ou_editar_sala()
        elif opcao == "2":
            visualizar_desempenho_alunos()
        elif opcao == "3":
            visualizar_media_geral_turma()
        elif opcao == "4":
            excluir_aluno()
        elif opcao == "5":
            os.system('cls' if os.name == 'nt' else 'clear')
            excluir_sala()
        elif opcao == "6":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu_principal()