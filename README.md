<h1 align="center">
  Tweet Generator Learning from Timeline, Powered by GPT-2-JA
</h1>

<p align="center">
  <img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/_determina_?color=skyblue&style=social">
</p>

<h4 align="center">
  Can easily generate tweets by GPT-2 Japanese model finetuned by your timeline.
  <br>
</h4>

## Installation

### 1. Clone this repository

```zsh
git clone https://github.com/discus0434/tweetgen-from-timeline.git
cd tweetgen-from-timeline
```

### 2. Install dependencies

#### pip

```zsh
pip install -r requirements.txt
```

#### conda

```zsh
conda create -n tweetgen python=3.9
echo "source activate tweetgen" > ~/.bashrc
conda run -n tweetgen pip install -r requirements.txt
```

#### ...or build docker image

```zsh
docker build tweetgen-from-timeline/. -t tweetgen-from-timeline
docker run -it --runtime=nvidia -d --restart=always tweetgen-from-timeline:latest bash
```

### 3. Arrange Twitter API tokens

Arrange `.env` file in the project directory.
`.env` file should look like this:

```txt
API_KEY = XXX
API_SECRET_KEY = XXX
BEARER_TOKEN = XXX
ACCESS_TOKEN = XXX
ACCESS_TOKEN_SECRET = XXX
```

## Usage

All you need is write a command below:
```
python main.py & disown
```

## Acknowledgements

This code borrows from [transformers](https://github.com/huggingface/transformers).
