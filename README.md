# Fake News & Misinformation Detection System

**Intra-IIT Hackathon 2026 — NLP / Trust & Safety**

A non-agentic AI/ML system for detecting likely misinformation in news articles and social media content. The system combines transformer-based text classification with explainability and a reviewer dashboard to help users identify and prioritize potentially misleading content.

> **Important:** The system provides model predictions, not verified fact-checking. A prediction of "fake" or "real" should not be treated as definitive proof of whether a claim is true or false.

---

## 1. Overview

The Fake News & Misinformation Detection System analyzes submitted news content and predicts whether it is:

* **Likely Misinformation**
* **Likely Real**

For every prediction, the system provides:

* Prediction label
* Confidence score
* Explainability information
* Review status
* Reviewer-oriented dashboard

The goal is to support human reviewers such as fact-checkers, researchers, journalists, and content moderators by helping them prioritize content that may require further investigation.

---

## 2. Key Features

### Content Analysis

Users can submit a news headline and article text through the Streamlit interface.

The system processes the text using the trained NLP classification model and generates a prediction with a confidence score.

### Explainable Predictions

The system uses an explainability layer to identify words/features that contributed to the model's prediction.

This helps users understand **why the model produced a particular prediction**, rather than providing only a classification label.

### Review Dashboard

The dashboard maintains analyzed items and displays them according to their predicted category and confidence.

The dashboard currently supports:

* Likely misinformation items
* Likely real items
* Confidence-based ranking
* Review status tracking

### Human-in-the-Loop Review

Each analyzed item is initially marked as:

`pending`

The dashboard is designed to support reviewer feedback such as:

* Confirming a prediction
* Dismissing a prediction
* Relabeling an item

Reviewer feedback is intended to remain separate from the original model prediction.

---

## 3. System Architecture

```text
                    ┌─────────────────────┐
                    │      User Input     │
                    │  Title + Article    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Preprocessing &   │
                    │     Tokenization    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Transformer-Based  │
                    │   Classification    │
                    │       Model         │
                    └──────────┬──────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼                         ▼
        ┌──────────────────┐      ┌──────────────────┐
        │   Prediction &   │      │  Explainability  │
        │    Confidence    │      │      Layer       │
        └────────┬─────────┘      └────────┬─────────┘
                 │                         │
                 └────────────┬────────────┘
                              ▼
                    ┌─────────────────────┐
                    │   Streamlit Review  │
                    │      Dashboard      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Human Reviewer      │
                    │ Feedback / Status   │
                    └─────────────────────┘
```

---

## 4. Project Structure

```text
fake-news-detection/
│
├── app.py
│
├── model_loader.py
│
├── explainability.py
│
├── requirements.txt
│
├── README.md
│
├── trained_model/
│   ├── config.json
│   ├── model.safetensors
│   ├── tokenizer.json
│   ├── tokenizer_config.json
│   └── ...
│
└── data/
    └── dataset.csv
```

### File Descriptions

| File / Folder       | Purpose                                       |
| ------------------- | --------------------------------------------- |
| `app.py`            | Main Streamlit application                    |
| `model_loader.py`   | Loads the trained model and tokenizer         |
| `explainability.py` | Generates model explanations                  |
| `trained_model/`    | Saved trained transformer model and tokenizer |
| `data/`             | Dataset used for development/evaluation       |
| `requirements.txt`  | Python dependencies                           |
| `README.md`         | Project documentation                         |

---

## 5. Machine Learning Pipeline

### Step 1 — Dataset

The model is trained using a labeled dataset containing real and fake news examples.

Each example contains:

```text
Title
Article Text
Label
```

Labels are represented as:

```text
0 → Fake / Misinformation
1 → Real
```

### Step 2 — Preprocessing

The title and article text are passed to the tokenizer as a text pair.

Conceptually:

```text
[CLS] Title [SEP] Article Text [SEP]
```

The sequence is truncated/padded to the configured maximum length.

### Step 3 — Model

A transformer-based sequence classification model is fine-tuned for binary classification.

The model produces two class logits:

```text
Fake
Real
```

The predicted class is obtained from the highest logit/probability.

### Step 4 — Confidence

The model output is converted into a confidence score representing the model's estimated probability for the predicted class.

### Step 5 — Explainability

The explainability module identifies important words/features associated with the prediction.

The explanation is intended to help reviewers understand the model's reasoning.

---

## 6. Training

Model training is performed separately from the Streamlit application.

The training pipeline consists of:

```text
Dataset
   ↓
Train / Validation Split
   ↓
Tokenization
   ↓
PyTorch Dataset
   ↓
DataLoader
   ↓
Transformer Fine-Tuning
   ↓
Validation
   ↓
Best Model Selection
   ↓
trained_model/
```

The best-performing model based on validation loss is saved for use by the Streamlit application.

The Streamlit application **does not retrain the model**.

---

## 7. Installation

### Requirements

* Python 3.10+
* pip
* Git
* PyTorch
* Transformers
* Streamlit
* Pandas
* NumPy
* Scikit-learn
* LIME / required explainability libraries

### Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd fake-news-detection
```

### Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 8. Running the Application

Make sure the trained model is present inside:

```text
trained_model/
```

Then run:

```bash
streamlit run app.py
```

The Streamlit application will open in your browser.

---

## 9. Using the Application

### Step 1 — Enter Content

Enter the headline/article content into the input interface.

### Step 2 — Analyze

Click:

```text
Analyze
```

The application sends the content through the trained model.

### Step 3 — View Prediction

The application displays:

```text
Prediction
Confidence
```

Example:

```text
Prediction: fake
Confidence: 91.2%
```

### Step 4 — View Explanation

The explainability component highlights important words/features that influenced the prediction.

### Step 5 — Review

The analyzed item is added to the reviewer dashboard.

Items can be prioritized according to their confidence and prediction category.

---

## 10. Reviewer Dashboard

The dashboard maintains a list of analyzed items.

Each item contains:

| Field      | Description           |
| ---------- | --------------------- |
| Index      | Item identifier       |
| Text       | Submitted content     |
| Prediction | Model prediction      |
| Confidence | Model confidence      |
| Status     | Current review status |

Items are separated into:

### Likely Misinformation

Content predicted as fake/misinformation is displayed here and ranked by confidence.

### Likely Real

Content predicted as real is displayed separately and ranked by confidence.

The dashboard is intended to help reviewers prioritize content requiring further investigation.

---

## 11. Explainability

The system does not treat the classifier as an opaque prediction engine.

For every prediction, the explainability module identifies features that contributed to the prediction.

The current implementation uses an explainability approach based on feature-level analysis.

Example:

```text
Prediction: Fake

Important features:

claim        +0.42
shocking     +0.31
government   +0.18
...
```

These explanations represent **model behavior**, not verified evidence that the underlying claim is true or false.

---

## 12. Evaluation

The classification model is evaluated using standard classification metrics:

* Accuracy
* Precision
* Recall
* F1 Score
* AUC

The validation pipeline also generates a classification report for the fake and real classes.

Example:

```text
              precision    recall    f1-score

fake             ...
real             ...

accuracy          ...
```

Failure cases should also be examined, particularly:

* False positives
* False negatives
* Low-confidence predictions
* Examples where linguistic patterns mislead the classifier

---

## 13. Responsible Use

This system is intended as a **decision-support tool**, not an automated fact-checker.

A model prediction should not be interpreted as definitive evidence that an article or claim is true or false.

Potential limitations include:

* Dataset bias
* Limited training data
* Distribution shift
* Missing source metadata
* Incomplete propagation information
* Linguistic patterns that may correlate with misinformation without proving it
* Incorrect model predictions

Human review remains important when making final judgments about potentially misleading content.

---

## 14. Hackathon Requirements Addressed

The system is designed around the core requirements of the Intra-IIT Hackathon:

| Requirement        | Implementation                       |
| ------------------ | ------------------------------------ |
| Data ingestion     | Labeled news dataset                 |
| Text preprocessing | Transformer tokenizer                |
| Classification     | Transformer-based binary classifier  |
| Confidence         | Prediction confidence score          |
| Explainability     | Explainability module                |
| Review dashboard   | Streamlit dashboard                  |
| Ranking            | Confidence-based ranking             |
| Human review       | Review status / feedback workflow    |
| Evaluation         | Accuracy, Precision, Recall, F1, AUC |
| Product interface  | Streamlit application                |

The hackathon brief specifically requires an interface for submitting content, integration with the trained misinformation model, confidence scores and explanations, a reviewer dashboard, and a feedback workflow.

---

## 15. Demo Flow

For the final demonstration, the recommended flow is:

```text
1. Open the Streamlit application
             ↓
2. Submit a news headline/article
             ↓
3. Click "Analyze"
             ↓
4. Display prediction + confidence
             ↓
5. Show explanation
             ↓
6. Add item to review dashboard
             ↓
7. Show confidence-based prioritization
             ↓
8. Reviewer confirms / dismisses / relabels
             ↓
9. Store reviewer feedback
```

This demonstrates the complete path from content analysis to human review.

---

## 16. Future Extensions

Possible extensions include:

* Article URL analysis
* Batch CSV analysis
* Downloadable CSV/PDF reports
* Source credibility profiles
* Historical source analysis
* Propagation signal integration
* Browser extension
* Multi-article comparison
* Contradictory claim detection
* Multilingual support
* Reviewer accounts and roles

These correspond to optional extensions described in the hackathon brief.

---

## 17. Limitations

The current system should not be considered a replacement for professional fact-checking.

Its predictions depend on:

1. The quality and distribution of the training dataset.
2. The transformer model's learned representations.
3. The availability and quality of input text.
4. The quality of the explainability method.
5. The difference between training data and real-world news.

Therefore, predictions should be interpreted together with the provided explanations and human review.

---

## 18. Team

**Intra-IIT Hackathon 2026**

**Track:** NLP / Trust & Safety
**Category:** Non-Agentic AI/ML System

```
