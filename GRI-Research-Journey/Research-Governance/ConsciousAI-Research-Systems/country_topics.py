"""Inspectable multinomial Naive Bayes topic baseline, not political forecasting.

Author-created multilingual examples are instructional training data. Scores are
uncalibrated model weights, never probabilities of policy or business outcomes.
"""
from collections import Counter
import hashlib
import json
import math
import re
import unicodedata

VERSION = "gri-country-topics-nb-0.1"
EXAMPLES = {
    "political_institutions": [
        "Election parliament coalition president government constitutional reform",
        "Voters election electoral commission legislature governing coalition",
        "Eleição governo presidente congresso reforma constitucional democracia",
        "Elecciones gobierno presidente congreso reforma constitucional democracia",
        "Political institutions electoral authority cabinet leadership transition",
        "Instituições políticas eleições parlamento coalizão autoridade eleitoral",
    ],
    "trade_investment": [
        "Trade tariffs exports imports investment customs market access agreement",
        "WTO commerce investment supply chains export trade agreement",
        "Comércio tarifas exportação importação investimento acordo comercial",
        "Comercio aranceles exportaciones importaciones inversión acuerdo comercial",
        "Foreign investment trade supply chains customs export restrictions",
        "Mercosul Mercosur comércio comercio exportações integración econômica",
    ],
    "organizational_management": [
        "Business operations management workforce training productivity strategy",
        "Company managers organizational leadership employees skills training",
        "Gestão empresas trabalhadores produtividade capacitação liderança",
        "Gestión empresas trabajadores productividad formación liderazgo",
        "Organizational management skills workforce business operations",
        "Empresas gestão empresarial empleo organización capacitación",
    ],
    "algorithmic_management": [
        "Algorithmic management platform workers automated decisions pay appeals",
        "Gig drivers rideshare delivery platform labor worker protections",
        "Gestão algorítmica plataformas motoristas entregadores trabalho remuneração",
        "Gestión algorítmica plataformas conductores repartidores trabajo remuneración",
        "Automated workplace surveillance worker rights algorithms scheduling",
        "Plataformas digitais trabalho algoritmos direitos dos trabalhadores",
    ],
    "artificial_intelligence": [
        "Artificial intelligence machine learning models AI governance computing",
        "AI regulation neural networks data centers artificial intelligence",
        "Inteligência artificial aprendizado máquina modelos regulação computação",
        "Inteligencia artificial aprendizaje automático modelos regulación cómputo",
        "Artificial intelligence public procurement compute AI infrastructure",
        "Inteligência inteligencia artificial IA governança gobernanza inovação",
    ],
}
HOLDOUT = {
    "political_institutions": ["Election coalition parliament transition", "Elecciones congreso gobierno", "Eleição presidente democracia"],
    "trade_investment": ["Trade tariffs customs agreement", "Comercio exportaciones aranceles", "Comércio investimento importação"],
    "organizational_management": ["Business workforce productivity training", "Gestión empresas formación", "Gestão produtividade capacitação"],
    "algorithmic_management": ["Platform workers pay appeals", "Conductores plataformas remuneración", "Motoristas entregadores direitos"],
    "artificial_intelligence": ["Artificial intelligence neural models", "Inteligencia artificial regulación", "Inteligência artificial computação"],
}


def normalize(text):
    return "".join(c for c in unicodedata.normalize("NFKD", text.casefold())
                   if not unicodedata.combining(c))


def tokens(text):
    return re.findall(r"[a-z]{3,}", normalize(text))


class TopicModel:
    def __init__(self):
        self.counts = {label: Counter(tokens(" ".join(rows))) for label, rows in EXAMPLES.items()}
        self.vocabulary = set().union(*(set(c) for c in self.counts.values()))
        self.training_sha256 = hashlib.sha256(json.dumps(EXAMPLES, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

    def predict(self, text):
        counts = Counter(tokens(text[:10000]))
        overlap = set(counts) & self.vocabulary
        scores = {}
        for label, training in self.counts.items():
            denominator = sum(training.values()) + len(self.vocabulary)
            scores[label] = sum(n * math.log((training[t] + 1) / denominator)
                                for t, n in counts.items() if t in self.vocabulary)
        maximum = max(scores.values())
        weights = {k: math.exp(v - maximum) for k, v in scores.items()}
        total = sum(weights.values())
        ranked = sorted(((k, v / total) for k, v in weights.items()), key=lambda x: (-x[1], x[0]))
        label, weight = ranked[0]
        accepted = len(overlap) >= 2 and weight >= 0.55 and weight - ranked[1][1] >= 0.15
        return {"label": label if accepted else "needs_review", "suggested_label": label,
                "score": round(weight, 4), "score_type": "uncalibrated_topic_weight",
                "known_terms": len(overlap), "abstained": not accepted,
                "model_version": VERSION, "human_review_required": True}

    def evaluation(self):
        pairs = [(expected, self.predict(text)["label"]) for expected, rows in HOLDOUT.items() for text in rows]
        metrics = {}
        for label in EXAMPLES:
            tp = sum(a == label and b == label for a, b in pairs)
            fp = sum(a != label and b == label for a, b in pairs)
            fn = sum(a == label and b != label for a, b in pairs)
            precision = tp / (tp + fp) if tp + fp else 0
            recall = tp / (tp + fn) if tp + fn else 0
            metrics[label] = {"precision": precision, "recall": recall,
                              "f1": 2 * precision * recall / (precision + recall) if precision + recall else 0}
        return {"model_version": VERSION, "method": "multinomial_naive_bayes_laplace_smoothing",
                "training_sha256": self.training_sha256, "training_examples": sum(map(len, EXAMPLES.values())),
                "evaluation_examples": len(pairs), "evaluation_origin": "author_created_instructional_holdout",
                "independently_labeled": False, "production_validated": False,
                "accuracy": sum(a == b for a, b in pairs) / len(pairs),
                "macro_f1": sum(x["f1"] for x in metrics.values()) / len(metrics),
                "abstention_rate": sum(b == "needs_review" for _, b in pairs) / len(pairs),
                "per_topic": metrics,
                "notice": "Small instructional evaluation only. Not evidence of real news accuracy, political direction, causal effects, or predictive validity."}
