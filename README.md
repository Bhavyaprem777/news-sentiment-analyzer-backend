# News Sentiment Analyzer

A web app that analyzes the sentiment of text input (like news or articles), summarizes long texts, displays insights, charts, and maintains history.

## 📄 Pages & Features

- **Home**  
  Explains how the app works and its purpose.

- **Analyzer**  
  Input any text → advanced sentiment analysis runs → returns:  
  • Overall sentiment (Very Negative / Negative / Neutral / Positive / Very Positive)  
  • Sentiment score  
  • Key phrases extracted using NLP  
  • Sentence-wise sentiment breakdown  
  • Pie chart & bar graph visualizations  

- **History**  
  Shows your past analyses. You can delete entries if not needed.

## 🛠️ Tech & Tools

- Frontend: React / JavaScript / Tailwind CSS  
- Backend: Flask  
- NLP & ML: HuggingFace Transformers (BERT for sentiment, BART for summarization), spaCy  
- Storage: Local JSON file for history  
- Deployment: Frontend hosted on Vercel  

## 🚀 API Endpoints

- `POST /analyze` → Analyze sentiment & extract key phrases  
- `POST /summarize` → Summarize text longer than 100 words  
- `POST /save-history` → Save analysis to history  
- `GET /get-history` → Retrieve all saved analyses  
- `DELETE /delete-entry` → Delete a history entry by timestamp  

## 🚀 How to Run Locally

1. Clone the repo  
   ```bash
   git clone https://github.com/Bhavyaprem777/news-sentiment-analyzer-backend.git
2.Install dependencies
3.Run the Flask backend
  python app.py
4.🌐 Live Demo
https://news-sentiment-analyzer-frontend.vercel.app/
5. Video Demo
https://drive.google.com/file/d/1GaCzZ-UQ-wYyz3iQ67thYXcKaFsy4v9h/view
