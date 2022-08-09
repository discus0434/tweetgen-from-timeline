from __future__ import annotations

import re
import time
import random

import torch
from transformers import T5Tokenizer, AutoModelForCausalLM

from lib import make_client, get_tweets_from_timeline, finetune

NUM_UPDATE_PER_DAY = 2
NUM_TWEETS_PER_DAY = 96


class TweetGenerator:
    def __init__(self):

        # make tweepy.Client object
        self.client = make_client()

        # Fetch tweets
        get_tweets_from_timeline(self.client, max_tweets=400)

        # Finetune and overwrite existing model
        finetune()

        # Read new tweets from timeline to set prompt
        with open("./train_texts/timeline_today.txt", "r") as f:
            self.data = f.readlines()

        # Prepare model for generation
        self.tokenizer, self.model, self.device = self.set_model_to_device()

    @staticmethod
    def set_model_to_device() -> tuple[T5Tokenizer, AutoModelForCausalLM, torch.device]:
        """Set tmodel to device."""
        tokenizer = T5Tokenizer.from_pretrained("rinna/japanese-gpt2-small")
        tokenizer.do_lower_case = True
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = AutoModelForCausalLM.from_pretrained("finetuned_model/")
        model = model.to(device)
        model.eval()

        return tokenizer, model, device

    def generate(self) -> str:
        prompt = ""
        while not prompt:
            prompt = (
                random.choice(self.data)
                .replace("<s>", "")
                .replace("</s>", "")
                .replace("\n", "")
            )

        if len(prompt) > 10:
            prompt = prompt[:10]

        input_ids = self.tokenizer.encode(
            prompt, return_tensors="pt", add_special_tokens=False
        ).to(self.device)

        with torch.no_grad():
            output = self.model.generate(
                input_ids,
                max_length=60,
                min_length=15,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                bos_token_id=self.tokenizer.bos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                bad_word_ids=[[self.tokenizer.unk_token_id]],
                repetition_penalty=0.99,
                num_return_sequences=1,
            )

        return self.tokenizer.batch_decode(output, skip_special_tokens=True)[0]

    def post_tweet(self) -> None:
        json = {}

        while True:
            text = self.generate()

            if (
                not bool(re.search("|".join(["rt", "http", "." "@", "殺"]), text))
                and len(text) < 139
            ):
                break

        json["text"] = text

        return self.client._make_request("POST", "/2/tweets", json=json, user_auth=True)


def main():
    while True:
        tweet_generator = TweetGenerator()

        for _ in range(NUM_TWEETS_PER_DAY // NUM_UPDATE_PER_DAY):
            tweet_generator.post_tweet()
            time.sleep(86400 // NUM_TWEETS_PER_DAY)

        del tweet_generator


if __name__ == "__main__":
    main()
