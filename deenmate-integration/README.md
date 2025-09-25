# DeenMate MCP Server Integration

This directory contains specialized tools and configurations for integrating the MCP server with the DeenMate Islamic utility app.

## 🕌 Overview

DeenMate is a comprehensive Islamic utility app that helps Muslims with:
- Prayer times tracking
- Fasting schedules 
- Zakat calculations
- Religious guidance
- Educational content
- Community features

This MCP server integration provides AI-powered Islamic guidance and content generation using your local LLM.

## 🛠️ Islamic Tools Available

### 1. **Islamic Guidance** (`islamic_guidance`)
Provides authentic Islamic guidance based on Quran and Sunnah.

**Parameters:**
- `question` (required): Islamic question for guidance
- `context` (optional): Additional context
- `madhab` (optional): School of thought (Hanafi, Shafi, Maliki, Hanbali)

### 2. **Quran Explanation** (`quran_explanation`)
Explains Quranic verses with context and commentary.

**Parameters:**
- `verse_reference` (required): Verse reference (e.g., "Al-Fatiha 1:1-7")
- `verse_text` (optional): Actual verse text
- `explanation_type` (optional): tafsir, context, practical, linguistic

### 3. **Hadith Guidance** (`hadith_guidance`)
Provides Hadith-based guidance and explanations.

**Parameters:**
- `topic` (required): Topic for Hadith guidance
- `hadith_text` (optional): Specific Hadith text
- `collection` (optional): Preferred collection (Bukhari, Muslim, etc.)

### 4. **Prayer Guidance** (`prayer_guidance`)
Guidance on Salah (prayer) related questions.

**Parameters:**
- `prayer_question` (required): Prayer-related question
- `prayer_type` (optional): Fajr, Dhuhr, Asr, Maghrib, Isha, etc.
- `situation` (optional): Special circumstances

### 5. **Zakat Calculator** (`zakat_calculator`)
Calculate Zakat obligations with Islamic guidance.

**Parameters:**
- `wealth_type` (required): cash, gold, silver, business, etc.
- `amount` (required): Amount of wealth
- `currency` (optional): Currency (USD, BDT, etc.)
- `calculation_method` (optional): standard or detailed

### 6. **Islamic Content Generator** (`islamic_content_generator`)
Generate Islamic educational content for DeenMate.

**Parameters:**
- `content_type` (required): daily_reminder, educational_article, dua, etc.
- `topic` (optional): Specific Islamic topic
- `target_audience` (optional): general, youth, adults, families, converts
- `length` (optional): short, medium, long

### 7. **Halal/Haram Guidance** (`halal_haram_guidance`)
Guidance on permissible and forbidden matters.

**Parameters:**
- `item_or_action` (required): Item or action to evaluate
- `context` (optional): Additional circumstances
- `evidence_level` (optional): basic, detailed, scholarly

### 8. **Ramadan Fasting Guide** (`ramadan_fasting_guide`)
Comprehensive Ramadan and fasting guidance.

**Parameters:**
- `fasting_question` (required): Fasting-related question
- `fasting_type` (optional): Ramadan, voluntary, make_up, kaffarah
- `personal_situation` (optional): Special circumstances

## 📚 Islamic Resources

### 1. **Daily Islamic Content** (`islamic://daily/content`)
Daily Quranic verses, Hadiths, and reflections for the app.

### 2. **Prayer Times** (`islamic://prayer/times`)
Current prayer times and Qibla direction information.

### 3. **Islamic Calendar** (`islamic://calendar/events`)
Upcoming Islamic holidays and significant dates.

### 4. **Content Library** (`islamic://content/library`)
Curated Islamic educational content for DeenMate.

## 🚀 Setup for DeenMate

### 1. Run the Enhanced Server

```bash
# Use the DeenMate-specific server
cd deenmate-integration
python deenmate_mcp_server.py
```

### 2. Integration with DeenMate Backend

**Add to your TypeScript backend:**

```typescript
// deenmate-backend integration
import { MCPClient } from './mcp-client';

const mcpClient = new MCPClient('http://your-gpu-server:8080');

// Example: Get Islamic guidance
async function getIslamicGuidance(question: string) {
  return await mcpClient.callTool('islamic_guidance', {
    question: question,
    madhab: 'Hanafi' // or user preference
  });
}

// Example: Generate daily content
async function getDailyContent() {
  return await mcpClient.getResource('islamic://daily/content');
}
```

### 3. Flutter App Integration

**Add to your Dart/Flutter app:**

```dart
// deenmate-app integration
class IslamicAIService {
  static const String mcpServerUrl = 'http://your-server:8080';
  
  Future<String> getIslamicGuidance(String question) async {
    final response = await http.post(
      Uri.parse('$mcpServerUrl/tools/call'),
      body: jsonEncode({
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'tools/call',
        'params': {
          'name': 'islamic_guidance',
          'arguments': {'question': question}
        }
      }),
    );
    // Handle response
  }
  
  Future<Map<String, dynamic>> getDailyContent() async {
    // Get daily Islamic content for app
  }
}
```

## 🧪 Testing Islamic Tools

### Test Islamic Guidance
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "islamic_guidance",
    "arguments": {
      "question": "What are the conditions for valid prayer?",
      "madhab": "Hanafi"
    }
  }
}
```

### Test Zakat Calculator
```json
{
  "jsonrpc": "2.0", 
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "zakat_calculator",
    "arguments": {
      "wealth_type": "cash",
      "amount": 10000,
      "currency": "USD"
    }
  }
}
```

### Test Daily Content
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "resources/read",
  "params": {
    "uri": "islamic://daily/content"
  }
}
```

## 🎯 DeenMate Use Cases

### 1. **Prayer Time Reminders**
- Generate personalized prayer reminders
- Provide guidance for prayer in special circumstances
- Explain prayer procedures and requirements

### 2. **Ramadan Features**
- Fasting guidance and rules
- Suhoor and Iftar recommendations
- Spiritual reflection content

### 3. **Zakat Management** 
- Automated Zakat calculations
- Educational content about Zakat
- Guidance on Zakat distribution

### 4. **Educational Content**
- Daily Islamic reflections
- Quranic verse explanations
- Hadith of the day with context

### 5. **Q&A Features**
- User questions answered with Islamic guidance
- Halal/Haram clarifications
- Religious practice guidance

## 🔧 Configuration

### Environment Variables

```bash
# Add to .env for Islamic context
ISLAMIC_CONTEXT_ENABLED=true
DEFAULT_MADHAB=Hanafi
PRAYER_TIME_API=your-prayer-api
ISLAMIC_CALENDAR_API=your-calendar-api
```

### Custom System Prompt

The server uses a specialized Islamic system prompt that ensures:
- Authentic Islamic knowledge
- Respectful and humble tone
- Citations from Quran and Hadith
- Acknowledgment of scholarly differences
- Recommendations for complex matters

## 🌟 Benefits for DeenMate

1. **Authentic Islamic Content**: Generated using proper Islamic context
2. **Personalized Guidance**: Tailored responses based on user questions
3. **Educational Value**: Comprehensive explanations with sources
4. **Daily Engagement**: Fresh content generated daily
5. **Community Support**: AI-powered answers to user questions
6. **Multilingual Potential**: Can generate content in multiple languages
7. **Scholarly Accuracy**: Emphasis on authentic sources and citations

## 🔒 Privacy & Security

- All processing happens on your local GPU server
- No Islamic questions or personal data sent to external APIs
- Complete control over content generation
- Compliant with Islamic values of privacy and discretion

This integration transforms your MCP server into a comprehensive Islamic AI assistant specifically designed for the DeenMate ecosystem! 🕌✨
