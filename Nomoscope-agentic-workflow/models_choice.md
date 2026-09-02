
## Models choices

For embeddings we use BGE-M3 that support many language, including European's languages : https://huggingface.co/BAAI/bge-m3/discussions/29#65fab3238e807a4adbfa4f78

Gemma 4: over 140 languages
Qwen 3: 119 languages
Tencent Hy3: 33 languages
NVIDIA: Nemotron 3 Super: English, French, German, Italian, Japanese, Spanish, and Chinese

## Open-weight LLM models for RAG generation

Recommended models for the JRC team (verified July 2026), grouped by hardware tier.

### Small — single workstation GPU (≤ 24 GB)

| Model | Size (total / active) | MoE | License | VRAM (Q4 quant.) | Language support |
|---|---|---|---|---|---|
| **EuroLLM-9B** | 9B | No | Apache 2.0 | ~6 GB | **All 24 EU official languages** + 11 more |
| **Teuken-7B** (OpenGPT-X) | 7B | No | Apache 2.0 | ~5 GB | **All 24 EU official languages** |
| **Qwen3-14B** | 14B | No | Apache 2.0 | ~9 GB | 119 languages |
| **Mistral Small 3.2** | 24B | No | Apache 2.0 | ~15 GB | ~30 languages, strong EU coverage |
| **Gemma 3 27B** | 27B | No | Gemma Terms of Use ⚠️ | ~16 GB | 140+ languages |
| **gpt-oss-20b** (OpenAI) | 21B / 3.6B | Yes | Apache 2.0 | ~16 GB (native MXFP4) | English-centric |

### Medium — one server GPU (48–96 GB, e.g. A100/H100/RTX 6000)

| Model | Size (total / active) | MoE | License | VRAM (Q4/FP8) | Language support |
|---|---|---|---|---|---|
| **Qwen3-32B** | 32B | No | Apache 2.0 | ~20 GB | 119 languages |
| **Qwen3-30B-A3B** | 30B / 3B | Yes | Apache 2.0 | ~20 GB (very fast inference) | 119 languages |
| **Llama 3.3 70B** | 70B | No | Llama Community License ⚠️ | ~40–48 GB | 8 languages (EN, FR, DE, IT, ES, PT, +2) |
| **gpt-oss-120b** (OpenAI) | 117B / 5.1B | Yes | Apache 2.0 | ~80 GB (fits one H100) | English-centric |

### Large — multi-GPU node (frontier-class quality)

| Model | Size (total / active) | MoE | License | VRAM | Language support |
|---|---|---|---|---|---|
| **Mistral Large 3** (Dec 2025) | 675B / 41B | Yes | Apache 2.0 | ~8× H200 (FP8); ~350 GB quantized | 40+ languages, multimodal, 256K context |
| **Qwen3-235B-A22B** | 235B / 22B | Yes | Apache 2.0 | ~150 GB+ (4× A100/H100) | 119 languages |
| **DeepSeek R1 / V3.1** | 671B / 37B | Yes | MIT | ~400 GB+ quantized | Strong EN/ZH, decent EU languages |

### Notes for JRC

- **EU sovereignty picks:** EuroLLM (EU HPC JU–funded, trained on MareNostrum 5 in Barcelona) and Teuken-7B (Fraunhofer/OpenGPT-X) are the only ones trained from scratch on all 24 EU official languages. Mistral is the frontier-class European option with clean Apache 2.0 licensing.
- **License warnings:** Llama's license has a 700M-MAU cap and branding obligations. Llama 4's multimodal license excludes EU-domiciled entities — unsuitable for an EC institution. Gemma's Terms of Use are not OSI-approved and include restrictions Google can update.
- **MoE trade-off:** Mixture of Experts models (Qwen3-30B-A3B, gpt-oss, Mistral Large 3) need VRAM for all parameters but compute only active ones, delivering better tokens/sec per quality level — valuable for RAG serving throughput.
- **For EUROMOD RAG:** recommend Qwen3-30B-A3B or Mistral Small 3.2 for generation on a single 24 GB GPU. EuroLLM-9B as fallback if EU-language parity (e.g., tax-benefit rules in Estonian or Greek) is required. Budget ~2–5 GB headroom for KV cache at long RAG context lengths.

Euromod current models :
- Mistral Small 3.2
- GPT-OSS
- MiniMax 2.7
- Llama 3.3 70B


Models tested throught Azure :
Models 	Input (Per 1M tokens) 	Cached Input (Per 1M tokens) 	Output (Per 1M tokens)
azure_openai/DeepSeek-V4-Flash : $0.19 	$0.028 	$0.51
azure_openai/mistral-medium-3-5 	Input: $1.50/1M Tokens Output: $7.50/1M Tokens 
azure_openai/gpt-5.4-nano-2
azure_openai/gpt-5.6-Luna
azure_openai/gpt-5.6-Terra
azure_openai/gpt-5.6-Sol
azure_openai/Mistral-Large-3
azure_openai/Cohere-command-a-plus-05-2026 Input: $0.80/1M Tokens Output: $3.20/1M Tokens 
