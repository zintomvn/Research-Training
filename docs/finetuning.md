# Complete Guide to Fine-Tuning Techniques

> A practical English reference for transfer learning, modern Transformer fine-tuning, parameter-efficient fine-tuning, LLM post-training, evaluation, and deployment.

---

## 1. What Fine-Tuning Means

**Fine-tuning** is the process of taking a pretrained model and continuing training it on a new dataset, task, domain, or instruction style. Instead of learning from random initialization, the model starts from weights that already contain useful representations.

In practice, fine-tuning is used because it usually:

- reduces training time;
- requires less labeled data than training from scratch;
- improves task-specific performance;
- allows reuse of powerful pretrained backbones;
- makes large models adaptable to specialized domains.

A simple view:

```text
Pretrained model + task/domain data + training strategy = fine-tuned model
```

Fine-tuning is not one single technique. It is a family of strategies that differ in **which parameters are updated**, **what data is used**, **what objective is optimized**, and **how much compute is required**.

---

## 2. High-Level Taxonomy

| Category | Main idea | Typical use case |
|---|---|---|
| Feature extraction | Freeze the pretrained model and train only a new head | Small dataset, fast baseline |
| Partial fine-tuning | Unfreeze only some upper layers | Medium dataset, limited compute |
| Full fine-tuning | Update all model parameters | Large dataset, strong GPU, domain shift |
| Gradual unfreezing | Unfreeze layers step by step | Stable adaptation |
| Discriminative learning rates | Use different learning rates for different layers | Avoid destroying pretrained features |
| Continued pretraining | Train on domain text/images before task fine-tuning | Domain adaptation |
| Task-specific supervised fine-tuning | Train on labeled input-output pairs | Classification, QA, chatbot behavior |
| PEFT | Train only small extra parameters | LLMs and large foundation models |
| Preference fine-tuning | Train from preferred vs rejected outputs | Alignment, helpfulness, style control |
| Multimodal fine-tuning | Adapt models across image-text-audio-video | VLMs, retrieval, captioning, assistants |

---

## 3. Classic Transfer Learning Techniques

### 3.1 Feature Extraction / Linear Probing

**Idea:** Freeze the pretrained backbone and train only a newly added classifier/regressor head.

Example:

```text
Pretrained ResNet / BERT / ViT
→ freeze backbone
→ replace output head
→ train only the head
```

This is sometimes called:

- feature extraction;
- linear probing;
- head-only fine-tuning;
- frozen backbone training.

**When to use:**

- Your dataset is small.
- The new task is similar to the pretraining task.
- You need a quick baseline.
- You have limited GPU memory.

**Advantages:**

- Cheap and fast.
- Lower risk of overfitting.
- Easy to debug.
- Good baseline before deeper fine-tuning.

**Limitations:**

- The backbone cannot adapt deeply.
- Performance may plateau if the domain is different.

---

### 3.2 Partial Fine-Tuning

**Idea:** Freeze most of the model and unfreeze only the last few layers plus the output head.

Example for CNNs:

```text
Freeze early convolution blocks
Unfreeze final block + classifier
```

Example for Transformers:

```text
Freeze embeddings + early transformer blocks
Unfreeze final transformer blocks + task head
```

**When to use:**

- Dataset is medium-sized.
- Task is related but not identical to the pretrained task.
- Full fine-tuning is too expensive.
- You want more adaptability than linear probing.

**Advantages:**

- Better adaptation than head-only training.
- Cheaper than full fine-tuning.
- Less likely to destroy general features.

**Limitations:**

- Choosing which layers to unfreeze requires experiments.
- Too few trainable layers may underfit.
- Too many trainable layers may overfit.

---

### 3.3 Full Fine-Tuning

**Idea:** Update all parameters of the pretrained model on the new dataset.

```text
Pretrained model
→ replace or keep the output head
→ unfreeze all layers
→ train the whole model
```

**When to use:**

- You have enough labeled data.
- The task/domain is different from pretraining.
- You have enough compute.
- Maximum performance is more important than cost.

**Advantages:**

- Strongest adaptation capacity.
- Often gives the best result if data and compute are sufficient.

**Limitations:**

- High memory and compute cost.
- Higher overfitting risk on small datasets.
- Can cause catastrophic forgetting.
- Requires careful learning rate and validation.

---

### 3.4 Gradual Unfreezing

**Idea:** Start by training only the head, then progressively unfreeze deeper layers.

Example schedule:

```text
Epoch 1-2: train only classification head
Epoch 3-4: unfreeze last block
Epoch 5-6: unfreeze last two blocks
Epoch 7+: optionally unfreeze all layers
```

**When to use:**

- You want stable training.
- The dataset is not large.
- Full fine-tuning immediately causes overfitting or instability.

**Advantages:**

- Preserves pretrained representations early in training.
- Gives the new head time to stabilize.
- Reduces sudden destructive updates.

**Limitations:**

- More training stages to manage.
- Requires scheduling decisions.

---

### 3.5 Discriminative Learning Rates

**Idea:** Use smaller learning rates for lower/general layers and larger learning rates for upper/task-specific layers.

Example:

```text
Early layers:      1e-5
Middle layers:     3e-5
Late layers:       1e-4
Task head:         1e-3
```

**Why it works:**

Early layers often encode general features. They should change slowly. Later layers are more task-specific, so they can be updated more aggressively.

**When to use:**

- Partial or full fine-tuning.
- You want to fine-tune deeply without damaging general features.
- You have a pretrained backbone with clear layer hierarchy.

---

### 3.6 Layer-Wise Learning Rate Decay

**Idea:** Similar to discriminative learning rates, but automated by applying a decay factor from top to bottom layers.

Example:

```text
Top layer LR = 1e-4
Each lower layer LR = previous LR × 0.9
```

This is common in Transformer and ViT fine-tuning.

**When to use:**

- BERT, RoBERTa, DeBERTa, ViT, Swin Transformer, ConvNeXt.
- Full fine-tuning with pretrained models.
- Tasks where preserving lower-layer representations matters.

---

## 4. Fine-Tuning by Data Objective

### 4.1 Supervised Fine-Tuning for Classification

**Data format:**

```text
Input → Label
```

Examples:

```text
Review text → rating class
Image → class label
News article → topic label
```

**Loss functions:**

- Cross-entropy for single-label classification.
- Binary cross-entropy for binary or multi-label classification.
- Focal loss for severe class imbalance.

**Common metrics:**

- Accuracy;
- Macro-F1;
- Weighted-F1;
- Precision and recall;
- AUROC for binary/multilabel tasks;
- Confusion matrix.

---

### 4.2 Supervised Fine-Tuning for Regression

**Data format:**

```text
Input → Continuous value
```

Examples:

```text
Movie metadata → rating score
House features → price
Sensor data → future value
```

**Loss functions:**

- MSE;
- MAE;
- Huber loss;
- Quantile loss.

**Common metrics:**

- MAE;
- RMSE;
- R²;
- MAPE, if appropriate.

---

### 4.3 Sequence Labeling Fine-Tuning

**Data format:**

```text
Token sequence → Label per token
```

Examples:

```text
Named entity recognition
Part-of-speech tagging
Medical entity extraction
```

**Models:**

- BERT-style encoders;
- BiLSTM-CRF;
- Transformer encoder + token classification head.

**Metrics:**

- Entity-level F1;
- Token-level accuracy;
- Precision and recall by entity type.

---

### 4.4 Sequence-to-Sequence Fine-Tuning

**Data format:**

```text
Input sequence → Output sequence
```

Examples:

```text
Document → Summary
Question → Answer
Source language → Target language
Instruction → Response
```

**Models:**

- T5;
- BART;
- mT5;
- FLAN-T5;
- encoder-decoder Transformers.

**Loss function:**

- Token-level negative log likelihood / cross-entropy.

**Metrics:**

- ROUGE for summarization;
- BLEU/chrF for translation;
- Exact match/F1 for QA;
- Human evaluation for open-ended generation.

---

### 4.5 Causal Language Model Fine-Tuning

**Data format:**

```text
Text prefix → Next token prediction
```

Examples:

```text
Instruction + answer text
Chat messages
Domain documents
Code repositories
```

**Models:**

- GPT-style models;
- Llama-family models;
- Mistral/Mixtral-style models;
- Qwen-style models;
- Gemma-style models.

**Use cases:**

- Chatbot fine-tuning;
- domain-specific writing;
- code generation;
- reasoning style adaptation;
- internal assistant behavior.

---

## 5. Continued Pretraining / Domain-Adaptive Training

### 5.1 Continued Pretraining

**Idea:** Continue self-supervised pretraining on domain-specific unlabeled data before task-specific fine-tuning.

Example:

```text
General LLM
→ train on company documents, legal text, medical text, or code
→ then supervised fine-tune for QA/chat/classification
```

**When to use:**

- You have lots of unlabeled domain data.
- The target domain has special vocabulary or style.
- The base model lacks domain knowledge.

**Advantages:**

- Helps the model learn domain language.
- Reduces mismatch between pretraining and downstream data.

**Limitations:**

- Expensive for large models.
- Can cause forgetting if domain corpus is narrow.
- Needs careful data cleaning.

---

### 5.2 Domain-Adaptive Pretraining (DAPT)

DAPT means continuing pretraining on a domain corpus, such as biomedical papers, legal documents, financial filings, or software code.

```text
BERT → biomedical corpus → biomedical NER/classification
```

---

### 5.3 Task-Adaptive Pretraining (TAPT)

TAPT means continuing pretraining on the unlabeled text from the target task dataset itself.

```text
BERT → unlabeled task training texts → supervised classification
```

This is usually smaller and cheaper than DAPT.

---

## 6. Parameter-Efficient Fine-Tuning (PEFT)

**PEFT** methods adapt large pretrained models while updating only a small number of parameters. This is especially important for LLMs, VLMs, and other foundation models because full fine-tuning can be too expensive.

General idea:

```text
Freeze most or all base model weights
Add or select a small set of trainable parameters
Train only those parameters
Save only the adapter/checkpoint delta
```

PEFT is useful when:

- the model is too large for full fine-tuning;
- you need multiple task-specific versions;
- you want small checkpoints;
- you are working with limited GPU memory;
- you want to preserve the base model.

---

## 7. Major PEFT Techniques

### 7.1 LoRA: Low-Rank Adaptation

**Idea:** Freeze the original model weights and inject trainable low-rank matrices into selected linear layers.

For a weight matrix update:

```text
W' = W + ΔW
ΔW = B × A
```

Where `A` and `B` are small low-rank matrices.

**Common target modules in Transformers:**

- query projection;
- key projection;
- value projection;
- output projection;
- MLP up/down/gate projections;
- sometimes the language modeling head.

**Important hyperparameters:**

| Hyperparameter | Meaning |
|---|---|
| `r` | LoRA rank; controls adapter capacity |
| `lora_alpha` | Scaling factor |
| `lora_dropout` | Dropout for LoRA layers |
| `target_modules` | Which layers receive LoRA adapters |
| `modules_to_save` | Extra full modules to train and save |

**When to use:**

- Fine-tuning LLMs on limited GPU.
- Instruction tuning.
- Domain adaptation.
- Classification with large language models.
- Multi-task adapter storage.

**Advantages:**

- Much cheaper than full fine-tuning.
- Small adapter checkpoints.
- Can be merged into the base model for inference.
- Strong default choice for LLM fine-tuning.

**Limitations:**

- Rank and target modules matter.
- Very different domains may need higher rank or more target layers.
- Adapter merging and quantization require care.

---

### 7.2 QLoRA

**Idea:** Quantize the frozen base model to low precision, commonly 4-bit, and train LoRA adapters on top.

```text
Frozen 4-bit base model + trainable LoRA adapters
```

**When to use:**

- You want to fine-tune a large LLM on limited VRAM.
- You cannot afford full precision training.
- You are using consumer GPUs.

**Advantages:**

- Major memory reduction.
- Enables training larger models on smaller hardware.
- Often close to full fine-tuning performance when data quality is good.

**Limitations:**

- Training can be slower than full precision in some setups.
- Requires correct quantization libraries.
- Some models/layers may be sensitive to quantization.

---

### 7.3 AdaLoRA

**Idea:** Instead of using the same LoRA rank everywhere, AdaLoRA dynamically allocates parameter budget to more important layers or matrices.

**When to use:**

- You want better parameter allocation than standard LoRA.
- You have strict adapter size constraints.
- Different layers likely need different adaptation capacity.

**Advantages:**

- More flexible than fixed-rank LoRA.
- Can improve low-budget adaptation.

**Limitations:**

- More complex than standard LoRA.
- More hyperparameters and training logic.

---

### 7.4 DoRA: Weight-Decomposed LoRA

**Idea:** Decompose weight updates into magnitude and direction components, then use LoRA-style adaptation mainly for direction.

**When to use:**

- You want a LoRA variant with stronger adaptation capacity.
- You are fine-tuning LLMs where standard LoRA underperforms.

**Advantages:**

- Can improve quality over standard LoRA in some settings.

**Limitations:**

- More complex.
- May increase memory or compute compared with plain LoRA.

---

### 7.5 VeRA

**Idea:** Use shared low-rank matrices and train only small scaling vectors.

**When to use:**

- You need extremely small adapter checkpoints.
- You want parameter-efficient personalization.

**Advantages:**

- Smaller than LoRA.
- Useful when many adapters must be stored.

**Limitations:**

- Less flexible than LoRA in some tasks.

---

### 7.6 IA3

**Idea:** Instead of learning low-rank matrix updates, IA3 learns vectors that rescale internal activations in attention and feed-forward modules.

```text
Frozen Transformer + learned activation scaling vectors
```

**When to use:**

- Very small trainable parameter budget.
- Multi-task adaptation.
- Fast training with minimal memory.

**Advantages:**

- Extremely parameter-efficient.
- Base model remains frozen.
- Adapter-like portability.

**Limitations:**

- Lower capacity than LoRA for some tasks.
- Target module selection still matters.

---

### 7.7 Adapter Tuning

**Idea:** Insert small trainable adapter modules inside the model, usually between Transformer sublayers.

Common adapter structure:

```text
Hidden state
→ down projection
→ nonlinearity
→ up projection
→ residual connection
```

**When to use:**

- You want one base model with many task-specific adapters.
- You want modularity across tasks.
- You need to avoid full model copies.

**Advantages:**

- Good multi-task management.
- Easy to swap adapters.
- Base model remains frozen.

**Limitations:**

- May add inference latency if not merged.
- Architecture modification is more intrusive than LoRA.

---

### 7.8 Prompt Tuning

**Idea:** Freeze the model and learn continuous soft prompt embeddings prepended to the input.

```text
Learned soft prompt + input tokens → frozen model → output
```

**When to use:**

- Very large language models.
- Simple tasks.
- Extremely small number of trainable parameters.

**Advantages:**

- Very lightweight.
- Easy to store one prompt per task.

**Limitations:**

- Often less powerful than LoRA.
- Can be sensitive to initialization and prompt length.
- Works better as model size grows.

---

### 7.9 Prefix Tuning

**Idea:** Learn continuous prefix vectors that are injected into Transformer attention, behaving like virtual tokens available to later tokens.

**When to use:**

- Natural language generation.
- Summarization.
- Table-to-text generation.
- Low-data settings.

**Advantages:**

- Very parameter-efficient.
- Good for generation tasks.

**Limitations:**

- Less commonly used than LoRA in modern LLM pipelines.
- Prefix length and initialization matter.

---

### 7.10 P-Tuning / P-Tuning v2

**Idea:** Learn trainable continuous prompts, sometimes inserted at multiple layers.

**When to use:**

- Prompt-based adaptation.
- NLU and generation tasks.
- Cases where discrete prompt engineering is insufficient.

**Advantages:**

- Lightweight.
- Avoids manually searching for natural-language prompts.

**Limitations:**

- May require tuning prompt length and placement.
- Can be less robust than LoRA.

---

### 7.11 BitFit

**Idea:** Freeze almost all model weights and train only bias terms.

**When to use:**

- Small-to-medium datasets.
- Very limited compute.
- You want a minimal baseline PEFT method.

**Advantages:**

- Extremely simple.
- Very few trainable parameters.

**Limitations:**

- Limited adaptation capacity.
- Usually not the first choice for modern LLM instruction tuning.

---

### 7.12 LayerNorm Tuning

**Idea:** Train only LayerNorm parameters, or LayerNorm plus bias terms.

**When to use:**

- Lightweight adaptation.
- Small data.
- Stabilizing model behavior without large updates.

**Advantages:**

- Cheap.
- Simple.

**Limitations:**

- Limited expressiveness.

---

### 7.13 Trainable Token Fine-Tuning

**Idea:** Train only selected token embeddings or newly added special tokens.

Examples:

```text
Add new domain tokens
Train only their embeddings
Keep the rest of the model frozen
```

**When to use:**

- New domain vocabulary.
- Personalization tokens.
- Style tokens.
- Special control tokens.

**Advantages:**

- Tiny parameter count.
- Useful for controlled generation or domain terms.

**Limitations:**

- Cannot deeply adapt model reasoning or task behavior alone.

---

## 8. LLM-Specific Fine-Tuning and Post-Training

### 8.1 Supervised Fine-Tuning (SFT)

**Idea:** Train a language model on curated instruction-response examples.

Common format:

```text
System message
User instruction
Assistant response
```

Example:

```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain transfer learning."},
    {"role": "assistant", "content": "Transfer learning is ..."}
  ]
}
```

**When to use:**

- You want a chatbot.
- You want the model to follow instructions.
- You want a domain-specific assistant.
- You want consistent answer format or tone.

**Data quality matters more than data quantity.** Bad SFT data can make the model verbose, inaccurate, unsafe, or stylistically inconsistent.

---

### 8.2 Instruction Fine-Tuning

Instruction fine-tuning is a form of SFT where the dataset contains many task instructions and desired outputs.

Examples:

```text
Translate this sentence → translated sentence
Summarize this article → summary
Classify this review → label
Write SQL for this request → SQL query
```

**Goal:** Teach the model to generalize across instructions, not only memorize one task.

---

### 8.3 Chat Fine-Tuning

Chat fine-tuning uses multi-turn conversation data.

```text
System → User → Assistant → User → Assistant
```

**When to use:**

- Customer support assistant.
- Internal company assistant.
- Tutor/chatbot.
- Domain-specific Q&A agent.

**Important:** Use the same chat template as the base model expects. Incorrect formatting can severely hurt performance.

---

### 8.4 Preference Fine-Tuning

Preference fine-tuning uses comparisons between better and worse responses.

Data format:

```text
Prompt
Chosen response
Rejected response
```

Goal:

```text
Increase probability of preferred outputs
Decrease probability of rejected outputs
```

Used for:

- helpfulness;
- harmlessness;
- style control;
- refusal behavior;
- reasoning quality;
- summarization quality;
- reducing hallucination tendencies.

---

### 8.5 RLHF

**RLHF** means Reinforcement Learning from Human Feedback.

Typical pipeline:

```text
1. SFT model
2. Collect preference data
3. Train reward model
4. Optimize policy with RL, often PPO-style methods
```

**Advantages:**

- Powerful alignment method.
- Can optimize human preferences beyond supervised labels.

**Limitations:**

- Complex.
- Expensive.
- Can be unstable.
- Requires high-quality preference data and reward modeling.

---

### 8.6 DPO: Direct Preference Optimization

**Idea:** Train directly on preference pairs without a separate reward model and without full RL training.

Data:

```text
Prompt + chosen answer + rejected answer
```

**When to use:**

- You already have preference pairs.
- You want simpler alignment than RLHF.
- You want to improve answer quality after SFT.

**Advantages:**

- Simpler than RLHF.
- Popular for open-source LLM alignment.
- Works well with LoRA/QLoRA.

**Limitations:**

- Quality depends heavily on preference data.
- Incorrect preference labels can damage model behavior.

---

### 8.7 ORPO

**ORPO** combines supervised learning and preference optimization in one objective.

**When to use:**

- You want a simpler pipeline than SFT followed by DPO.
- You have chosen/rejected preference data.

**Advantages:**

- Can simplify post-training.
- Reduces need for multiple stages.

**Limitations:**

- Less standard than SFT + DPO.
- Needs careful evaluation.

---

### 8.8 KTO

**KTO** uses binary feedback such as desirable vs undesirable outputs rather than explicit chosen/rejected pairs.

**When to use:**

- You have thumbs-up/thumbs-down style feedback.
- Pairwise preferences are unavailable.

**Advantages:**

- Easier feedback format.

**Limitations:**

- Needs enough reliable feedback.
- Can be sensitive to label quality.

---

### 8.9 PPO / GRPO-Style Online Optimization

These methods optimize model outputs using reward signals, often involving sampling from the model during training.

**When to use:**

- Advanced alignment or reasoning training.
- You have reward functions or verifiable tasks.
- You can afford more complex training.

**Advantages:**

- Can optimize objectives that are hard to express as supervised labels.

**Limitations:**

- More complex than SFT or DPO.
- Requires careful monitoring.
- Can exploit flawed reward functions.

---

### 8.10 Distillation Fine-Tuning

**Idea:** Train a smaller student model using outputs from a stronger teacher model.

Data format:

```text
Prompt → Teacher response → Student learns response
```

**When to use:**

- You want a smaller model with teacher-like behavior.
- You need lower inference cost.
- You want to transfer style, reasoning format, or domain behavior.

**Advantages:**

- Can create efficient specialized models.
- Useful for deployment.

**Limitations:**

- Student inherits teacher mistakes.
- Synthetic data needs filtering.

---

## 9. Fine-Tuning for Different Model Families

### 9.1 CNN Fine-Tuning

Common models:

- ResNet;
- EfficientNet;
- ConvNeXt;
- DenseNet;
- MobileNet.

Recommended progression:

```text
1. Train classifier head only
2. Unfreeze last block
3. Use data augmentation
4. Try full fine-tuning if dataset is large
```

Important details:

- Use pretrained normalization statistics if required.
- Use augmentation for small datasets.
- Monitor overfitting through validation loss.

---

### 9.2 Vision Transformer Fine-Tuning

Common models:

- ViT;
- DeiT;
- Swin Transformer;
- CLIP vision encoder.

Useful techniques:

- Layer-wise learning rate decay;
- RandAugment/Mixup/CutMix;
- warmup schedule;
- strong regularization;
- partial unfreezing;
- LoRA for ViT attention layers.

---

### 9.3 Encoder Transformer Fine-Tuning

Common models:

- BERT;
- RoBERTa;
- DeBERTa;
- DistilBERT;
- PhoBERT;
- XLM-R.

Tasks:

- text classification;
- token classification;
- retrieval embedding;
- natural language inference;
- extractive QA.

Recommended progression:

```text
1. Freeze encoder + train head
2. Unfreeze final layers
3. Full fine-tune with small LR
4. Try layer-wise LR decay
5. Evaluate Macro-F1 and error cases
```

Typical learning rates:

```text
Encoder full fine-tuning: 1e-5 to 5e-5
Task head: 1e-4 to 1e-3
```

---

### 9.4 Decoder-Only LLM Fine-Tuning

Common models:

- Llama-family models;
- Mistral-style models;
- Qwen-style models;
- Gemma-style models;
- GPT-style models.

Typical techniques:

- SFT;
- LoRA;
- QLoRA;
- DPO;
- ORPO/KTO;
- continued pretraining;
- distillation;
- retrieval-augmented fine-tuning.

Recommended progression:

```text
1. Decide whether RAG is enough before fine-tuning
2. Build high-quality instruction dataset
3. Start with LoRA or QLoRA
4. Evaluate on held-out prompts
5. Add DPO/preference tuning only if needed
6. Monitor hallucination, format following, and safety behavior
```

---

### 9.5 Encoder-Decoder Fine-Tuning

Common models:

- T5;
- FLAN-T5;
- BART;
- mT5.

Tasks:

- summarization;
- translation;
- structured generation;
- question answering;
- instruction-to-output tasks.

Useful techniques:

- teacher forcing;
- label smoothing;
- sequence-level metrics;
- length penalty tuning;
- beam search evaluation;
- LoRA on attention and feed-forward layers.

---

### 9.6 Multimodal Model Fine-Tuning

Common model types:

- CLIP-style image-text encoders;
- BLIP-style vision-language models;
- LLaVA-style visual instruction models;
- audio-language models;
- video-language retrieval models.

Fine-tuning types:

- contrastive fine-tuning;
- captioning fine-tuning;
- visual instruction tuning;
- retrieval fine-tuning;
- projector-only fine-tuning;
- LoRA on language model layers;
- LoRA on vision encoder layers;
- full multimodal fine-tuning.

Typical progression:

```text
1. Freeze vision encoder and language model
2. Train projector/alignment layer
3. Add LoRA to language model
4. Optionally unfreeze selected vision layers
5. Evaluate both text quality and visual grounding
```

---

## 10. Data Strategy for Fine-Tuning

### 10.1 Data Quality Checklist

Good fine-tuning data should be:

- relevant to the target task;
- clean and deduplicated;
- correctly labeled;
- balanced enough for the task;
- representative of real user inputs;
- split properly into train/validation/test;
- free of leakage from evaluation data;
- formatted consistently.

Bad data can make a strong model worse.

---

### 10.2 Dataset Splitting

Recommended split:

```text
Train set:      model learns from it
Validation set: tune hyperparameters and early stopping
Test set:       final unbiased evaluation
```

Never tune directly on the test set.

For small datasets:

- use stratified split for classification;
- consider cross-validation;
- keep a small final holdout test set if possible.

---

### 10.3 Data Leakage Checks

Check for:

- duplicate samples across train and test;
- near-duplicate text;
- same user/session/entity appearing in both splits;
- labels accidentally included in input features;
- future information used to predict the past;
- synthetic data generated from test examples.

---

### 10.4 Handling Class Imbalance

Options:

- class-weighted loss;
- focal loss;
- oversampling minority classes;
- undersampling majority classes;
- data augmentation;
- threshold tuning;
- macro-F1 as primary metric.

Avoid relying only on accuracy for imbalanced datasets.

---

### 10.5 Instruction Data Design for LLMs

Good instruction data should include:

- clear user intent;
- accurate responses;
- diverse phrasing;
- real task distribution;
- consistent style;
- examples of refusal or uncertainty when appropriate;
- multi-turn examples if the final product is a chatbot.

Avoid:

- noisy generated data without review;
- overly long answers for every prompt;
- hallucinated facts;
- contradictory style guidelines;
- training on evaluation prompts.

---

## 11. Optimization Techniques

### 11.1 Learning Rate

Fine-tuning usually needs lower learning rates than training from scratch.

Typical ranges:

```text
CNN/ViT full fine-tuning:      1e-5 to 1e-4
BERT-style full fine-tuning:   1e-5 to 5e-5
Classification head only:      1e-4 to 1e-3
LoRA/QLoRA for LLMs:           1e-5 to 2e-4
```

These are starting points, not fixed rules.

---

### 11.2 Warmup

Warmup slowly increases the learning rate at the start of training.

Useful when:

- fine-tuning Transformers;
- training is unstable early;
- using larger batch sizes;
- using mixed precision.

Common warmup ratio:

```text
3% to 10% of total training steps
```

---

### 11.3 Learning Rate Schedules

Common schedules:

- linear decay;
- cosine decay;
- cosine with restarts;
- constant with warmup;
- polynomial decay.

For Transformers, linear or cosine schedules with warmup are common.

---

### 11.4 Weight Decay

Weight decay helps regularization.

Typical values:

```text
0.01 for Transformer fine-tuning
1e-4 to 1e-2 for vision models
```

Do not apply weight decay to:

- bias terms;
- LayerNorm weights;
- sometimes embeddings.

---

### 11.5 Gradient Clipping

Gradient clipping prevents exploding gradients.

Typical value:

```text
max_grad_norm = 1.0
```

Useful for:

- LLM fine-tuning;
- RNNs;
- unstable losses;
- mixed precision training.

---

### 11.6 Mixed Precision Training

Mixed precision uses lower precision arithmetic to reduce memory and speed up training.

Common formats:

- FP16;
- BF16;
- FP8 in newer hardware/software stacks.

BF16 is often more stable than FP16 when hardware supports it.

---

### 11.7 Gradient Accumulation

Gradient accumulation simulates a larger batch size when GPU memory is limited.

Example:

```text
per_device_batch_size = 2
gradient_accumulation_steps = 8
effective_batch_size = 16
```

Useful for:

- LLM fine-tuning;
- long sequence training;
- limited VRAM.

---

### 11.8 Gradient Checkpointing

Gradient checkpointing saves memory by recomputing activations during backward pass.

**Trade-off:**

```text
Lower memory usage, slower training
```

Useful for:

- large models;
- long context length;
- QLoRA/LoRA training with limited VRAM.

---

### 11.9 Early Stopping

Stop training when validation performance no longer improves.

Useful when:

- dataset is small;
- overfitting happens quickly;
- training budget is limited.

Monitor:

- validation loss;
- Macro-F1;
- task-specific metric;
- hallucination or human evaluation for generation tasks.

---

## 12. Regularization Techniques

### 12.1 Dropout

Dropout randomly disables activations during training.

Use for:

- classifier heads;
- LoRA dropout;
- small datasets;
- text classification.

Too much dropout can cause underfitting.

---

### 12.2 Label Smoothing

Label smoothing prevents the model from becoming overconfident.

Useful for:

- classification;
- sequence generation;
- noisy labels.

---

### 12.3 Data Augmentation

Vision augmentation:

- random crop;
- random horizontal flip;
- color jitter;
- RandAugment;
- Mixup;
- CutMix.

Text augmentation:

- paraphrasing;
- back translation;
- synonym replacement with caution;
- template variation;
- synthetic instruction generation with review.

Audio/video augmentation:

- noise injection;
- time masking;
- frequency masking;
- random frame sampling;
- temporal cropping.

---

### 12.4 Freezing as Regularization

Freezing lower layers can act as regularization by limiting the number of trainable parameters.

Use when:

- dataset is small;
- overfitting is severe;
- domain is similar to pretraining.

---

### 12.5 Weight Averaging / EMA

Exponential Moving Average or weight averaging can stabilize final models.

Useful for:

- vision models;
- noisy fine-tuning;
- long training runs.

---

## 13. Evaluation Strategy

### 13.1 Classification Evaluation

Use:

- accuracy;
- Macro-F1;
- precision/recall;
- confusion matrix;
- per-class metrics;
- calibration metrics if probabilities matter.

For imbalanced data, prefer Macro-F1 over accuracy.

---

### 13.2 Generation Evaluation

Automatic metrics:

- ROUGE;
- BLEU;
- chrF;
- BERTScore;
- exact match;
- pass@k for code;
- task-specific correctness.

Human or judge-based evaluation:

- helpfulness;
- factuality;
- instruction following;
- conciseness;
- safety;
- style consistency.

Automatic metrics alone are often insufficient for open-ended generation.

---

### 13.3 LLM Evaluation Checklist

Evaluate:

- factual accuracy;
- hallucination rate;
- instruction following;
- formatting consistency;
- refusal behavior;
- domain knowledge;
- multi-turn consistency;
- latency;
- token cost;
- robustness to edge cases;
- regression against base model capabilities.

---

### 13.4 Ablation Studies

Run experiments such as:

```text
Base model vs fine-tuned model
Head-only vs partial vs full fine-tuning
LoRA rank 4 vs 8 vs 16 vs 32
Target attention only vs attention + MLP
SFT only vs SFT + DPO
With vs without domain pretraining
```

Ablation helps identify what actually improves performance.

---

## 14. Choosing the Right Fine-Tuning Method

### 14.1 If Your Dataset Is Small

Start with:

```text
1. Feature extraction / head-only training
2. Partial fine-tuning
3. Strong regularization
4. Data augmentation
5. PEFT if the model is large
```

Avoid immediate full fine-tuning unless validation proves it helps.

---

### 14.2 If Your Dataset Is Medium-Sized

Try:

```text
1. Partial fine-tuning
2. Discriminative learning rates
3. Layer-wise LR decay
4. LoRA for large Transformers
5. Full fine-tuning if overfitting is controlled
```

---

### 14.3 If Your Dataset Is Large

Try:

```text
1. Full fine-tuning
2. Continued pretraining if domain-specific
3. SFT for instruction behavior
4. Preference tuning if output quality matters
5. Distributed training if needed
```

---

### 14.4 If You Are Fine-Tuning an LLM on Limited GPU

Recommended default:

```text
QLoRA or LoRA
```

Start with:

```text
r = 8 or 16
lora_alpha = 16 or 32
dropout = 0.05 to 0.1
learning_rate = 1e-5 to 2e-4
```

Then experiment with:

- target modules;
- rank;
- dataset quality;
- sequence length;
- batch size;
- learning rate;
- number of epochs.

---

### 14.5 If You Need Domain Knowledge

First ask:

```text
Can retrieval-augmented generation solve this without fine-tuning?
```

If not, use:

```text
1. Continued pretraining on domain corpus
2. SFT on domain instructions
3. Optional DPO on domain preference pairs
```

Fine-tuning is not a replacement for knowledge retrieval when facts change often.

---

## 15. RAG vs Fine-Tuning

| Goal | Better choice |
|---|---|
| Add frequently changing facts | RAG |
| Teach response style | Fine-tuning |
| Teach a fixed domain format | Fine-tuning |
| Use private documents with citations | RAG |
| Improve instruction following | SFT / DPO |
| Reduce hallucination with source grounding | RAG + evaluation |
| Adapt model vocabulary/domain language | Continued pretraining / fine-tuning |
| Personalize behavior across many users | Adapters / LoRA / prompt tuning |

A strong production system often combines both:

```text
RAG for knowledge + fine-tuning for behavior/style/task skill
```

---

## 16. Practical Fine-Tuning Pipeline

### Step 1: Define the Objective

Clarify:

- What is the input?
- What is the output?
- What metric matters?
- What is the deployment constraint?
- Is fine-tuning necessary, or would prompting/RAG be enough?

---

### Step 2: Choose the Base Model

Consider:

- task type;
- language support;
- model size;
- license;
- context length;
- inference cost;
- available GPU;
- community support.

---

### Step 3: Prepare Data

Do:

- clean text/images/audio;
- deduplicate samples;
- remove corrupted records;
- normalize labels;
- split train/validation/test;
- format examples correctly;
- inspect random samples manually.

---

### Step 4: Build a Baseline

Baselines may include:

- prompt-only model;
- RAG-only system;
- head-only fine-tuning;
- small model baseline;
- classical ML baseline such as TF-IDF + Logistic Regression for text classification.

Never fine-tune blindly without a baseline.

---

### Step 5: Select Fine-Tuning Strategy

Decision guide:

```text
Small model + enough data → full fine-tuning
Large LLM + limited GPU → LoRA/QLoRA
Need style/instruction behavior → SFT
Need preference alignment → DPO/RLHF/KTO/ORPO
Need domain vocabulary → continued pretraining
Need many task variants → adapters/LoRA per task
```

---

### Step 6: Train with Tracking

Track:

- training loss;
- validation loss;
- task metric;
- learning rate;
- gradient norm;
- GPU memory;
- examples per second;
- random seed;
- dataset version;
- model checkpoint version.

Recommended tools:

- Weights & Biases;
- TensorBoard;
- MLflow;
- Hugging Face Hub;
- custom experiment logs.

---

### Step 7: Evaluate Carefully

Evaluate on:

- validation set;
- held-out test set;
- real-world examples;
- adversarial or edge cases;
- long-tail categories;
- latency and cost constraints.

For LLMs, also inspect outputs manually.

---

### Step 8: Deploy and Monitor

Monitor:

- latency;
- error rate;
- output quality;
- hallucinations;
- user feedback;
- drift;
- safety issues;
- cost per request.

Plan rollback if the fine-tuned model performs worse than the baseline.

---

## 17. Common Mistakes

### Mistake 1: Fine-Tuning When Prompting or RAG Is Enough

Fine-tuning is not always necessary. If you only need to add external knowledge, RAG may be better.

---

### Mistake 2: Training on Low-Quality Data

A small clean dataset is often better than a large noisy dataset.

---

### Mistake 3: No Validation Set

Without validation, you cannot know whether the model is improving or overfitting.

---

### Mistake 4: Too High Learning Rate

High learning rates can destroy pretrained representations.

---

### Mistake 5: Evaluating Only Training Loss

Lower training loss does not always mean better real-world performance.

---

### Mistake 6: Ignoring Chat Templates

For LLMs, incorrect prompt/chat formatting can significantly damage fine-tuning quality.

---

### Mistake 7: Overfitting to Style

If every training answer has the same rigid format, the model may become inflexible.

---

### Mistake 8: Mixing Contradictory Instructions

If the dataset contains conflicting behavior rules, the fine-tuned model will behave inconsistently.

---

## 18. Recommended Experiment Order

### For Computer Vision

```text
1. Pretrained backbone + train head
2. Add data augmentation
3. Unfreeze final block
4. Try discriminative learning rates
5. Full fine-tuning if data is large enough
6. Compare with ViT/ConvNeXt alternatives
```

### For NLP Classification

```text
1. TF-IDF + Logistic Regression baseline
2. Frozen encoder + classifier head
3. Partial Transformer fine-tuning
4. Full Transformer fine-tuning
5. Try class weights/focal loss if imbalanced
6. Evaluate Macro-F1 and confusion matrix
```

### For LLM Chatbot

```text
1. Prompting baseline
2. RAG baseline if knowledge is needed
3. LoRA/QLoRA SFT
4. Evaluate held-out prompts
5. Add preference tuning if needed
6. Deploy with monitoring and rollback
```

### For Domain-Specific LLM

```text
1. Check whether RAG solves the problem
2. Collect domain corpus
3. Continued pretraining if domain shift is large
4. SFT on domain instruction data
5. DPO/KTO/ORPO if preference data exists
6. Evaluate factuality and domain correctness
```

---

## 19. Hardware and Memory Considerations

### 19.1 What Consumes Memory During Training?

Memory is used by:

- model weights;
- gradients;
- optimizer states;
- activations;
- temporary buffers;
- batch size;
- sequence length.

Full fine-tuning large models is expensive because optimizer states and gradients scale with all parameters.

---

### 19.2 Ways to Reduce Memory

Use:

- LoRA;
- QLoRA;
- smaller batch size;
- gradient accumulation;
- gradient checkpointing;
- mixed precision;
- shorter sequence length;
- optimizer memory reduction;
- DeepSpeed ZeRO;
- Fully Sharded Data Parallel;
- CPU/NVMe offloading when necessary.

---

## 20. Cheat Sheet

| Situation | Recommended method |
|---|---|
| Small image dataset | Pretrained CNN + train head |
| Medium image dataset | Unfreeze final block |
| Large image dataset | Full fine-tuning |
| Text classification with little data | Frozen encoder + classifier |
| Text classification with enough data | Full BERT/PhoBERT fine-tuning |
| LLM with one consumer GPU | QLoRA |
| LLM with enough VRAM | LoRA or full fine-tuning |
| Need chatbot behavior | SFT |
| Need better answer preference | DPO / ORPO / KTO |
| Need constantly updated facts | RAG, not fine-tuning alone |
| Need domain language adaptation | Continued pretraining + SFT |
| Need many task-specific variants | LoRA/adapters per task |
| Need tiny trainable parameter count | IA3 / prompt tuning / BitFit |

---

## 21. Minimal Practical Configurations

### 21.1 BERT/PhoBERT Text Classification

```text
Base model: PhoBERT/BERT/RoBERTa
Max length: 128 or 256
Learning rate: 1e-5 to 5e-5
Batch size: 16 or 32 if possible
Epochs: 3 to 5
Optimizer: AdamW
Scheduler: linear/cosine with warmup
Metric: Macro-F1 for imbalanced data
```

### 21.2 ResNet/EfficientNet Image Classification

```text
Input size: 224 or model-specific
Augmentation: random crop, flip, color jitter
Phase 1: train head only
Phase 2: unfreeze final block
Learning rate head: 1e-3
Learning rate backbone: 1e-5 to 1e-4
Metric: accuracy + per-class F1
```

### 21.3 LLM QLoRA SFT

```text
Base model: instruction-capable or general causal LM
Quantization: 4-bit
Adapter: LoRA
Rank r: 8, 16, or 32
Alpha: 16, 32, or 64
Dropout: 0.05 to 0.1
Learning rate: 1e-5 to 2e-4
Epochs: 1 to 3 for high-quality data
Evaluation: held-out prompts + human review
```

### 21.4 LLM DPO

```text
Starting point: SFT model
Data: prompt, chosen response, rejected response
Learning rate: often lower than SFT
Training method: DPO with reference model or PEFT setup
Evaluation: preference win rate, factuality, regressions
```

---

## 22. Final Mental Model

Think of fine-tuning as a spectrum:

```text
No weight update
→ prompt engineering
→ RAG
→ train output head
→ partial fine-tuning
→ PEFT adapters
→ full fine-tuning
→ continued pretraining
→ preference optimization
```

The best method depends on:

- data size;
- data quality;
- task difficulty;
- domain shift;
- model size;
- compute budget;
- deployment requirements;
- evaluation quality.

A professional workflow is not to choose one method by intuition, but to run controlled experiments:

```text
Baseline → simple fine-tuning → stronger fine-tuning → ablation → evaluation → deployment monitoring
```

---

## 23. References and Further Reading

1. PyTorch Transfer Learning Tutorial — https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
2. Hugging Face Transformers Fine-Tuning Guide — https://huggingface.co/docs/transformers/en/training
3. Hugging Face PEFT Documentation — https://huggingface.co/docs/peft/en/index
4. Hugging Face Transformers PEFT Integration — https://huggingface.co/docs/transformers/en/peft
5. Hugging Face TRL Documentation — https://huggingface.co/docs/trl/en/index
6. Hugging Face DPO Trainer — https://huggingface.co/docs/trl/en/dpo_trainer
7. LoRA: Low-Rank Adaptation of Large Language Models — https://arxiv.org/abs/2106.09685
8. QLoRA: Efficient Finetuning of Quantized LLMs — https://arxiv.org/abs/2305.14314
9. Prefix-Tuning: Optimizing Continuous Prompts for Generation — https://arxiv.org/abs/2101.00190
10. BitFit: Simple Parameter-efficient Fine-tuning for Transformer-based Masked Language-models — https://arxiv.org/abs/2106.10199
11. AdaLoRA: Adaptive Budget Allocation for Parameter-Efficient Fine-Tuning — https://arxiv.org/abs/2303.10512

---

## 24. Suggested Learning Path

If you are learning fine-tuning from zero, follow this order:

```text
1. Transfer learning with CNNs
2. BERT/PhoBERT text classification
3. Full vs partial fine-tuning experiments
4. LoRA and QLoRA for LLMs
5. SFT dataset design
6. DPO/preference optimization
7. Evaluation and deployment monitoring
8. RAG + fine-tuning combined systems
```

By the end, you should be able to decide not only **how to fine-tune**, but also **whether fine-tuning is the right solution at all**.
