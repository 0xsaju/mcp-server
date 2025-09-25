#!/usr/bin/env python3
"""
DeenMate Project Code Generator

Specialized code generator that understands the DeenMate tech stack:
- Flutter/Dart for mobile app (deenmate-app)
- TypeScript/Node.js for backend (deenmate-backend)
- HTML/CSS/JS for web (deenmate-web)
- Islamic context and best practices
"""

from typing import Dict, Any, List
from datetime import datetime
import json

class DeenMateCodeGenerator:
    """Code generator specifically for DeenMate project"""
    
    def __init__(self):
        self.project_info = {
            "name": "DeenMate",
            "description": "Islamic utility app for Muslims",
            "repositories": {
                "deenmate-app": {
                    "tech": "Flutter/Dart",
                    "description": "Cross-platform mobile app",
                    "features": ["Prayer times", "Fasting tracker", "Zakat calculator", "Islamic content"]
                },
                "deenmate-backend": {
                    "tech": "TypeScript/Node.js",
                    "description": "Backend services and APIs",
                    "features": ["Authentication", "Content management", "Prayer time APIs", "User data"]
                },
                "deenmate-web": {
                    "tech": "HTML/CSS/JavaScript",
                    "description": "Marketing website",
                    "features": ["Landing pages", "Information", "API integrations"]
                }
            }
        }
    
    def get_deenmate_tools(self) -> List[Dict[str, Any]]:
        """Get DeenMate-specific code generation tools"""
        
        return [
            {
                "name": "generate_flutter_feature",
                "description": "Generate Flutter/Dart code for DeenMate app features",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "feature_name": {
                            "type": "string",
                            "description": "Name of the feature to generate"
                        },
                        "feature_type": {
                            "type": "string",
                            "description": "Type of feature",
                            "enum": ["prayer_times", "zakat_calculator", "fasting_tracker", "islamic_content", "qibla_finder", "hadith_reader", "quran_reader", "dua_collection", "custom"],
                            "default": "custom"
                        },
                        "components": {
                            "type": "array",
                            "description": "Components to generate",
                            "items": {
                                "type": "string",
                                "enum": ["widget", "screen", "service", "model", "provider", "all"]
                            },
                            "default": ["widget", "screen"]
                        },
                        "islamic_context": {
                            "type": "boolean",
                            "description": "Include Islamic context and best practices",
                            "default": True
                        }
                    },
                    "required": ["feature_name"]
                }
            },
            {
                "name": "generate_backend_api",
                "description": "Generate TypeScript backend API for DeenMate",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "api_name": {
                            "type": "string",
                            "description": "Name of the API endpoint"
                        },
                        "api_type": {
                            "type": "string",
                            "description": "Type of API",
                            "enum": ["prayer_times", "islamic_content", "user_management", "zakat_calculation", "authentication", "notifications", "custom"],
                            "default": "custom"
                        },
                        "http_methods": {
                            "type": "array",
                            "description": "HTTP methods to support",
                            "items": {
                                "type": "string",
                                "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"]
                            },
                            "default": ["GET", "POST"]
                        },
                        "include_auth": {
                            "type": "boolean",
                            "description": "Include authentication middleware",
                            "default": True
                        },
                        "include_validation": {
                            "type": "boolean",
                            "description": "Include request validation",
                            "default": True
                        }
                    },
                    "required": ["api_name"]
                }
            },
            {
                "name": "generate_web_component",
                "description": "Generate web component for DeenMate website",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "component_name": {
                            "type": "string",
                            "description": "Name of the web component"
                        },
                        "component_type": {
                            "type": "string",
                            "description": "Type of component",
                            "enum": ["landing_section", "prayer_widget", "feature_showcase", "testimonial", "pricing", "contact_form", "custom"],
                            "default": "custom"
                        },
                        "styling": {
                            "type": "string",
                            "description": "CSS framework/approach",
                            "enum": ["vanilla_css", "tailwind", "bootstrap", "css_modules"],
                            "default": "vanilla_css"
                        },
                        "interactive": {
                            "type": "boolean",
                            "description": "Include JavaScript interactivity",
                            "default": True
                        }
                    },
                    "required": ["component_name"]
                }
            },
            {
                "name": "generate_islamic_ui_components",
                "description": "Generate Islamic-themed UI components",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "platform": {
                            "type": "string",
                            "description": "Target platform",
                            "enum": ["flutter", "web", "both"],
                            "default": "flutter"
                        },
                        "component_category": {
                            "type": "string",
                            "description": "Category of Islamic component",
                            "enum": ["prayer_related", "calendar", "quran_reader", "hadith_display", "islamic_patterns", "arabic_typography", "custom"],
                            "default": "custom"
                        },
                        "design_style": {
                            "type": "string",
                            "description": "Design style",
                            "enum": ["modern", "traditional", "minimalist", "ornate"],
                            "default": "modern"
                        },
                        "include_animations": {
                            "type": "boolean",
                            "description": "Include animations and transitions",
                            "default": False
                        }
                    },
                    "required": ["component_category"]
                }
            },
            {
                "name": "generate_database_schema",
                "description": "Generate database schema for DeenMate features",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "schema_name": {
                            "type": "string",
                            "description": "Name of the database schema/table"
                        },
                        "data_type": {
                            "type": "string",
                            "description": "Type of data to store",
                            "enum": ["user_data", "prayer_times", "islamic_content", "zakat_records", "fasting_logs", "quran_bookmarks", "hadith_favorites", "custom"],
                            "default": "custom"
                        },
                        "database_type": {
                            "type": "string",
                            "description": "Database type",
                            "enum": ["postgresql", "mongodb", "sqlite", "mysql"],
                            "default": "postgresql"
                        },
                        "include_migrations": {
                            "type": "boolean",
                            "description": "Include database migration files",
                            "default": True
                        }
                    },
                    "required": ["schema_name"]
                }
            },
            {
                "name": "generate_test_suite",
                "description": "Generate comprehensive test suite for DeenMate features",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "test_target": {
                            "type": "string",
                            "description": "What to test",
                            "enum": ["flutter_widget", "backend_api", "web_component", "islamic_calculations", "prayer_times", "full_feature"],
                            "default": "full_feature"
                        },
                        "test_types": {
                            "type": "array",
                            "description": "Types of tests to generate",
                            "items": {
                                "type": "string",
                                "enum": ["unit", "integration", "widget", "e2e", "api"]
                            },
                            "default": ["unit", "integration"]
                        },
                        "feature_name": {
                            "type": "string",
                            "description": "Name of the feature being tested"
                        },
                        "include_mocks": {
                            "type": "boolean",
                            "description": "Include mock data for Islamic content",
                            "default": True
                        }
                    },
                    "required": ["feature_name"]
                }
            },
            {
                "name": "generate_documentation",
                "description": "Generate documentation for DeenMate features",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "doc_type": {
                            "type": "string",
                            "description": "Type of documentation",
                            "enum": ["api_docs", "feature_guide", "setup_instructions", "islamic_context", "user_manual", "developer_guide"],
                            "default": "feature_guide"
                        },
                        "feature_name": {
                            "type": "string",
                            "description": "Name of the feature to document"
                        },
                        "target_audience": {
                            "type": "string",
                            "description": "Target audience",
                            "enum": ["developers", "users", "islamic_scholars", "contributors"],
                            "default": "developers"
                        },
                        "include_examples": {
                            "type": "boolean",
                            "description": "Include code examples",
                            "default": True
                        }
                    },
                    "required": ["feature_name"]
                }
            }
        ]

# Template repository for DeenMate code patterns
DEENMATE_TEMPLATES = {
    "flutter": {
        "prayer_times_widget": """
import 'package:flutter/material.dart';
import '../services/prayer_time_service.dart';
import '../models/prayer_time.dart';

class PrayerTimesWidget extends StatefulWidget {
  final String location;
  
  const PrayerTimesWidget({
    Key? key,
    required this.location,
  }) : super(key: key);

  @override
  _PrayerTimesWidgetState createState() => _PrayerTimesWidgetState();
}

class _PrayerTimesWidgetState extends State<PrayerTimesWidget> {
  final PrayerTimeService _prayerService = PrayerTimeService();
  PrayerTime? _todaysPrayers;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadPrayerTimes();
  }

  Future<void> _loadPrayerTimes() async {
    try {
      final prayers = await _prayerService.getTodaysPrayerTimes(widget.location);
      setState(() {
        _todaysPrayers = prayers;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      // Handle error
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      margin: EdgeInsets.all(16),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.schedule, color: Colors.green),
                SizedBox(width: 8),
                Text(
                  'Prayer Times',
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
              ],
            ),
            SizedBox(height: 16),
            
            if (_isLoading)
              Center(child: CircularProgressIndicator())
            else if (_todaysPrayers != null)
              _buildPrayerTimesList()
            else
              Text('Unable to load prayer times'),
              
            SizedBox(height: 16),
            _buildQiblaDirection(),
          ],
        ),
      ),
    );
  }

  Widget _buildPrayerTimesList() {
    final prayers = [
      ('Fajr', _todaysPrayers!.fajr),
      ('Dhuhr', _todaysPrayers!.dhuhr),
      ('Asr', _todaysPrayers!.asr),
      ('Maghrib', _todaysPrayers!.maghrib),
      ('Isha', _todaysPrayers!.isha),
    ];

    return Column(
      children: prayers.map((prayer) {
        return Padding(
          padding: EdgeInsets.symmetric(vertical: 4),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                prayer.$1,
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
              ),
              Text(
                prayer.$2,
                style: TextStyle(fontSize: 16, color: Colors.green[700]),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }

  Widget _buildQiblaDirection() {
    return Container(
      padding: EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.green[50],
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        children: [
          Icon(Icons.explore, color: Colors.green[700]),
          SizedBox(width: 8),
          Text(
            'Qibla Direction: ${_todaysPrayers?.qiblaDirection ?? "Unknown"}',
            style: TextStyle(color: Colors.green[700]),
          ),
        ],
      ),
    );
  }
}
""",
        
        "zakat_calculator_screen": """
import 'package:flutter/material.dart';
import '../services/zakat_service.dart';
import '../models/zakat_calculation.dart';

class ZakatCalculatorScreen extends StatefulWidget {
  @override
  _ZakatCalculatorScreenState createState() => _ZakatCalculatorScreenState();
}

class _ZakatCalculatorScreenState extends State<ZakatCalculatorScreen> {
  final _formKey = GlobalKey<FormState>();
  final _amountController = TextEditingController();
  final ZakatService _zakatService = ZakatService();
  
  String _selectedWealthType = 'cash';
  String _selectedCurrency = 'USD';
  ZakatCalculation? _result;
  bool _isCalculating = false;

  final List<String> _wealthTypes = [
    'cash', 'gold', 'silver', 'business', 'agriculture'
  ];
  
  final List<String> _currencies = ['USD', 'BDT', 'EUR', 'GBP', 'SAR'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Zakat Calculator'),
        backgroundColor: Colors.green,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildHeader(),
              SizedBox(height: 24),
              _buildWealthTypeSelector(),
              SizedBox(height: 16),
              _buildAmountInput(),
              SizedBox(height: 16),
              _buildCurrencySelector(),
              SizedBox(height: 24),
              _buildCalculateButton(),
              SizedBox(height: 24),
              if (_result != null) _buildResults(),
              SizedBox(height: 16),
              _buildIslamicGuidance(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [Colors.green[100]!, Colors.green[50]!],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Zakat Calculator',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: Colors.green[800],
            ),
          ),
          SizedBox(height: 8),
          Text(
            'Calculate your Zakat obligation according to Islamic jurisprudence',
            style: TextStyle(
              fontSize: 14,
              color: Colors.green[700],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildWealthTypeSelector() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Wealth Type', style: TextStyle(fontWeight: FontWeight.w600)),
        SizedBox(height: 8),
        DropdownButtonFormField<String>(
          value: _selectedWealthType,
          decoration: InputDecoration(
            border: OutlineInputBorder(),
            contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
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
      ],
    );
  }

  Widget _buildAmountInput() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Amount', style: TextStyle(fontWeight: FontWeight.w600)),
        SizedBox(height: 8),
        TextFormField(
          controller: _amountController,
          decoration: InputDecoration(
            border: OutlineInputBorder(),
            hintText: 'Enter amount',
            prefixIcon: Icon(Icons.attach_money),
          ),
          keyboardType: TextInputType.number,
          validator: (value) {
            if (value?.isEmpty ?? true) return 'Please enter an amount';
            if (double.tryParse(value!) == null) return 'Please enter a valid number';
            return null;
          },
        ),
      ],
    );
  }

  Widget _buildCurrencySelector() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Currency', style: TextStyle(fontWeight: FontWeight.w600)),
        SizedBox(height: 8),
        DropdownButtonFormField<String>(
          value: _selectedCurrency,
          decoration: InputDecoration(
            border: OutlineInputBorder(),
            contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
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
      ],
    );
  }

  Widget _buildCalculateButton() {
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton(
        onPressed: _isCalculating ? null : _calculateZakat,
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.green,
          padding: EdgeInsets.symmetric(vertical: 16),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
        child: _isCalculating
            ? CircularProgressIndicator(color: Colors.white)
            : Text(
                'Calculate Zakat',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
              ),
      ),
    );
  }

  Widget _buildResults() {
    return Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: _result!.isZakatDue ? Colors.blue[50] : Colors.orange[50],
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: _result!.isZakatDue ? Colors.blue[200]! : Colors.orange[200]!,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                _result!.isZakatDue ? Icons.check_circle : Icons.info,
                color: _result!.isZakatDue ? Colors.blue[700] : Colors.orange[700],
              ),
              SizedBox(width: 8),
              Text(
                _result!.isZakatDue ? 'Zakat is Due' : 'No Zakat Due',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: _result!.isZakatDue ? Colors.blue[700] : Colors.orange[700],
                ),
              ),
            ],
          ),
          SizedBox(height: 12),
          if (_result!.isZakatDue) ...[
            Text('Amount Due: ${_result!.zakatAmount.toStringAsFixed(2)} ${_selectedCurrency}'),
            SizedBox(height: 8),
          ],
          Text('Nisab Threshold: ${_result!.nisabThreshold.toStringAsFixed(2)} ${_selectedCurrency}'),
          SizedBox(height: 8),
          Text(_result!.explanation),
        ],
      ),
    );
  }

  Widget _buildIslamicGuidance() {
    return Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.green[50],
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.mosque, color: Colors.green[700]),
              SizedBox(width: 8),
              Text(
                'Islamic Guidance',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: Colors.green[700],
                ),
              ),
            ],
          ),
          SizedBox(height: 8),
          Text(
            'Zakat is one of the Five Pillars of Islam and a religious obligation for all eligible Muslims. '
            'It purifies wealth and helps those in need. Consult with Islamic scholars for complex situations.',
            style: TextStyle(color: Colors.green[600]),
          ),
        ],
      ),
    );
  }

  Future<void> _calculateZakat() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isCalculating = true;
    });

    try {
      final amount = double.parse(_amountController.text);
      final result = await _zakatService.calculateZakat(
        wealthType: _selectedWealthType,
        amount: amount,
        currency: _selectedCurrency,
      );

      setState(() {
        _result = result;
        _isCalculating = false;
      });
    } catch (e) {
      setState(() {
        _isCalculating = false;
      });
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error calculating Zakat: ${e.toString()}')),
      );
    }
  }

  @override
  void dispose() {
    _amountController.dispose();
    super.dispose();
  }
}
"""
    },
    
    "backend": {
        "prayer_times_api": """
import { Router } from 'express';
import { PrayerTimeService } from '../services/prayerTimeService';
import { validateRequest } from '../middleware/validation';
import { authenticateUser } from '../middleware/auth';
import { ApiResponse } from '../types/api';
import { PrayerTimesRequest, PrayerTimesResponse } from '../types/prayer';

const router = Router();
const prayerTimeService = new PrayerTimeService();

// Get prayer times for a location
router.get('/times', 
  authenticateUser, 
  validateRequest({
    query: {
      type: 'object',
      properties: {
        latitude: { type: 'number', minimum: -90, maximum: 90 },
        longitude: { type: 'number', minimum: -180, maximum: 180 },
        date: { type: 'string', pattern: '^\\\\d{4}-\\\\d{2}-\\\\d{2}$' },
        method: { type: 'number', minimum: 1, maximum: 12 },
        madhab: { type: 'number', enum: [0, 1] }
      },
      required: ['latitude', 'longitude']
    }
  }),
  async (req, res) => {
    try {
      const { latitude, longitude, date, method = 2, madhab = 1 } = req.query as any;
      
      const prayerTimes = await prayerTimeService.getPrayerTimes({
        latitude: parseFloat(latitude),
        longitude: parseFloat(longitude),
        date: date || new Date().toISOString().split('T')[0],
        calculationMethod: parseInt(method),
        madhab: parseInt(madhab)
      });

      const response: ApiResponse<PrayerTimesResponse> = {
        success: true,
        data: {
          date: prayerTimes.date,
          location: {
            latitude: parseFloat(latitude),
            longitude: parseFloat(longitude)
          },
          times: {
            fajr: prayerTimes.fajr,
            sunrise: prayerTimes.sunrise,
            dhuhr: prayerTimes.dhuhr,
            asr: prayerTimes.asr,
            maghrib: prayerTimes.maghrib,
            isha: prayerTimes.isha
          },
          qibla: {
            direction: prayerTimes.qiblaDirection,
            distance: prayerTimes.qiblaDistance
          },
          calculationMethod: method,
          madhab: madhab
        },
        message: 'Prayer times retrieved successfully'
      };

      res.json(response);
    } catch (error) {
      console.error('Prayer times API error:', error);
      
      const errorResponse: ApiResponse<null> = {
        success: false,
        data: null,
        message: 'Failed to retrieve prayer times',
        error: error instanceof Error ? error.message : 'Unknown error'
      };
      
      res.status(500).json(errorResponse);
    }
  }
);

// Get next prayer time
router.get('/next', 
  authenticateUser,
  validateRequest({
    query: {
      type: 'object',
      properties: {
        latitude: { type: 'number', minimum: -90, maximum: 90 },
        longitude: { type: 'number', minimum: -180, maximum: 180 },
        method: { type: 'number', minimum: 1, maximum: 12 },
        madhab: { type: 'number', enum: [0, 1] }
      },
      required: ['latitude', 'longitude']
    }
  }),
  async (req, res) => {
    try {
      const { latitude, longitude, method = 2, madhab = 1 } = req.query as any;
      
      const nextPrayer = await prayerTimeService.getNextPrayer({
        latitude: parseFloat(latitude),
        longitude: parseFloat(longitude),
        calculationMethod: parseInt(method),
        madhab: parseInt(madhab)
      });

      const response: ApiResponse<any> = {
        success: true,
        data: {
          name: nextPrayer.name,
          time: nextPrayer.time,
          timeRemaining: nextPrayer.timeRemaining,
          isToday: nextPrayer.isToday
        },
        message: 'Next prayer time retrieved successfully'
      };

      res.json(response);
    } catch (error) {
      console.error('Next prayer API error:', error);
      
      const errorResponse: ApiResponse<null> = {
        success: false,
        data: null,
        message: 'Failed to retrieve next prayer time',
        error: error instanceof Error ? error.message : 'Unknown error'
      };
      
      res.status(500).json(errorResponse);
    }
  }
);

// Get monthly prayer times
router.get('/monthly',
  authenticateUser,
  validateRequest({
    query: {
      type: 'object',
      properties: {
        latitude: { type: 'number', minimum: -90, maximum: 90 },
        longitude: { type: 'number', minimum: -180, maximum: 180 },
        year: { type: 'number', minimum: 1900, maximum: 2100 },
        month: { type: 'number', minimum: 1, maximum: 12 },
        method: { type: 'number', minimum: 1, maximum: 12 },
        madhab: { type: 'number', enum: [0, 1] }
      },
      required: ['latitude', 'longitude', 'year', 'month']
    }
  }),
  async (req, res) => {
    try {
      const { latitude, longitude, year, month, method = 2, madhab = 1 } = req.query as any;
      
      const monthlyTimes = await prayerTimeService.getMonthlyPrayerTimes({
        latitude: parseFloat(latitude),
        longitude: parseFloat(longitude),
        year: parseInt(year),
        month: parseInt(month),
        calculationMethod: parseInt(method),
        madhab: parseInt(madhab)
      });

      const response: ApiResponse<any> = {
        success: true,
        data: {
          year: parseInt(year),
          month: parseInt(month),
          location: {
            latitude: parseFloat(latitude),
            longitude: parseFloat(longitude)
          },
          times: monthlyTimes,
          calculationMethod: method,
          madhab: madhab
        },
        message: 'Monthly prayer times retrieved successfully'
      };

      res.json(response);
    } catch (error) {
      console.error('Monthly prayer times API error:', error);
      
      const errorResponse: ApiResponse<null> = {
        success: false,
        data: null,
        message: 'Failed to retrieve monthly prayer times',
        error: error instanceof Error ? error.message : 'Unknown error'
      };
      
      res.status(500).json(errorResponse);
    }
  }
);

export default router;
""",

        "islamic_content_api": """
import { Router } from 'express';
import { IslamicContentService } from '../services/islamicContentService';
import { IslamicAIService } from '../services/islamicAIService';
import { validateRequest } from '../middleware/validation';
import { authenticateUser } from '../middleware/auth';
import { ApiResponse } from '../types/api';

const router = Router();
const contentService = new IslamicContentService();
const aiService = new IslamicAIService();

// Get daily Islamic content
router.get('/daily', 
  authenticateUser,
  async (req, res) => {
    try {
      // Get AI-generated daily content
      const dailyContent = await aiService.getDailyContent();
      
      // Combine with curated content
      const curatedContent = await contentService.getTodaysContent();
      
      const response: ApiResponse<any> = {
        success: true,
        data: {
          date: new Date().toISOString().split('T')[0],
          aiGenerated: dailyContent,
          curated: curatedContent,
          features: {
            verseOfDay: dailyContent.verse_of_day,
            hadithOfDay: dailyContent.hadith_of_day,
            duaOfDay: dailyContent.dua_of_day,
            dailyTip: dailyContent.daily_tip
          }
        },
        message: 'Daily Islamic content retrieved successfully'
      };

      res.json(response);
    } catch (error) {
      console.error('Daily content API error:', error);
      
      const errorResponse: ApiResponse<null> = {
        success: false,
        data: null,
        message: 'Failed to retrieve daily content',
        error: error instanceof Error ? error.message : 'Unknown error'
      };
      
      res.status(500).json(errorResponse);
    }
  }
);

// Generate custom Islamic content
router.post('/generate',
  authenticateUser,
  validateRequest({
    body: {
      type: 'object',
      properties: {
        contentType: {
          type: 'string',
          enum: ['daily_reminder', 'educational_article', 'dua', 'dhikr', 'reflection', 'tip']
        },
        topic: { type: 'string', minLength: 1, maxLength: 200 },
        targetAudience: {
          type: 'string',
          enum: ['general', 'youth', 'adults', 'families', 'converts']
        },
        length: {
          type: 'string',
          enum: ['short', 'medium', 'long']
        }
      },
      required: ['contentType']
    }
  }),
  async (req, res) => {
    try {
      const { contentType, topic, targetAudience = 'general', length = 'medium' } = req.body;
      
      const generatedContent = await aiService.generateContent({
        contentType,
        topic,
        targetAudience,
        length
      });

      // Store generated content for future reference
      await contentService.saveGeneratedContent({
        userId: req.user?.id,
        contentType,
        topic,
        content: generatedContent,
        targetAudience,
        length
      });

      const response: ApiResponse<any> = {
        success: true,
        data: {
          content: generatedContent,
          metadata: {
            contentType,
            topic,
            targetAudience,
            length,
            generatedAt: new Date().toISOString()
          }
        },
        message: 'Islamic content generated successfully'
      };

      res.json(response);
    } catch (error) {
      console.error('Content generation API error:', error);
      
      const errorResponse: ApiResponse<null> = {
        success: false,
        data: null,
        message: 'Failed to generate Islamic content',
        error: error instanceof Error ? error.message : 'Unknown error'
      };
      
      res.status(500).json(errorResponse);
    }
  }
);

// Get Islamic guidance
router.post('/guidance',
  authenticateUser,
  validateRequest({
    body: {
      type: 'object',
      properties: {
        question: { type: 'string', minLength: 5, maxLength: 500 },
        context: { type: 'string', maxLength: 1000 },
        madhab: {
          type: 'string',
          enum: ['Hanafi', 'Shafi', 'Maliki', 'Hanbali', 'General']
        },
        urgency: {
          type: 'string',
          enum: ['low', 'medium', 'high']
        }
      },
      required: ['question']
    }
  }),
  async (req, res) => {
    try {
      const { question, context, madhab = 'General', urgency = 'medium' } = req.body;
      
      const guidance = await aiService.getIslamicGuidance({
        question,
        context,
        madhab
      });

      // Log the question for analytics (anonymized)
      await contentService.logGuidanceRequest({
        userId: req.user?.id,
        questionHash: contentService.hashQuestion(question),
        madhab,
        urgency,
        timestamp: new Date()
      });

      const response: ApiResponse<any> = {
        success: true,
        data: {
          guidance,
          metadata: {
            madhab,
            disclaimer: 'This guidance is AI-generated. For complex matters, please consult qualified Islamic scholars.',
            sources: 'Based on Quran, authentic Hadith, and established Islamic scholarship',
            generatedAt: new Date().toISOString()
          }
        },
        message: 'Islamic guidance provided successfully'
      };

      res.json(response);
    } catch (error) {
      console.error('Guidance API error:', error);
      
      const errorResponse: ApiResponse<null> = {
        success: false,
        data: null,
        message: 'Failed to provide Islamic guidance',
        error: error instanceof Error ? error.message : 'Unknown error'
      };
      
      res.status(500).json(errorResponse);
    }
  }
);

export default router;
"""
    },
    
    "web": {
        "prayer_widget": """
<div class="prayer-times-widget" id="prayerWidget">
  <div class="widget-header">
    <h3>Prayer Times</h3>
    <span class="location" id="locationDisplay">Loading...</span>
  </div>
  
  <div class="prayer-times-list" id="prayerTimesList">
    <!-- Prayer times will be inserted here -->
  </div>
  
  <div class="next-prayer" id="nextPrayer">
    <!-- Next prayer info will be inserted here -->
  </div>
  
  <div class="qibla-direction" id="qiblaDirection">
    <!-- Qibla direction will be inserted here -->
  </div>
</div>

<style>
.prayer-times-widget {
  background: linear-gradient(135deg, #2d5016 0%, #3d6b1f 100%);
  color: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  max-width: 350px;
  margin: 20px auto;
  font-family: 'Arial', sans-serif;
}

.widget-header {
  text-align: center;
  margin-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding-bottom: 15px;
}

.widget-header h3 {
  margin: 0 0 5px 0;
  font-size: 24px;
  font-weight: 600;
}

.location {
  font-size: 14px;
  opacity: 0.9;
}

.prayer-times-list {
  margin-bottom: 20px;
}

.prayer-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.prayer-item:last-child {
  border-bottom: none;
}

.prayer-name {
  font-weight: 500;
  font-size: 16px;
}

.prayer-time {
  font-size: 16px;
  font-weight: 600;
  color: #90EE90;
}

.prayer-item.current {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 12px 8px;
  margin: 4px 0;
}

.next-prayer {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 15px;
  text-align: center;
  margin-bottom: 15px;
}

.next-prayer-label {
  font-size: 12px;
  opacity: 0.8;
  margin-bottom: 5px;
}

.next-prayer-name {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 5px;
}

.next-prayer-time {
  font-size: 16px;
  color: #90EE90;
  margin-bottom: 5px;
}

.time-remaining {
  font-size: 14px;
  opacity: 0.9;
}

.qibla-direction {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 12px;
}

.qibla-icon {
  margin-right: 8px;
  font-size: 18px;
}

.loading {
  text-align: center;
  opacity: 0.7;
  padding: 20px;
}

.error {
  text-align: center;
  color: #ffcccc;
  padding: 20px;
  background: rgba(255, 0, 0, 0.1);
  border-radius: 8px;
  margin: 10px 0;
}

@media (max-width: 480px) {
  .prayer-times-widget {
    margin: 10px;
    padding: 15px;
  }
  
  .widget-header h3 {
    font-size: 20px;
  }
  
  .prayer-name, .prayer-time {
    font-size: 14px;
  }
}
</style>

<script>
class PrayerTimesWidget {
  constructor() {
    this.apiUrl = 'https://api.deenmate.app';
    this.widget = document.getElementById('prayerWidget');
    this.updateInterval = null;
    this.init();
  }

  async init() {
    try {
      // Get user location
      const location = await this.getUserLocation();
      
      // Load prayer times
      await this.loadPrayerTimes(location);
      
      // Set up auto-refresh
      this.setupAutoRefresh();
      
    } catch (error) {
      this.showError('Failed to load prayer times');
      console.error('Prayer widget error:', error);
    }
  }

  async getUserLocation() {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('Geolocation not supported'));
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          });
        },
        (error) => {
          // Fallback to default location (Mecca)
          resolve({
            latitude: 21.4225,
            longitude: 39.8262
          });
        },
        { timeout: 10000 }
      );
    });
  }

  async loadPrayerTimes(location) {
    try {
      // Show loading state
      this.showLoading();
      
      // Fetch prayer times
      const response = await fetch(
        `${this.apiUrl}/api/prayer/times?latitude=${location.latitude}&longitude=${location.longitude}`
      );
      
      if (!response.ok) throw new Error('Failed to fetch prayer times');
      
      const data = await response.json();
      
      if (data.success) {
        this.renderPrayerTimes(data.data);
        await this.loadNextPrayer(location);
      } else {
        throw new Error(data.message || 'Failed to load prayer times');
      }
      
    } catch (error) {
      this.showError(error.message);
    }
  }

  async loadNextPrayer(location) {
    try {
      const response = await fetch(
        `${this.apiUrl}/api/prayer/next?latitude=${location.latitude}&longitude=${location.longitude}`
      );
      
      if (!response.ok) return;
      
      const data = await response.json();
      
      if (data.success) {
        this.renderNextPrayer(data.data);
      }
      
    } catch (error) {
      console.warn('Failed to load next prayer:', error);
    }
  }

  renderPrayerTimes(data) {
    const listElement = document.getElementById('prayerTimesList');
    const locationElement = document.getElementById('locationDisplay');
    
    // Update location display
    locationElement.textContent = `${data.location.latitude.toFixed(2)}, ${data.location.longitude.toFixed(2)}`;
    
    // Render prayer times
    const prayers = [
      { name: 'Fajr', time: data.times.fajr },
      { name: 'Sunrise', time: data.times.sunrise },
      { name: 'Dhuhr', time: data.times.dhuhr },
      { name: 'Asr', time: data.times.asr },
      { name: 'Maghrib', time: data.times.maghrib },
      { name: 'Isha', time: data.times.isha }
    ];
    
    listElement.innerHTML = prayers.map(prayer => `
      <div class="prayer-item">
        <span class="prayer-name">${prayer.name}</span>
        <span class="prayer-time">${this.formatTime(prayer.time)}</span>
      </div>
    `).join('');
    
    // Render Qibla direction
    const qiblaElement = document.getElementById('qiblaDirection');
    qiblaElement.innerHTML = `
      <span class="qibla-icon">🧭</span>
      <span>Qibla: ${data.qibla.direction}°</span>
    `;
  }

  renderNextPrayer(data) {
    const nextPrayerElement = document.getElementById('nextPrayer');
    
    nextPrayerElement.innerHTML = `
      <div class="next-prayer-label">Next Prayer</div>
      <div class="next-prayer-name">${data.name}</div>
      <div class="next-prayer-time">${this.formatTime(data.time)}</div>
      <div class="time-remaining">${data.timeRemaining}</div>
    `;
  }

  formatTime(timeString) {
    try {
      const time = new Date(`2000-01-01T${timeString}`);
      return time.toLocaleTimeString([], { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
      });
    } catch {
      return timeString;
    }
  }

  showLoading() {
    const listElement = document.getElementById('prayerTimesList');
    listElement.innerHTML = '<div class="loading">Loading prayer times...</div>';
  }

  showError(message) {
    const listElement = document.getElementById('prayerTimesList');
    listElement.innerHTML = `<div class="error">${message}</div>`;
  }

  setupAutoRefresh() {
    // Refresh every 5 minutes
    this.updateInterval = setInterval(() => {
      this.init();
    }, 5 * 60 * 1000);
  }

  destroy() {
    if (this.updateInterval) {
      clearInterval(this.updateInterval);
    }
  }
}

// Initialize the widget when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new PrayerTimesWidget();
});
</script>
"""
    }
}
