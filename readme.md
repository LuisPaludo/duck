# Duck GO! - Documentação Técnica

## Sumário

1. [Introdução](#introdução)
2. [Configuração](#configuração)
3. [Apps](#apps)
    - [user_data](#user_data)
    - [prizes](#prizes)
    - [locations](#locations)

## Introdução

O projeto **Duck GO!** é um webapp desenvolvido com Django, cujo principal objetivo é promover o turismo em Pato Branco. Baseado na ideia do popular jogo Pokémon GO, o projeto visa incentivar visitas a pontos turísticos, permitindo que os visitantes acumulem pontos através da leitura de QR Codes espalhados pelos locais. Esses pontos podem ser trocados por prêmios, incentivando ainda mais a exploração da cidade.

## Configuração

- **Banco de Dados**: Hospedado no RDS da Amazon.
- **Armazenamento de Imagens**: Utilizando o S3 da AWS.
- **Servidor**: Hospedado no Railway.
- **Autenticação**: Implementado utilizando a biblioteca `rest_auth` e `rest_framework`, com sistema de tokens (acesso e refresh).

## Apps e seus principais serlializadores/viewsets

### user_data

#### Modelos

- **CustomUser**: 
    - Modelo personalizado que representa um usuário, podendo ser um usuário regular ou um parceiro.
    - Campos: `username`, `first_name`, `last_name`, `email`, `cep`, `cpf`, `cnpj`, `address_street`, `address_state`, `address_city`, `profile_photo`, `birth_date`, `is_partner`, `partner_company_name`, `partner_email_contact`, `partner_number_contact`, `partner_company_description` e `partner_company_name_slug`.
    - O campo `is_partner` indica se o usuário é um parceiro.
    - Parceiros possuem campos adicionais, como nome da empresa, contato e descrição da empresa.
    - A geração do campo slug facilita a navegação e busca por parceiros.

- **History**:
    - Armazena o histórico de ações do usuário.
    - Campos: `date`, `points`, `total_points` e `description`.
    - O campo `total_points` é apenas para leitura e é calculado no servidor.

#### Serializadores

- **CustomUserSerializer**:
    - Serializa o modelo `CustomUser`.
    - Retorna campos que representam as informações do usuário.
    - O campo `is_partner` é somente para leitura.

- **HistorySerializer**:
    - Serializa o modelo `History`.
    - Retorna campos relacionados ao histórico de ações do usuário.

#### ViewSets

- **CustomUserViewSet**:
    - Manipula e lista informações dos usuários.
    - Utiliza autenticação por token.

- **HistoryViewSet**:
    - Lista o histórico de ações de um usuário.

- **PartnerDetailsViewSet**:
    - Fornece detalhes sobre um parceiro específico.
    - Filtra os parceiros usando o campo slug.

### prizes

#### Modelos

- **PrizeCategory**:
    - Define categorias para prêmios.
    - Campos: `name`.

- **Prizes**:
    - Representa os prêmios disponíveis para resgate.
    - Campos: `name`, `description`, `generated_by`, `generated_by_slug`, `times_to_be_used`, `times_used`, `cost_in_points`, `category`, `logo`, `expiry_date`, `disabled`.

- **UserRedeemedPrizes**:
    - Representa os prêmios que foram resgatados por usuários.
    - Campos: `user`, `prize`, `redeemed_at`, `code`, `qr_code`, `is_used`.

#### Serializadores

- **PrizesSerializer**:
    - Serializa o modelo `Prizes`.
    - Retorna todos os campos associados ao prêmio.

- **UserRedeemedPrizesSerializer**:
    - Serializa o modelo `UserRedeemedPrizes`.
    - Retorna informações sobre os prêmios resgatados.

#### ViewSets

- **PrizesViewSet**:
    - Lista e manipula prêmios disponíveis.
    - Utiliza o `PrizesSerializer` para serialização.

- **UserRedeemPrizeViewSet**:
    - Permite que os usuários resgatem prêmios.
    - Usa autenticação por token.

- **PartnerRedeemPrizeViewSet**:
    - Permite que os parceiros validem os prêmios resgatados pelos usuários.

### locations

#### Modelos

- **Location**:
    - Armazena os principais pontos turísticos da cidade.
    - Campos: `name`, `resume`, `description`, `review_link`, `map_link`, `coordinates_lat`, `coordinates_long`, `slug_field`, `photo_1`, `photo_2`, `photo_3`.

- **TouristAttraction**:
    - Representa pontos turísticos específicos associados a uma `Location`.

#### Serializadores

- **LocationSerializer**:
    - Serializa o modelo `Location`.
    - Retorna todos os campos associados ao ponto turístico principal.

- **TouristAttractionSerializer**:
    - Serializa o modelo `TouristAttraction`.
    - Retorna todos os campos associados ao ponto turístico específico.

#### ViewSets

- **LocationViewSet**:
    - Lista os principais pontos turísticos da cidade.
    - Não requer autenticação.

- **TouristAttractionViewSet**:
    - Lista pontos turísticos específicos associados a uma `Location`.
    - Requer autenticação e suporta a filtragem de dados com base no campo `code`.

# Tutorial de Teste para o Aplicativo Duck GO!

Siga os passos abaixo para testar todas as funcionalidades do aplicativo Duck GO!.

## 1. Acesso ao WebApp

- Acesse o aplicativo através do link: [https://luispaludo.github.io/duck-go](https://luispaludo.github.io/duck-go)

## 2. Criação de Contas

- Crie **duas contas**:
    1. A primeira conta será um **usuário normal**.
    2. A segunda conta será um **usuário parceiro**.
- Para criar as contas, serão necessários 2 emails. Execute a verificação em ambos os emails.

> Nota: Se preferir, você também pode utilizar as contas já criadas que foram fornecidas anteriormente.

## 3. Acesso ao Admin

- Clone o repositório do servidor do backend para a sua máquina.
- Navegue até o diretório do projeto.
- Crie um ambiente virtual (venv) para isolar as dependências.
- Instale os requerimentos do projeto.
- Execute o servidor localmente.
  > Nota: O acesso ao servidor local é necessário devido a problemas de acesso pelo servidor hospedado. Esta é uma solução temporária para edição do banco de dados.
- Acesse a interface de administração do Django em [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).
- Utilize as credenciais do super usuário fornecidas para fazer o login.

## 4. Tornando um Usuário em Parceiro

- No painel de administração, vá para `user_data` -> `users`.
- Escolha o usuário que deseja transformar em parceiro.
- Na página de edição, marque a caixa de seleção `is_partner`.
- Salve as alterações.

## 5. Coletando Coordenadas

- Acesse [https://browserleaks.com/geo](https://browserleaks.com/geo) e colete as coordenadas do seu local atual.
  - Recomendamos que faça isso com o celular para obter maior precisão.

## 6. Adicionando um Ponto Turístico

- No painel de Admin do Django, vá para `locations` e depois em `touristAtractions` para adicionar um novo ponto turístico.
- Preencha os campos necessários. Exclua os campos `code` e `qr code` (eles serão preenchidos automaticamente ao salvar).
- Adicione as coordenadas que você coletou no passo 5.
- Salve e acesse o ponto turístico criado. Copie o link em `QR_code` e salve-o para uso futuro.

## 7. Resgatando Pontos

- Acesse [https://luispaludo.github.io/duck-go](https://luispaludo.github.io/duck-go) e faça login com sua conta de usuário.
- Na página inicial, clique no botão da câmera e leia o QR Code que você criou no passo 6.
- Uma mensagem de sucesso aparecerá, indicando que os pontos foram adicionados à sua conta.
- Vá para o perfil e na aba `histórico`, verifique se os pontos foram adicionados.

## 8. Acessando como Parceiro

- Deslogue da conta do usuário e faça login com a conta do parceiro.

## 9. Atualizando Perfil do Parceiro

- Na aba `perfil`, complete as informações que faltam.

## 10. Criando um Prêmio

- Vá para a aba `criar prêmio` e crie um prêmio para os usuários resgatarem.

## 11. Resgatando Prêmio como Usuário

- Deslogue da conta do parceiro e faça login com a conta do usuário.
- Vá para a lista de prêmios e, se tiver pontos suficientes, resgate o prêmio criado na etapa 10.

## 12. Verificando o Cupom Resgatado

- Acesse seu perfil e na aba `cupons`, verifique se o cupom resgatado está lá.
- Acesse o QR Code do prêmio resgatado e salve a imagem.

## 13. Validando o Cupom como Parceiro

- Deslogue da conta do usuário e faça login novamente como parceiro.
- Na página inicial, clique no botão da câmera e leia o QR Code do usuário.

---

**Outras Funcionalidades**:
- Reenviar email de verificação.
- Trocar de senha.
- Resetar a senha.
- Conhecer os locais turísticos.
- Acessar informações das empresas parceiras.

---


