# DESAFIO SWOT — Python + Streamlit

Jogo educacional em que o aluno vira consultor e salva empresas usando análise
SWOT/TOWS.

## Publicar no Streamlit Cloud

1. Suba este repositório para o GitHub.
2. No Streamlit Cloud, escolha o repositório e a branch.
3. Use `game-swot.py` como **Main file path**.
4. Clique em **Deploy**.

O arquivo `requirements.txt` já contém as dependências necessárias.

## Executar localmente

```bash
pip install -r requirements.txt
streamlit run game-swot.py
```

## O jogo inclui

- 3 fases: classificação, cruzamento FO/FA/WO/WA e decisão;
- 4 cases didáticos de pequenos negócios;
- pontuação, cronômetro, feedback e modo individual ou em grupo;
- bônus de votação para grupos;
- ranking persistido em `data/ranking_swot.json`;
- download do ranking completo em PDF.

O código completo do jogo está em `.conversation/game-swot.py`; o arquivo
`game-swot.py` na raiz é o ponto de entrada reconhecido pelo Streamlit Cloud.