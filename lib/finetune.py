from __future__ import annotations

import subprocess

def finetune() -> None:
    subprocess.run(
        "python ./transformers/examples/pytorch/language-modeling/run_clm.py \
            --model_name_or_path=rinna/japanese-gpt2-small \
            --train_file=train_texts/timeline.txt \
            --do_train \
            --num_train_epochs=10 \
            --save_steps=10000 \
            --save_total_limit=3 \
            --per_device_train_batch_size=1 \
            --output_dir=finetuned_model/ \
            --overwrite_output_dir \
            --use_fast_tokenizer=False",
        shell=True,
    )
