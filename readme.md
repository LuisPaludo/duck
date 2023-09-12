# Projeto Final do Curso - Semeando Devs - Proposto pela empresa SoftFocus

## Descrição do Projeto

A proposta do projeto tenta solucionar os problemas apresentados quanto ao turismo de Pato Branco - PR, ao mesmo tempo que incentiva a prática na cidade. O projeto chama-se Duck GO! e está disponível no link: 

https://luispaludo.github.io/duck-go/

Como o nome sugere, trata-se de uma reimaginação do já consagrado Pokemon GO!, porém voltado apenas para o turismo da cidade de Pato Branco. Duck GO! é um web app de simples funcionamento: Os usuários leem QR Codes em pontos turísticos e acumulam pontos que podem ser trocados por prêmios no comércio local.

Vou detalhar o funcionamento e explicar quais problemas busco resolver com o projeto:

- De ínicio, para poder utilizar o aplicativo, o usuário necessita efetuar um cadastro no aplicativo, assim, coletamos as informações de quem estará utilizando. Isso permite conhecer quem, quando e de onde são as pessoas que compõe o fluxo turístico de Pato Branco.
- Com a Conta criada e verificada, o usuário pode começar a acumular pontos.
- Os pontos podem ser obtidos da seguinte forma: O usuário visita um dos pontos turísticos apresentados na aba "Locais de Caça". Ao chegar no ponto, deve buscar por QR Codes escondidos próximos de Atrações Turísticas. Escaneando o QR Codes os pontos serão automaticamente adicionados a conta.
- Após uma quantida de pontos atingida, ele pode trocar por prêmios, localizados na aba "Lista de Prêmios".

A ideia principal é a de incentivar a visitação de pontos turísticos diversos na cidade, propondo uma recompensa para a ação dos usuários.

Além de usuários convencionais, o sistema possui suporte a Usuários Parceiros, sendo esses, contas que não irão acumular pontos e sim, criar prêmios para usuários convencionais poderem realizar a troca, além de, validar os prêmios criados e permitir a implementação dos descontos na vida real.

Para obter uma conta parceira, somente é possível entrando em contato com o administrador do sistema, não existe um cadastro para parceiros no momento.

## Framework Utilizado

O back end do projeto foi inteiramente produzido com o framework Django. O Servidor está rodando atualmente no RailWay, com armazenamento do banco de dados no RCD da Amazon, além de também armazenar as imagens no S3, também da Amazon.

Obs: Maiores comentários estarão posicionados no código do projeto, aqui é apresentada apenas uma breve descrição.

O projeto conta com 3 apps principais:

- **user_data**: Responsável pelo armazenamento das informações dos usuários, bem como seus históricos de ações.
- **prizes**: Responsável pelo sistema de prêmios do projeto.
- **Locations**: Resposável pelos locais turísticos e suas atrações.

# user_data

Esse app gira em torno de duas models: CustomUser e History.

- **CustomUser**: é uma extensão da classe de usuário padrão, acrescentando diversos campos de cadastro. 
- **History**: Aqui ficarão registradas todas as ações do usuário, desde aquisições de pontos, até obtenção de prêmios e validação dos prêmios com a empresa.

# prizes

Aqui existem três models:

- **Prizes**: Referente aos prêmios disponíveis para os usuários (Criados pelos parceiros).
- **PrizesCategorys**: Categorias de prêmios
- **UserRedeemedPrizes**: Prêmios resgatados pelos usuários. Cada usuário pode resgatar apenas uma instância de cada prêmio, e, cada resgate irá gerar um código único, que será utilizado no processo de validação do prêmio na hora da retirada com a empresa que o criou.

# Locations

Por fim, o app é composto por duas models:

- **Locations**: Refere-se aos locais turísticos da cidade, estes locais que abrigam os pontos turísticos.
- **TouristAttractions**: Refere-se aos pontos turísticos. Cada ponto é associado a um código, que então produz um QR Code único. A leitura do QR Code próximo das coordenadas do local, valida a quantia de pontos a serem adicionadas a conta do usuário.





