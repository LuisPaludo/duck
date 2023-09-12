# **Duck GO!**: Projeto Final - Semeando Devs
> Proposto pela empresa SoftFocus

## 📌 **Visão Geral**
O **Duck GO!** é uma solução inovadora voltada para o incentivo e enriquecimento do turismo em Pato Branco - PR. Inspirado pelo conceito de Pokémon GO!, este projeto visa não apenas promover o turismo, mas também integrar a comunidade local através de recompensas tangíveis.

**[Acessar o Duck GO!](https://luispaludo.github.io/duck-go/)**

## 🌟 **Funcionalidades**

### 1. **Cadastro de Usuário**
- Coleta de informações do usuário para entender o fluxo e perfil dos turistas.
- Suporte para dois tipos de contas: **Usuários Convencionais** e **Usuários Parceiros**.

### 2. **Acúmulo de Pontos**
- Os usuários exploram locais turísticos, escaneiam QR Codes e acumulam pontos.

### 3. **Troca de Prêmios**
- Pontos podem ser trocados por prêmios no comércio local.

### 4. **Usuários Parceiros**
- Contas dedicadas à criação e oferta de prêmios.
- Não acumulam pontos, mas validam prêmios para os usuários convencionais.

### 5. **Administração**
- Contas parceiras só podem ser criadas através do administrador do sistema.

## 🛠 **Tecnologias e Frameworks**

- **Backend**: Construído com o framework **Django**.
- **Hospedagem**: Servidor no **RailWay**.
- **Banco de Dados**: Armazenado no **RCD da Amazon**.
- **Armazenamento de Imagens**: Utilizando o **Amazon S3**.

## 🔍 **Estrutura do Projeto**

### 1. **user_data**
- **Models**:
  - **CustomUser**: Extensão do modelo de usuário padrão do Django, com campos de cadastro adicionais.
  - **History**: Registra atividades do usuário, desde aquisição de pontos até resgate de prêmios.

### 2. **prizes**
- **Models**:
  - **Prizes**: Refere-se aos prêmios disponíveis, criados pelos parceiros.
  - **PrizesCategorys**: Classificações de prêmios.
  - **UserRedeemedPrizes**: Prêmios que os usuários resgataram, gerando um código único para validação.

### 3. **Locations**
- **Models**:
  - **Locations**: Representa os locais turísticos de Pato Branco.
  - **TouristAttractions**: Representa os pontos turísticos, associados a códigos QR únicos.

## 📝 **Notas Adicionais**
- Todos os detalhes técnicos, especificações e comentários mais profundos sobre o código podem ser encontrados diretamente no código fonte.
- Esta descrição é apenas um panorama para facilitar a compreensão da estrutura e da funcionalidade do projeto.

## Metas do Projeto

| Meta                                 | Status          |
| ------------------------------------ | --------------  |
| MVP                                  | ✅ Superada     |
| Testes                               | ⌛ Em Progresso |
| Sistema de Conquistas                | ❌ Não Superada |
| Melhorias no código                  | ❌ Não Superada |
