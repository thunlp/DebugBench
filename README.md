# Repo of DebugBench

<img src="figs/icon.png" style="width: 20vw; height: auto;" alt="icon"> 

### Overview

Implementation for paper DebugBench: Evaluating Debugging Capabilities of Large Language Models with datasets, prompts, model outputs.



### Benchmark

Please refer to the [Hugging Face Dataset](https://huggingface.co/datasets/Rtian/DebugBench) for the data source and evaluation script if you want to use the benchmark.

DebugBench is a Large Language Model (LLM) debugging benchmark introduced in the paper "DebugBench: Evaluating Debugging Capability of Large Language Models" [url]. We collect code snippets from the [LeetCode](https://leetcode.com/) community and implant bugs into source data with [GPT-4](https://openai.com/research/gpt-4). 

- It consists of 4,253 instances.
- It covers four major bug categories and 18 minor types.
- It includes C++, Java, and Python instances.
- It contains three difficulty levels: easy, medium, and hard.
- All the instances were released after June 2022.
- Please refer to the article [url] for more details.



### Repo Content

This repository contains the implementation for benchmark construction and evaluation.

- `benchmark` directory contains the 51 JSON shards of different languages and bug types of the benchmark. 
- `dataset_construction` directory contains the implementation for bug implantation to solution code via LLMs.

- `evaluation` directory contains the implementation for evaluating the debugging capabilities of LLMs with API. 
- `evalution_result` directory contains the model output of `gpt-4-0613` ,  `gpt-3.5-turbo-0613`  and `CodeLlama-34b-instruct` under different scenarios. 

More elements will be added to the repository soon.



### Citations

Please cite the paper and star the repo if you use DebugBench and find it helpful.

Feel free to contact trc20@mails.tsinghua.edu.cn or open an issue if you have any questions.

```latex
The preprint version is coming soon.
```
