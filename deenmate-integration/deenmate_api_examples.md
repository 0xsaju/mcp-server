# DeenMate API Integration Examples

This document provides practical examples for integrating the Islamic MCP server with DeenMate's three repositories.

## 🔧 Backend Integration (deenmate-backend - TypeScript)

### 1. MCP Client Service

```typescript
// services/mcpClient.ts
import axios from 'axios';

export interface MCPRequest {
  jsonrpc: string;
  id: number;
  method: string;
  params: any;
}

export interface MCPResponse {
  jsonrpc: string;
  id: number;
  result?: any;
  error?: {
    code: number;
    message: string;
  };
}

export class MCPClient {
  private baseUrl: string;
  private requestId: number = 1;

  constructor(baseUrl: string = process.env.MCP_SERVER_URL || 'http://localhost:8080') {
    this.baseUrl = baseUrl;
  }

  async callTool(toolName: string, arguments: any): Promise<any> {
    const request: MCPRequest = {
      jsonrpc: '2.0',
      id: this.requestId++,
      method: 'tools/call',
      params: {
        name: toolName,
        arguments: arguments
      }
    };

    try {
      const response = await axios.post<MCPResponse>(`${this.baseUrl}/mcp`, request);
      
      if (response.data.error) {
        throw new Error(`MCP Error: ${response.data.error.message}`);
      }
      
      return response.data.result;
    } catch (error) {
      console.error('MCP Tool Call Error:', error);
      throw error;
    }
  }

  async getResource(uri: string): Promise<any> {
    const request: MCPRequest = {
      jsonrpc: '2.0',
      id: this.requestId++,
      method: 'resources/read',
      params: { uri }
    };

    try {
      const response = await axios.post<MCPResponse>(`${this.baseUrl}/mcp`, request);
      return response.data.result;
    } catch (error) {
      console.error('MCP Resource Error:', error);
      throw error;
    }
  }
}
```

### 2. Islamic Services

```typescript
// services/islamicService.ts
import { MCPClient } from './mcpClient';

export class IslamicService {
  private mcpClient: MCPClient;

  constructor() {
    this.mcpClient = new MCPClient();
  }

  // Get Islamic guidance for user questions
  async getIslamicGuidance(question: string, context?: string, madhab?: string): Promise<string> {
    const result = await this.mcpClient.callTool('islamic_guidance', {
      question,
      context,
      madhab: madhab || 'General'
    });
    
    return result.content[0].text;
  }

  // Calculate Zakat for user
  async calculateZakat(wealthType: string, amount: number, currency: string = 'USD'): Promise<any> {
    return await this.mcpClient.callTool('zakat_calculator', {
      wealth_type: wealthType,
      amount,
      currency
    });
  }

  // Generate daily Islamic content
  async getDailyContent(): Promise<any> {
    const result = await this.mcpClient.getResource('islamic://daily/content');
    return result.contents[0].json;
  }

  // Get prayer guidance
  async getPrayerGuidance(question: string, prayerType?: string, situation?: string): Promise<string> {
    const result = await this.mcpClient.callTool('prayer_guidance', {
      prayer_question: question,
      prayer_type: prayerType,
      situation
    });
    
    return result.content[0].text;
  }

  // Generate content for the app
  async generateContent(contentType: string, topic?: string, audience?: string): Promise<string> {
    const result = await this.mcpClient.callTool('islamic_content_generator', {
      content_type: contentType,
      topic,
      target_audience: audience || 'general'
    });
    
    return result.content[0].text;
  }

  // Get Halal/Haram guidance
  async getHalalHaramGuidance(item: string, context?: string): Promise<string> {
    const result = await this.mcpClient.callTool('halal_haram_guidance', {
      item_or_action: item,
      context
    });
    
    return result.content[0].text;
  }
}
```

### 3. API Endpoints

```typescript
// routes/islamic.ts
import { Router } from 'express';
import { IslamicService } from '../services/islamicService';

const router = Router();
const islamicService = new IslamicService();

// Get Islamic guidance
router.post('/guidance', async (req, res) => {
  try {
    const { question, context, madhab } = req.body;
    const guidance = await islamicService.getIslamicGuidance(question, context, madhab);
    
    res.json({
      success: true,
      data: { guidance }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Calculate Zakat
router.post('/zakat/calculate', async (req, res) => {
  try {
    const { wealthType, amount, currency } = req.body;
    const calculation = await islamicService.calculateZakat(wealthType, amount, currency);
    
    res.json({
      success: true,
      data: calculation
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Get daily content
router.get('/daily-content', async (req, res) => {
  try {
    const content = await islamicService.getDailyContent();
    
    res.json({
      success: true,
      data: content
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Generate educational content
router.post('/content/generate', async (req, res) => {
  try {
    const { contentType, topic, audience } = req.body;
    const content = await islamicService.generateContent(contentType, topic, audience);
    
    res.json({
      success: true,
      data: { content }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

export default router;
```

## 📱 Flutter App Integration (deenmate-app - Dart)

### 1. Islamic AI Service

```dart
// lib/services/islamic_ai_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class IslamicAIService {
  static const String baseUrl = 'https://your-backend.com/api/islamic';
  
  // Get Islamic guidance
  static Future<String> getIslamicGuidance({
    required String question,
    String? context,
    String? madhab,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/guidance'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'question': question,
        'context': context,
        'madhab': madhab ?? 'General',
      }),
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['data']['guidance'];
    } else {
      throw Exception('Failed to get Islamic guidance');
    }
  }
  
  // Calculate Zakat
  static Future<Map<String, dynamic>> calculateZakat({
    required String wealthType,
    required double amount,
    String currency = 'USD',
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/zakat/calculate'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'wealthType': wealthType,
        'amount': amount,
        'currency': currency,
      }),
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['data'];
    } else {
      throw Exception('Failed to calculate Zakat');
    }
  }
  
  // Get daily content
  static Future<Map<String, dynamic>> getDailyContent() async {
    final response = await http.get(
      Uri.parse('$baseUrl/daily-content'),
      headers: {'Content-Type': 'application/json'},
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['data'];
    } else {
      throw Exception('Failed to get daily content');
    }
  }
  
  // Generate content
  static Future<String> generateContent({
    required String contentType,
    String? topic,
    String? audience,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/content/generate'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'contentType': contentType,
        'topic': topic,
        'audience': audience ?? 'general',
      }),
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['data']['content'];
    } else {
      throw Exception('Failed to generate content');
    }
  }
}
```

### 2. UI Widgets for Islamic Features

```dart
// lib/widgets/islamic_guidance_widget.dart
import 'package:flutter/material.dart';
import '../services/islamic_ai_service.dart';

class IslamicGuidanceWidget extends StatefulWidget {
  @override
  _IslamicGuidanceWidgetState createState() => _IslamicGuidanceWidgetState();
}

class _IslamicGuidanceWidgetState extends State<IslamicGuidanceWidget> {
  final TextEditingController _questionController = TextEditingController();
  String? _guidance;
  bool _isLoading = false;

  Future<void> _getGuidance() async {
    if (_questionController.text.isEmpty) return;
    
    setState(() {
      _isLoading = true;
    });
    
    try {
      final guidance = await IslamicAIService.getIslamicGuidance(
        question: _questionController.text,
      );
      
      setState(() {
        _guidance = guidance;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: ${e.toString()}')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Ask Islamic Question',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            SizedBox(height: 16),
            TextField(
              controller: _questionController,
              decoration: InputDecoration(
                hintText: 'What is your Islamic question?',
                border: OutlineInputBorder(),
              ),
              maxLines: 3,
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: _isLoading ? null : _getGuidance,
              child: _isLoading 
                ? CircularProgressIndicator()
                : Text('Get Guidance'),
            ),
            if (_guidance != null) ...[
              SizedBox(height: 16),
              Container(
                padding: EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.green.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  _guidance!,
                  style: TextStyle(fontSize: 14),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
```

### 3. Zakat Calculator Widget

```dart
// lib/widgets/zakat_calculator_widget.dart
import 'package:flutter/material.dart';
import '../services/islamic_ai_service.dart';

class ZakatCalculatorWidget extends StatefulWidget {
  @override
  _ZakatCalculatorWidgetState createState() => _ZakatCalculatorWidgetState();
}

class _ZakatCalculatorWidgetState extends State<ZakatCalculatorWidget> {
  final TextEditingController _amountController = TextEditingController();
  String _selectedWealthType = 'cash';
  String _selectedCurrency = 'USD';
  Map<String, dynamic>? _zakatResult;
  bool _isLoading = false;

  final List<String> _wealthTypes = ['cash', 'gold', 'silver', 'business'];
  final List<String> _currencies = ['USD', 'BDT', 'EUR', 'GBP'];

  Future<void> _calculateZakat() async {
    final amount = double.tryParse(_amountController.text);
    if (amount == null || amount <= 0) return;
    
    setState(() {
      _isLoading = true;
    });
    
    try {
      final result = await IslamicAIService.calculateZakat(
        wealthType: _selectedWealthType,
        amount: amount,
        currency: _selectedCurrency,
      );
      
      setState(() {
        _zakatResult = result;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error calculating Zakat: ${e.toString()}')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Zakat Calculator',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            SizedBox(height: 16),
            
            // Wealth Type Dropdown
            DropdownButtonFormField<String>(
              value: _selectedWealthType,
              decoration: InputDecoration(
                labelText: 'Wealth Type',
                border: OutlineInputBorder(),
              ),
              items: _wealthTypes.map((type) {
                return DropdownMenuItem(
                  value: type,
                  child: Text(type.toUpperCase()),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  _selectedWealthType = value!;
                });
              },
            ),
            
            SizedBox(height: 16),
            
            // Amount Input
            TextField(
              controller: _amountController,
              decoration: InputDecoration(
                labelText: 'Amount',
                border: OutlineInputBorder(),
              ),
              keyboardType: TextInputType.number,
            ),
            
            SizedBox(height: 16),
            
            // Currency Dropdown
            DropdownButtonFormField<String>(
              value: _selectedCurrency,
              decoration: InputDecoration(
                labelText: 'Currency',
                border: OutlineInputBorder(),
              ),
              items: _currencies.map((currency) {
                return DropdownMenuItem(
                  value: currency,
                  child: Text(currency),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  _selectedCurrency = value!;
                });
              },
            ),
            
            SizedBox(height: 16),
            
            ElevatedButton(
              onPressed: _isLoading ? null : _calculateZakat,
              child: _isLoading 
                ? CircularProgressIndicator()
                : Text('Calculate Zakat'),
            ),
            
            if (_zakatResult != null) ...[
              SizedBox(height: 16),
              Container(
                padding: EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.blue.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  _zakatResult!['content'][0]['text'],
                  style: TextStyle(fontSize: 14),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
```

## 🌐 Web Integration (deenmate-web - CSS/HTML)

### 1. JavaScript Islamic AI Client

```javascript
// assets/js/islamicAI.js
class IslamicAIClient {
  constructor(baseUrl = 'https://your-backend.com/api/islamic') {
    this.baseUrl = baseUrl;
  }

  async getIslamicGuidance(question, context = null, madhab = 'General') {
    try {
      const response = await fetch(`${this.baseUrl}/guidance`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question,
          context,
          madhab
        })
      });

      const data = await response.json();
      
      if (data.success) {
        return data.data.guidance;
      } else {
        throw new Error(data.error);
      }
    } catch (error) {
      console.error('Error getting Islamic guidance:', error);
      throw error;
    }
  }

  async calculateZakat(wealthType, amount, currency = 'USD') {
    try {
      const response = await fetch(`${this.baseUrl}/zakat/calculate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          wealthType,
          amount,
          currency
        })
      });

      const data = await response.json();
      return data.success ? data.data : null;
    } catch (error) {
      console.error('Error calculating Zakat:', error);
      throw error;
    }
  }

  async getDailyContent() {
    try {
      const response = await fetch(`${this.baseUrl}/daily-content`);
      const data = await response.json();
      return data.success ? data.data : null;
    } catch (error) {
      console.error('Error getting daily content:', error);
      throw error;
    }
  }
}

// Initialize client
const islamicAI = new IslamicAIClient();
```

### 2. Interactive Zakat Calculator (HTML)

```html
<!-- zakat-calculator.html -->
<div class="zakat-calculator">
  <h2>Zakat Calculator</h2>
  
  <form id="zakatForm">
    <div class="form-group">
      <label for="wealthType">Wealth Type:</label>
      <select id="wealthType" required>
        <option value="cash">Cash</option>
        <option value="gold">Gold</option>
        <option value="silver">Silver</option>
        <option value="business">Business</option>
      </select>
    </div>
    
    <div class="form-group">
      <label for="amount">Amount:</label>
      <input type="number" id="amount" required min="0" step="0.01">
    </div>
    
    <div class="form-group">
      <label for="currency">Currency:</label>
      <select id="currency">
        <option value="USD">USD</option>
        <option value="BDT">BDT</option>
        <option value="EUR">EUR</option>
        <option value="GBP">GBP</option>
      </select>
    </div>
    
    <button type="submit">Calculate Zakat</button>
  </form>
  
  <div id="zakatResult" class="result hidden">
    <!-- Zakat calculation results will appear here -->
  </div>
</div>

<script>
document.getElementById('zakatForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const wealthType = document.getElementById('wealthType').value;
  const amount = parseFloat(document.getElementById('amount').value);
  const currency = document.getElementById('currency').value;
  
  try {
    const result = await islamicAI.calculateZakat(wealthType, amount, currency);
    
    const resultDiv = document.getElementById('zakatResult');
    resultDiv.innerHTML = result.content[0].text.replace(/\n/g, '<br>');
    resultDiv.classList.remove('hidden');
  } catch (error) {
    alert('Error calculating Zakat: ' + error.message);
  }
});
</script>
```

## 🔧 Environment Configuration

### Backend (.env)
```bash
# DeenMate Backend Environment
MCP_SERVER_URL=http://your-gpu-server:8080
ISLAMIC_AI_ENABLED=true
DEFAULT_MADHAB=Hanafi
ZAKAT_NISAB_API=your-nisab-api
PRAYER_TIME_API=your-prayer-api
```

### Flutter (config.dart)
```dart
class Config {
  static const String backendUrl = 'https://your-backend.com';
  static const String mcpServerUrl = 'http://your-gpu-server:8080';
  static const bool islamicAIEnabled = true;
  static const String defaultMadhab = 'Hanafi';
}
```

This integration provides DeenMate with powerful AI-driven Islamic features while maintaining authentic religious guidance and user privacy! 🕌✨
