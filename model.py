import torch
import torch.nn as nn
import torch.nn.functional as F

from transformers import BertTokenizer, BertModel

import re


# ================= DEVICE =================
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ================= TOKENIZER =================
tokenizer = BertTokenizer.from_pretrained(
    "bert-base-uncased"
)


# ================= MODEL =================
class Model(nn.Module):

    def __init__(self):

        super().__init__()

        self.bert = BertModel.from_pretrained(
            "bert-base-uncased"
        )

        self.lstm = nn.LSTM(
            input_size=768,
            hidden_size=128,
            batch_first=True,
            bidirectional=True
        )

        self.dropout = nn.Dropout(0.3)

        self.fc = nn.Linear(256, 128)

    def forward(self, ids, mask):

        output = self.bert(
            input_ids=ids,
            attention_mask=mask
        ).last_hidden_state

        # BiLSTM
        output, _ = self.lstm(output)

        # Mean Pooling
        output = torch.mean(output, dim=1)

        # Dropout
        output = self.dropout(output)

        # FC Layer
        output = self.fc(output)

        return output


# ================= LOAD MODEL =================
model = Model().to(device)

# OPTIONAL:
# Uncomment if you have trained weights
# model.load_state_dict(
#     torch.load("model.pth", map_location=device)
# )

model.eval()


# ================= CLEAN TEXT =================
def clean_text(text):

    text = str(text).lower()

    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# ================= EMBEDDING =================
def get_embedding(text):

    tokens = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=128
    )

    ids = tokens["input_ids"].to(device)

    mask = tokens["attention_mask"].to(device)

    with torch.no_grad():

        embedding = model(ids, mask)

    return embedding


# ================= KEYWORD MATCH =================
def keyword_score(student_answer, reference_answer):

    student_words = set(
        clean_text(student_answer).split()
    )

    reference_words = set(
        clean_text(reference_answer).split()
    )

    if len(reference_words) == 0:
        return 0

    matched_words = student_words.intersection(
        reference_words
    )

    score = (
        len(matched_words) / len(reference_words)
    ) * 100

    return score


# ================= SIMILARITY =================
def calculate_similarity(student_answer, reference_answer):

    # Clean text
    student_answer = clean_text(student_answer)

    reference_answer = clean_text(reference_answer)

    # Empty answer
    if len(student_answer.strip()) == 0:

        return {
            "score": 0
        }

    # Generate embeddings
    emb1 = get_embedding(student_answer)

    emb2 = get_embedding(reference_answer)

    # Semantic Similarity
    similarity = F.cosine_similarity(
        emb1,
        emb2
    ).item()

    semantic_score = similarity * 100

    # Keyword Score
    key_score = keyword_score(
        student_answer,
        reference_answer
    )

    # Word Count
    ref_len = len(reference_answer.split())

    stu_len = len(student_answer.split())

    # ================= SHORT ANSWERS =================
    if ref_len <= 10:

        final_score = (
            semantic_score * 0.70 +
            key_score * 0.30
        )

    # ================= LONG ANSWERS =================
    else:

        # Small Length Penalty
        length_ratio = min(
            stu_len / ref_len,
            1
        )

        length_score = length_ratio * 100

        final_score = (
            semantic_score * 0.75 +
            key_score * 0.15 +
            length_score * 0.10
        )

    # Clamp Score
    final_score = max(
        0,
        min(final_score, 100)
    )

    return {
        "score": round(final_score, 2)
    }