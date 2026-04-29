# Computação Grafica

Projeto de estudos da disciplina de Computacao Grafica usando Python + OpenGL.
O repositorio esta organizado por aulas (`aula1` a `aula5`), com exercicios de renderizacao 2D e 3D, transformacoes, camera e carregamento de modelos `.obj`.

## Estrutura do projeto

- `aula1/`: primeiros exemplos com OpenGL (ex.: desenho de quadrado).
- `aula2/`: primitivas e cenas 2D com GLFW (triangulos, formas e composicao).
- `aula3/`: carregamento de objetos 3D (`.obj`) com `PyWavefront`.
- `aula4/`: transformacoes e hierarquia de modelos (carro e rodas).
- `aula5/`: continuidade da cena 3D com camera/visualizacao.
- `requirements.txt`: dependencias Python do projeto.

## Requisitos

- Python 3.10+ (recomendado 3.12)
- Sistema com suporte a OpenGL
- `pip` instalado

## Instalacao

### 1) Clonar o repositorio

```bash
git clone <URL_DO_REPOSITORIO>
cd ComputacaoGrafica
```

### 2) Criar e ativar ambiente virtual (Windows PowerShell)

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3) Instalar dependencias

```bash
pip install -r requirements.txt
```

## Dependencias principais

- `glfw==2.10.0`
- `PyOpenGL==3.1.10`
- `PyOpenGL-accelerate==3.1.10`
- `PyWavefront==1.3.3`

## Como executar

Execute os scripts a partir da pasta correta da aula (alguns arquivos `.obj` sao carregados por caminho relativo).

### Exemplo 1: Aula 1

```bash
python aula1/quadradov1.py
```

### Exemplo 2: Aula 3 (carregando OBJ)

```bash
cd aula3
python carrega_obj3.py
```

### Exemplo 3: Aula 4 (carro 3D)

```bash
cd aula4
python carroAt.py
```

## Controles (quando aplicavel)

Nos exemplos de carro (`carroAt.py`):

- `Seta para cima`: mover para frente
- `Seta para baixo`: mover para tras
- `Seta para esquerda/direita`: girar direcao

## Observacoes

- Muitos scripts usam OpenGL no modo imediato (`glBegin/glEnd`), com foco didatico.
- Alguns exemplos dependem de arquivos `.obj` estarem no mesmo diretorio do script.
- Se houver erro de contexto OpenGL, verifique driver de video e suporte da maquina.

## Materiais de apoio

As pastas das aulas incluem PDFs usados em aula para consulta teorica.

## Licenca

Uso academico/educacional.
