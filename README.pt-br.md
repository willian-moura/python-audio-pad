# python-audio-pad
  ![Python SoundTable](/images/example.png)
***

## Requerimentos
- python3
- pygame

## Instalação
`$ git clone git@github.com:willian-moura/python-audio-pad.git`

`$ cd python-audio-pad`

`$ python3 -m pip install pygame`

`$ python3 main.py`

Tendo o objetivo principal de simular uma mesa de som, a aplicação oferece ao usuário um total de 24 canais, onde cada um conta com as seguintes funções:
- Play/pause: tocar/pausar a faixa no canal selecionado;
- Stop: para a faixa completamente, não sendo possível continuar executando-a de onde parou;
- Loop: com essa opção habilitada, a faixa iniciará novamente de forma automática após terminar;
- Volume: controla o volume do canal;
- Fechar: remove a faixa do canal selecionado, deixando-o livre para que outra faixa possa ser adicionada a ele.

Os arquivos de áudio devem ser primeiramente adicionados à lista posicionada no lado esquerdo, que conta com os seguintes botões:
- Add: adiciona um arquivo de áudio à lista;
- Del: remove um arquivo de áudio da lista;
- Musics: adiciona o arquivo de áudio selecionado ao primeiro canal disponível da sessão Musics;
- Environments: adiciona o arquivo de áudio selecionado ao primeiro canal disponível da sessão Environments;
- Effects: adiciona o arquivo de áudio selecionado ao primeiro canal disponível da sessão Effects.

**A aplicação só aceita arquivos nos formatos OGG ou WAV**, para arquivos MP3, converta-os com o conversor disponível na aplicação.

## Usando no RPG
O Python SoundTable funciona muito bem na sonorização de partidas de RPG, proporcionando o controle de diversas faixas de áudio simultâneas, perfeito para quem precisa tocar um efeito de porta abrindo, enquanto toca uma música de fundo e uma faixa com o som ambiente de uma taverna, por exemplo.



