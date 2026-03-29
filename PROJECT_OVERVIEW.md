# 📊 HỆ THỐNG TƯ VẤN ĐẦU TƯ CHỨNG KHOÁN THÔNG MINH

## 🎯 Mục tiêu dự án

Xây dựng một hệ thống AI tư vấn đầu tư chứng khoán có khả năng:
- ✅ **Hiểu ngữ cảnh thị trường** (Market Context Understanding)
- ✅ **Đưa ra quyết định đầu tư** (Investment Decision Making)
- ✅ **Giải thích lý do** (Explainable AI)

---

## 📥 INPUT - OUTPUT

### Input (Dữ liệu đầu vào)
```json
{
  "stock_code": "VIC",
  "date": "2025-12-20",
  "price_data": {
    "open": 245000,
    "high": 250000,
    "low": 243000,
    "close": 248000,
    "volume": 5200000
  },
  "technical_indicators": {
    "RSI": 68.5,
    "MACD": 2.3,
    "MA20": 240000,
    "MA50": 230000,
    "Bollinger_Upper": 255000,
    "Bollinger_Lower": 235000
  },
  "sentiment_score": 0.65,
  "news_summary": [
    "VIC reaches new all-time high...",
    "Vingroup expands into renewable energy..."
  ],
  "exchange_rate": {
    "USD_VND": 25000
  }
}
```

### Output (Quyết định + Giải thích)
```json
{
  "decision": "BUY",
  "confidence": 0.85,
  "reasoning": "Based on historical patterns, when RSI is around 68 and sentiment score is positive (0.65), similar market conditions in the past (2024-03-15, 2024-08-22) showed continued upward momentum. The stock broke resistance at 245K with strong volume support. Positive news sentiment about renewable energy expansion aligns with sector rotation trends.",
  "risk_level": "Medium",
  "suggested_entry": 248000,
  "stop_loss": 238000,
  "target_price": 268000
}
```

---

## 🏗️ KIẾN TRÚC HỆ THỐNG (System Architecture)

```
┌─────────────────────────────────────────────────────────────────┐
│                     INPUT: Market Data JSON                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  GIAI ĐOẠN 1: DATA ENGINEERING & FEATURE EXTRACTION             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │ Price Data   │  │ News Data    │  │ Technical           │   │
│  │ Collection   │  │ Scraping     │  │ Indicators          │   │
│  └──────┬───────┘  └──────┬───────┘  └─────────┬───────────┘   │
│         │                  │                     │               │
│         │                  ▼                     │               │
│         │          ┌──────────────┐             │               │
│         │          │   FinGPT     │             │               │
│         │          │  Sentiment   │             │               │
│         │          │   Analysis   │             │               │
│         │          └──────┬───────┘             │               │
│         │                  │                     │               │
│         └──────────────────┴─────────────────────┘               │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  GIAI ĐOẠN 2: VECTOR DATABASE (Memory System)                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  ChromaDB / Faiss / Pinecone                              │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │  │
│  │  │ Day 1   │ │ Day 2   │ │ Day 3   │ │ Day N   │ ...    │  │
│  │  │ Vector  │ │ Vector  │ │ Vector  │ │ Vector  │        │  │
│  │  │+ Outcome│ │+ Outcome│ │+ Outcome│ │+ Outcome│        │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘        │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  GIAI ĐOẠN 3: RETRIEVAL (RAG + RDES)                            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Today's Data → Search Vector DB → Top K Similar Days    │  │
│  │                                                           │  │
│  │  Option 1 (Basic):  kNN / Cosine Similarity              │  │
│  │  Option 2 (Advanced): RDES Agent                         │  │
│  │    - Relevance: Find similar market conditions           │  │
│  │    - Diversity: Include both Bull & Bear examples        │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  GIAI ĐOẠN 4: REASONING (ICL - In-Context Learning)             │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Prompt Construction:                                     │  │
│  │  ┌─────────────────────────────────────────────────────┐ │  │
│  │  │ SYSTEM: You are an expert financial advisor...      │ │  │
│  │  │                                                      │ │  │
│  │  │ CONTEXT: Historical Examples (from RAG)             │ │  │
│  │  │ - Example 1: [2024-03-15] Similar RSI → Price +8%  │ │  │
│  │  │ - Example 2: [2024-08-22] Similar pattern → +5%    │ │  │
│  │  │ - Example 3: [2024-06-10] High RSI → Correction    │ │  │
│  │  │                                                      │ │  │
│  │  │ INPUT: Today's Market Data [JSON]                   │ │  │
│  │  │                                                      │ │  │
│  │  │ TASK: Analyze and decide Buy/Hold/Sell with reason │ │  │
│  │  └─────────────────────────────────────────────────────┘ │  │
│  │                           │                               │  │
│  │                           ▼                               │  │
│  │                  ┌─────────────────┐                      │  │
│  │                  │   Main LLM      │                      │  │
│  │                  │ GPT-4 / Claude  │                      │  │
│  │                  │  Llama 3 70B    │                      │  │
│  │                  └────────┬────────┘                      │  │
│  └───────────────────────────┼─────────────────────────────────┘  │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  GIAI ĐOẠN 5: VERIFICATION (TTRL - Optional Advanced)           │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Generate Multiple Scenarios:                            │  │
│  │  - Scenario 1: BUY  (Bullish case)                       │  │
│  │  - Scenario 2: HOLD (Neutral case)                       │  │
│  │  - Scenario 3: SELL (Bearish case)                       │  │
│  │                                                           │  │
│  │  Value Model Scoring:                                    │  │
│  │  - Safety Score                                          │  │
│  │  - Logic Consistency                                     │  │
│  │  - Risk Assessment                                       │  │
│  │                                                           │  │
│  │  → Select Best Decision with Highest Score               │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              OUTPUT: Decision + Reasoning + Risk                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔑 CÁC KỸ THUẬT CHÍNH (Key Techniques)

### 1. 📰 Sentiment Analysis với FinGPT

**Vai trò**: Chuyển đổi tin tức văn bản thành điểm số cảm xúc

**Model**: `FinGPT/fingpt-sentiment_llama2-13b_lora`

**Quy trình**:
```
News Text → FinGPT → {Positive, Negative, Neutral}
                  ↓
           Sentiment Score (-1 to +1)
```

**Ví dụ**:
- *"VIC reaches all-time high with strong volume"* → **Positive (+0.8)**
- *"Market correction expected due to Fed rate hike"* → **Negative (-0.6)**
- *"Company maintains dividend policy"* → **Neutral (0.0)**

---

### 2. 🔍 RAG (Retrieval-Augmented Generation)

**Vai trò**: Tìm kiếm và sử dụng dữ liệu lịch sử tương tự

**Cách hoạt động**:
1. **Vectorize**: Mỗi ngày giao dịch trong quá khứ được chuyển thành vector
2. **Store**: Lưu vào Vector Database (ChromaDB/Faiss)
3. **Retrieve**: Khi có dữ liệu hôm nay, tìm K ngày giống nhất trong quá khứ
4. **Augment**: Đưa các ví dụ lịch sử vào Prompt cho LLM học

**Lợi ích**:
- ✅ LLM học từ kinh nghiệm thực tế (không chỉ kiến thức training)
- ✅ Tận dụng pattern lặp lại trong thị trường tài chính
- ✅ Giảm hallucination (ảo giác) của LLM

---

### 3. 🎓 ICL (In-Context Learning)

**Vai trò**: Dạy LLM "học trong ngữ cảnh" thông qua ví dụ

**Phương pháp**:
```python
# Prompt Structure
prompt = f"""
You are an expert financial advisor.

Here are similar historical situations:

Example 1 (2024-03-15):
Market Data: RSI=67, Sentiment=0.7, Volume=High
Outcome: Price increased 8% next day
Reason: Strong momentum continuation

Example 2 (2024-08-22):
Market Data: RSI=68, Sentiment=0.6, Volume=High  
Outcome: Price increased 5% next day
Reason: Positive sector rotation

Example 3 (2024-06-10):
Market Data: RSI=72, Sentiment=0.5, Volume=Low
Outcome: Price dropped 3% next day
Reason: Overbought correction with weak volume

Now analyze today's situation:
{today_data}

Provide your decision (BUY/HOLD/SELL) and explain why.
"""
```

**Chain-of-Thought (CoT)**:
LLM tự tạo chuỗi suy luận trước khi đưa ra quyết định:
```
"Looking at the examples:
1. When RSI is high (67-68) AND sentiment is positive (0.6-0.7) AND volume is high → Usually bullish
2. When RSI exceeds 72 with low volume → Correction risk
3. Today's RSI is 68.5 with high volume and positive sentiment → More similar to Example 1 & 2
4. Therefore, I recommend BUY with target +6-8%"
```

---

### 4. 🎯 RDES (Relevance-Diversity Enhanced Selection)

**Vấn đề với RAG thông thường**:
- Chỉ tìm những ngày "giống nhất" về chỉ số
- Thiếu đa dạng góc nhìn → Dễ bias

**Giải pháp RDES**:
Sử dụng một Agent (trained with RL) để chọn ví dụ sao cho:

**Relevance (Tính liên quan)**:
- Cấu trúc thị trường tương đồng (RSI, MACD, Volume pattern)

**Diversity (Tính đa dạng)**:
- Bao gồm cả kịch bản Tăng VÀ Giảm trong điều kiện tương tự
- Giúp LLM nhìn đa chiều, không "mù quáng" theo trend

**Ví dụ so sánh**:

| Method | Ví dụ được chọn |
|--------|-----------------|
| **RAG thường** | 5 ngày giống nhau về RSI, cả 5 đều tăng giá → LLM có thể quá tự tin |
| **RDES** | 3 ngày tăng giá + 2 ngày giảm giá (cùng RSI) → LLM cân nhắc cả rủi ro |

---

### 5. ⚡ TTRL (Test-Time Reinforcement Learning)

**Vai trò**: Kiểm chứng và tự sửa sai trước khi output

**Vấn đề**:
- LLM đôi khi quá tự tin hoặc bị ảo giác
- Quyết định thiếu kiểm soát rủi ro

**Giải pháp TTRL**:

**Bước 1**: Generate Multiple Scenarios
```
LLM tạo 3 kịch bản song song:
- Kịch bản A: BUY (Lý do: Technical breakout + positive news)
- Kịch bản B: HOLD (Lý do: Wait for confirmation at resistance)
- Kịch bản C: SELL (Lý do: Overbought, take profit)
```

**Bước 2**: Value Model Scoring
```python
def score_scenario(scenario, market_data, risk_tolerance):
    safety_score = calculate_downside_risk(scenario)
    logic_score = check_reasoning_consistency(scenario)
    historical_accuracy = compare_with_past_similar_decisions(scenario)
    
    total_score = (safety_score * 0.4 + 
                   logic_score * 0.3 + 
                   historical_accuracy * 0.3)
    return total_score
```

**Bước 3**: Self-Correction & Selection
```
Scores:
- Scenario A (BUY):  0.85 ← Highest score
- Scenario B (HOLD): 0.72
- Scenario C (SELL): 0.45

→ Final Decision: BUY (with reasoning from Scenario A)
```

---

## 📋 QUY TRÌNH TRIỂN KHAI (Implementation Roadmap)

### Phase 1: MVP (Minimum Viable Product) - 2-3 tuần

**Mục tiêu**: Có hệ thống chạy được end-to-end

**Tasks**:
1. ✅ Thu thập dữ liệu lịch sử giá (VIC từ 2023-2025)
2. ✅ Scrape tin tức liên quan VIC
3. ✅ Dịch tin tức Việt → Anh (script `convert_VIC.ipynb`)
4. ✅ Chạy FinGPT sentiment trên tin tức
5. ✅ Tính toán technical indicators
6. ✅ Xây dựng Vector DB đơn giản (ChromaDB)
7. ✅ Implement RAG cơ bản (kNN search)
8. ✅ Tạo prompt template cho LLM
9. ✅ Test với GPT-4 / Claude

**Deliverable**: 
- Hệ thống nhận JSON → Trả về decision + reasoning

---

### Phase 2: Optimization - 2-3 tuần

**Mục tiêu**: Cải thiện chất lượng quyết định

**Tasks**:
1. ⚙️ Phân tích lỗi của Phase 1 (Khi nào hệ thống sai?)
2. ⚙️ Fine-tune prompt engineering
3. ⚙️ Implement RDES (nếu kịp):
   - Train một agent đơn giản bằng RL
   - Hoặc dùng heuristic rules để chọn ví dụ đa dạng
4. ⚙️ Thêm feature engineering (thêm indicators)
5. ⚙️ Optimize Vector DB (thử Faiss nếu ChromaDB chậm)

**Deliverable**: 
- Accuracy tăng 10-15% so với Phase 1

---

### Phase 3: Reliability & Evaluation - 1-2 tuần

**Mục tiêu**: Đảm bảo hệ thống đáng tin cậy cho production

**Tasks**:
1. 🛡️ Implement TTRL (nếu kịp thời gian):
   - Multi-scenario generation
   - Value model scoring
2. 🛡️ Add risk management layer
3. 📊 Backtesting trên dữ liệu 2024
4. 📊 So sánh với baseline:
   - Buy & Hold
   - Simple Moving Average strategy
   - Random trading
5. 📝 Viết báo cáo kết quả cho khóa luận

**Deliverable**: 
- Báo cáo đầy đủ với metrics, charts, analysis

---

## 📊 ĐÁNH GIÁ HỆ THỐNG (Evaluation Metrics)

### 1. Trading Performance Metrics

```python
# Backtesting Results Example
Total Trades: 120
Win Rate: 65% (78 wins / 42 losses)
Average Return per Trade: +2.3%
Maximum Drawdown: -8.5%
Sharpe Ratio: 1.8

Comparison:
- AI System:        +32% annual return
- Buy & Hold:       +18% annual return
- Market Index:     +15% annual return
```

### 2. Decision Quality Metrics

- **Precision**: Trong số các lần khuyên BUY, bao nhiêu % thực sự sinh lời?
- **Recall**: Trong số các cơ hội tốt, hệ thống catch được bao nhiêu %?
- **F1-Score**: Cân bằng giữa Precision và Recall

### 3. Reasoning Quality (Định tính)

**Checklist đánh giá reasoning**:
- ✅ Có mention đến historical examples không?
- ✅ Logic có mâu thuẫn nội tại không?
- ✅ Có cân nhắc rủi ro không?
- ✅ Giải thích có dễ hiểu cho người không chuyên không?

---

## 🔬 VAI TRÒ CỦA TỪNG MODEL

| Model | Vai trò | Input | Output |
|-------|---------|-------|--------|
| **FinGPT** | Sentiment Analyst | News text (English) | Sentiment label + score |
| **Embedding Model** | Feature Extractor | Market data (price, indicators, sentiment) | Vector representation |
| **Vector DB** | Memory System | Historical vectors | Top-K similar examples |
| **RDES Agent** *(Optional)* | Smart Retriever | Today's vector + Historical DB | Diverse & relevant examples |
| **Main LLM** | Decision Maker | Prompt (System + Context + Input) | Decision + Reasoning |
| **Value Model** *(Optional)* | Verifier | Multiple scenarios | Best scenario score |

---

## 🎓 ĐÓNG GÓP KHOA HỌC (Research Contributions)

### Điểm mới của đề tài:

1. **Tích hợp đa nguồn dữ liệu**:
   - Kết hợp Technical Analysis + Sentiment Analysis + Historical Patterns
   - Không chỉ dựa vào một loại tín hiệu

2. **Explainable AI**:
   - Không chỉ cho kết quả BUY/SELL
   - Giải thích rõ "tại sao" dựa trên bằng chứng lịch sử
   - Người dùng có thể verify logic

3. **Context-Aware Decision Making**:
   - Sử dụng ICL để LLM học từ ngữ cảnh tương tự
   - Không chỉ dựa vào kiến thức training sẵn

4. **Risk-Aware System** *(Nếu làm TTRL)*:
   - Tự đánh giá rủi ro trước khi output
   - Tạo ra quyết định "conservative" và "reliable" hơn

---

## 🚀 KẾT LUẬN

Hệ thống này kết hợp:
- **Specialized Model** (FinGPT cho sentiment)
- **General Model** (GPT-4/Claude cho reasoning)
- **Retrieval System** (RAG cho historical context)
- **Verification Layer** *(Optional)* (TTRL cho reliability)

Tạo nên một AI advisor có thể:
- ✅ Đọc tin tức
- ✅ Phân tích kỹ thuật
- ✅ Học từ quá khứ
- ✅ Đưa ra quyết định có căn cứ
- ✅ Giải thích rõ ràng
- ✅ Kiểm soát rủi ro

**Target Users**: 
- Nhà đầu tư cá nhân cần công cụ hỗ trợ quyết định
- Người mới bắt đầu muốn học cách phân tích từ AI

**Future Work**:
- Mở rộng sang nhiều mã cổ phiếu
- Thêm portfolio optimization
- Real-time trading integration
- Multi-agent system (Bull Agent vs Bear Agent debate)

---

## 📚 TÀI LIỆU THAM KHẢO

1. **FinGPT**: [FinGPT: Open-Source Financial Large Language Models](https://arxiv.org/abs/2306.06031)
2. **RAG**: [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
3. **ICL**: [Language Models are Few-Shot Learners (GPT-3)](https://arxiv.org/abs/2005.14165)
4. **RDES**: [Improving Retrieval in RAG Systems via Diversity](https://arxiv.org/abs/2401.xxxxx)
5. **TTRL**: [Test-Time Training Can Close the Natural Distribution Shift](https://arxiv.org/abs/2209.07511)

---

**Author**: [Your Name]  
**Project**: Stock Investment Advisory System  
**Date**: December 2025  
**Status**: In Development
