import os
import json

def criar_pasta():
    if not os.path.exists("salas_aula"):
        os.makedirs("salas_aula")

def obter_caminho_sala(numero_sala):
    return os.path.join("salas_aula", f"sala_{numero_sala}.json")

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
    numero_sala = input("Digite o número da sala: ")
    dados_sala = carregar_sala(numero_sala)
    
    if dados_sala is None:
        print(f"Criando cadastro para a Sala {numero_sala}.")
        dados_sala = {}
    else:
        print(f"Editando a Sala {numero_sala} existente.")
    
    qtd_alunos = int(input("Quantos alunos deseja cadastrar/atualizar nesta sala? "))
    
    for _ in range(qtd_alunos):
        nome = input("Digite o nome do aluno: ")
        notas = []
        for i in range(1, 7):
            nota = float(input(f"Digite a nota {i} de {nome}: "))
            notas.append(nota)
        dados_sala[nome] = notas
        
    salvar_sala(numero_sala, dados_sala)
    print(f"Dados da Sala {numero_sala} salvos com sucesso!")

def visualizar_desempenho_alunos():
    numero_sala = input("Digite o número da sala que deseja consultar: ")
    dados_sala = carregar_sala(numero_sala)
    
    if dados_sala is None:
        print("Sala não encontrada!")
        return
        
    print(f"\n--- Relatório de Alunos - Sala {numero_sala} ---")
    for nome, notas in dados_sala.items():
        maior_nota = max(notas)
        menor_nota = min(notas)
        media = sum(notas) / len(notas)
        print(f"Aluno(a): {nome}")
        print(f"  > Maior Nota: {maior_nota}")
        print(f"  > Menor Nota: {menor_nota}")
        print(f"  > Média: {media:.2f}")
        print("-" * 30)

def visualizar_media_geral_turma():
    numero_sala = input("Digite o número da sala para ver a média geral: ")
    dados_sala = carregar_sala(numero_sala)
    
    if dados_sala is None:
        print("Sala não encontrada!")
        return
        
    soma_todas_notas = 0
    total_notas = 0
    
    for notas in dados_sala.values():
        soma_todas_notas += sum(notas)
        total_notas += len(notas)
        
    if total_notas == 0:
        print("Esta sala não possui notas cadastradas.")
        return
        
    media_geral = soma_todas_notas / total_notas
    print(f"\nA média geral da Sala {numero_sala} é: {media_geral:.2f}")


def excluir_sala():
    numero_sala = input("Digite o número da sala que deseja excluir: ")
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
        print("4. Excluir sala")
        print("5. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_ou_editar_sala()
        elif opcao == "2":
            visualizar_desempenho_alunos()
        elif opcao == "3":
            visualizar_media_geral_turma()
        elif opcao == "4":
            excluir_sala()
        elif opcao == "5":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.")

menu_principal()