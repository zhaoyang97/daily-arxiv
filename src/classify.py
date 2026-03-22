#!/usr/bin/env python3
"""论文领域分类规则。

从 Auto Research 项目的 reclassify_auto.py 提取，用于 daily arXiv 论文分类。
"""

# (keywords, domain) — 按优先级排序，第一个匹配的 wins
CATEGORY_RULES = [
    # ══ 非 NLP/LLM 领域 (优先匹配) ══
    (["medical", "clinical", "patholog", "radiology", "x-ray", "mri", "surgical",
      "retina", "cancer", "tumor", "lesion", "ultrasound", "endoscop", "histopath",
      "ophthal", "brain mri", "echocardiog", "chest x-ray", "ct scan", "fundus",
      "drug discovery", "molecule generat", "protein", "genomic", "biomedical"],
     "medical_imaging"),
    (["autonomous driv", "self-driving", "lidar", "bev ", "occupancy predict",
      "lane detect", "traffic", "vehicle detect", "driving scene", "pedestrian",
      "trajectory predict", "autonomous vehicle"],
     "autonomous_driving"),
    (["3d gaussian", "gaussian splat", "nerf", "neural radiance", "3d reconstruct",
      "3d generation", "mesh ", "point cloud", "3d object", "slam",
      "structure from motion", "sfm", "stereo match", "depth estimat",
      "monocular depth", "3d scene", "novel view", "view synthesis",
      "3d aware", "3d-aware", "voxel", "3d detect", "3d perception"],
     "3d_vision"),
    (["segmentat", "panoptic", "semantic seg", "instance seg", "salient object",
      "camouflage", "referring seg", "open-vocabulary seg", "interactive seg"],
     "segmentation"),
    (["object detect", "detector ", "yolo", "detr", "anchor", "bounding box",
      "few-shot detect"],
     "object_detection"),
    (["diffusion model", "text-to-image", "image generation", "image synthesis",
      "generative model", "inpainting", "image editing", "style transfer",
      "text-to-3d", "image-to-image", "denoising score", "flow matching",
      "score-based", "rectified flow"],
     "image_generation"),
    (["video generation", "video synthesis", "video editing", "video understand",
      "video question", "temporal ground", "action recogn", "action detect",
      "optical flow", "video object", "tracking", "frame interpolat",
      "video caption", "video grounding", "video language", "video-language"],
     "video_understanding"),
    (["image restor", "deblur", "denois", "derain", "dehaze", "low-light",
      "image enhance", "super-resol"],
     "image_restoration"),
    (["remote sensing", "aerial", "satellite", "geo-spatial", "hyperspectral"],
     "remote_sensing"),
    (["face ", "person re-id", "pose estimat", "human pose", "hand ",
      "body ", "avatar", "gesture", "skeleton", "gait", "motion capture",
      "human mesh", "human motion", "garment"],
     "human_understanding"),
    (["adversarial attack", "backdoor", "watermark", "privacy",
      "fairness", "deepfake", "forgery detect"],
     "ai_safety"),

    # ══ RL / 优化 / 控制 ══
    (["reinforcement learn", "multi-agent reinforcement", "policy gradient",
      "q-learning", "actor-critic", "markov decision", "reward shaping",
      "multi-arm bandit", "bandit algorithm", "contextual bandit",
      "offline reinforcement", "online reinforcement", "imitation learn",
      "inverse reinforcement"],
     "reinforcement_learning"),
    (["time series", "time-series", "forecasting", "temporal pattern",
      "sequential data", "anomaly detection in time"],
     "time_series"),
    (["speech recogn", "speech synth", "text-to-speech", "audio",
      "speaker ", "voice ", "acoustic", "music generat", "music ",
      "sound ", "asr ", "tts "],
     "audio_speech"),
    (["graph neural", "graph transform", "graph convolu", "node classif",
      "link predict", "knowledge graph", "heterogeneous graph",
      "graph generation", "molecular graph", "message passing"],
     "graph_learning"),
    (["robot", "embodied", "manipulat", "grasp", "navigation",
      "locomotion", "dexterous", "sim-to-real"],
     "robotics"),
    (["recommend", "collaborative filter", "click-through rate",
      "user preference", "item recommend", "sequential recommend"],
     "recommender"),

    # ══ VLM / 多模态 ══
    (["vision-language", "vlm", "multimodal", "multi-modal", "visual question",
      "image caption", "visual grounding", "mllm", "visual reasoning",
      "vision language action", "vla ", "vision-language-action",
      "visual instruction", "visual prompt"],
     "multimodal_vlm"),

    # ══ 模型压缩 / 高效推理 ══
    (["pruning", "quantiz", "distill", "compress", "lightweight",
      "parameter-efficient", "lora", "adapter", "token compress",
      "token merg", "efficient infer", "model effici",
      "knowledge distill"],
     "model_compression"),

    # ══ 自监督 / 基础模型 ══
    (["self-supervis", "contrastive learn", "masked auto",
      "representation learn", "foundation model"],
     "self_supervised"),

    # ══ LLM 子领域 ══
    (["chain-of-thought", "chain of thought", "mathematical reason",
      "logical reason", "test-time scal", "test time scal",
      "step-by-step reason", "reasoning model", "self-consistency",
      "multi-step reason", "tree of thought", "reasoning chain",
      "cot ", "process reward", "verifier", "thinking model"],
     "llm_reasoning"),
    (["llm agent", "tool use", "tool-augment", "tool augment",
      "gui agent", "agentic", "web agent", "code agent",
      "tool select", "tool call", "react framework",
      "function calling", "api call"],
     "llm_agent"),
    (["rlhf", "reinforcement learning from human", "dpo ",
      "direct preference", "grpo", "reward model", "preference optim",
      "instruction tun", "human feedback", "steerabil",
      "preference learn", "value alignment", "safety alignment",
      "red teaming", "jailbreak"],
     "llm_alignment"),
    (["speculative decod", "kv cache", "long context", "long-context",
      "context window", "flash attention", "mixture of expert",
      " moe ", "sparse attention", "token effici",
      "attention effici", "context length", "inference effici",
      "serving", "batched infer", "model parallel"],
     "llm_efficiency"),
    (["named entity", " ner ", "sentiment", "text classif",
      "information extract", "question answer", "reading comprehens",
      "relation extract", "event extract"],
     "nlp_understanding"),
    (["text generat", "summariz", "machine translat", "neural machine",
      "dialogue system", "code generat", "program synth",
      "controllable generat", "data-to-text"],
     "nlp_generation"),

    # ══ LLM 兜底 ══
    (["large language model", "llm", "prompt", "in-context learn",
      "language model", "tokeniz", "pretrain", "scaling law",
      " nlp ", "natural language process", "transformer"],
     "llm_nlp"),
]

# 负面规则
NEGATIVE_RULES = {
    "llm_agent": [
        "reinforcement learn", "multi-agent reinforcement", "policy gradient",
        "q-learning", "actor-critic", "markov decision",
    ],
    "reinforcement_learning": [
        "llm agent", "gui agent", "web agent", "code agent",
        "rlhf", "direct preference", "grpo", "human feedback",
    ],
    "llm_alignment": [
        "representational alignment", "feature alignment", "domain adaptation",
        "image alignment", "sequence alignment",
    ],
}

# 领域中文名
DOMAIN_NAMES = {
    "medical_imaging": "医学影像",
    "autonomous_driving": "自动驾驶",
    "3d_vision": "3D视觉",
    "segmentation": "图像分割",
    "object_detection": "目标检测",
    "image_generation": "图像生成",
    "video_understanding": "视频理解",
    "image_restoration": "图像修复",
    "remote_sensing": "遥感",
    "human_understanding": "人体理解",
    "ai_safety": "AI安全",
    "reinforcement_learning": "强化学习",
    "time_series": "时间序列",
    "audio_speech": "语音音频",
    "graph_learning": "图学习",
    "robotics": "机器人",
    "recommender": "推荐系统",
    "multimodal_vlm": "多模态/VLM",
    "model_compression": "模型压缩",
    "self_supervised": "自监督学习",
    "llm_reasoning": "LLM推理",
    "llm_agent": "LLM Agent",
    "llm_alignment": "LLM对齐",
    "llm_efficiency": "LLM效率",
    "nlp_understanding": "NLP理解",
    "nlp_generation": "NLP生成",
    "llm_nlp": "LLM/NLP",
    "others": "其他",
}

# 领域 Emoji
DOMAIN_EMOJI = {
    "medical_imaging": "🏥",
    "autonomous_driving": "🚗",
    "3d_vision": "🧊",
    "segmentation": "🎯",
    "object_detection": "🔍",
    "image_generation": "🎨",
    "video_understanding": "🎬",
    "image_restoration": "🖼️",
    "remote_sensing": "🛰️",
    "human_understanding": "👤",
    "ai_safety": "🛡️",
    "reinforcement_learning": "🎮",
    "time_series": "📈",
    "audio_speech": "🔊",
    "graph_learning": "🕸️",
    "robotics": "🤖",
    "recommender": "📋",
    "multimodal_vlm": "🧩",
    "model_compression": "📦",
    "self_supervised": "🔄",
    "llm_reasoning": "🧠",
    "llm_agent": "🦾",
    "llm_alignment": "⚖️",
    "llm_efficiency": "⚡",
    "nlp_understanding": "📖",
    "nlp_generation": "✍️",
    "llm_nlp": "🗣️",
    "others": "📄",
}


def classify_paper(title: str, abstract: str) -> str:
    """根据标题和摘要分类论文到最匹配的领域。"""
    text = f"{title} {abstract}".lower()

    for keywords, domain in CATEGORY_RULES:
        if any(kw in text for kw in keywords):
            # 检查负面规则
            neg_keywords = NEGATIVE_RULES.get(domain, [])
            if neg_keywords and any(nk in text for nk in neg_keywords):
                continue
            return domain

    return "others"
