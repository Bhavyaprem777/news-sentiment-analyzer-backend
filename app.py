from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import spacy
import json
from datetime import datetime
import os
HISTORY_FILE = "history.json"

app = Flask(__name__)
CORS(app)

# ✅ Load Pretrained Sentiment Analysis Model (BERT)
sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# ✅ Load spaCy for Key Phrase Extraction
nlp = spacy.load("en_core_web_sm")

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.json
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # ✅ Run Sentiment Analysis with BERT
    bert_results = sentiment_analyzer(text)[0]  # Example: {'label': '4 stars', 'score': 0.98}

    # ✅ Convert BERT output to a human-readable format
    label_map = {
        "1 star": "Very Negative",
        "2 stars": "Negative",
        "3 stars": "Neutral",
        "4 stars": "Positive",
        "5 stars": "Very Positive"
    }
    sentiment = label_map.get(bert_results["label"], "Unknown")

    # ✅ Extract Key Phrases using spaCy
    doc = nlp(text)
    key_phrases = [chunk.text for chunk in doc.noun_chunks]  # Extract noun phrases

    # ✅ Sentence-wise Sentiment Analysis
    sentence_sentiments = []
    for sentence in doc.sents:
        sentence_result = sentiment_analyzer(sentence.text)[0]
        sentence_sentiments.append({
            "sentence": sentence.text,
            "sentiment": label_map.get(sentence_result["label"], "Unknown"),
            "score": round(sentence_result["score"], 3)
        })

    return jsonify({
        "text": text,
        "overall_sentiment": sentiment,
        "score": round(bert_results["score"], 3),
        "raw_label": bert_results["label"],  # e.g., "4 stars"
        "key_phrases": key_phrases,
        "sentence_analysis": sentence_sentiments
    })
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.json
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    if len(text.split()) > 100:  # ✅ Summarize if the text is longer than 100 words
        summary = summarizer(text, max_length=100, min_length=50, do_sample=False)[0]["summary_text"]
        return jsonify({"summary": summary})
    else:
        return jsonify({"summary": text})  # ✅ Return original text if already short
# Save analysis result to history
@app.route('/save-history', methods=['POST'])
def save_history():
    data = request.json
    entry = {
        "text": data.get("text"),
        "overall_sentiment": data.get("overall_sentiment"),
        "score": data.get("score"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "key_phrases": data.get("key_phrases", []),
        "summary": data.get("summary", ""),
    }

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append(entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    return jsonify({"message": "History saved successfully"})


# Get all history entries
@app.route('/get-history', methods=['GET'])
def get_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
        return jsonify(history)
    else:
        return jsonify([])
@app.route('/delete-entry', methods=['DELETE'])
def delete_entry():
    data = request.json
    timestamp = data.get("timestamp")

    if not timestamp:
        return jsonify({"error": "Missing timestamp"}), 400

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)

        updated_history = [entry for entry in history if entry["timestamp"] != timestamp]

        with open(HISTORY_FILE, "w") as f:
            json.dump(updated_history, f, indent=2)

        return jsonify({"message": "Entry deleted successfully"})
    else:
        return jsonify({"error": "History file not found"}), 404



if __name__ == '__main__':
    app.run(debug=True)
