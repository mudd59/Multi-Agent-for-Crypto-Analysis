# LangGraph Multi-Agent Crypto Analyzer

Dieses Projekt ist die aufgeteilte Version deiner alten `app.py`.
Es nutzt:

- Streamlit für Dashboard
- LangGraph für Agent Workflow
- LangChain + OpenAI LLM für Prompt-basierte Analyse
- yfinance für Marktdaten
- RSS/Tavily für News
- einfache Sentiment-Analyse mit optionaler LLM-Verbesserung
- parallelen Researcher-Team-Flow: Bullish Agent und Bearish Agent analysieren unabhängig, danach Discussion/Debate Agent

## Start

```bash
cd crypto_multiagent_langgraph
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

Auf Mac/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

## API Keys

Das Projekt läuft auch ohne OpenAI API Key. Dann benutzt es einfache Regeln.
Mit OpenAI API Key werden Bullish/Bearish, Sentiment und Report besser erklärt.

## Wichtiger Hinweis

Das Projekt ist für Lernen, Analyse und Paper-Trading gedacht. Es ist keine Finanzberatung und führt keine echten Trades aus.

## Neuer Researcher-Team-Flow

Der Flow wurde angepasst, damit er wie in deiner Grafik funktioniert:

```text
Data Agent
  -> Indicator Agent
  -> News Agent
  -> Sentiment Agent
      -> Bullish Agent
      -> Bearish Agent
  -> Discussion / Debate Agent
  -> Trader Agent
  -> Risk Agent
  -> Manager Agent
  -> Backtest Agent
  -> Report Agent
```

Wichtig: `Bullish Agent` und `Bearish Agent` laufen nach dem `Sentiment Agent` getrennt. Beide Ergebnisse gehen danach gemeinsam in den `Debate Agent`. Danach macht der `Trader Agent` einen Vorschlag, der vom `Risk Agent` geprüft und vom `Manager Agent` final entschieden wird.
