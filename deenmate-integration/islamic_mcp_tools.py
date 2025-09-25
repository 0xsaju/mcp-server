#!/usr/bin/env python3
"""
Islamic-specific MCP tools for DeenMate integration

This module extends the base MCP server with Islamic content generation,
religious guidance, and educational tools specifically for DeenMate.
"""

from typing import Dict, Any, List
from datetime import datetime
import json

# Islamic context for the LLM
ISLAMIC_SYSTEM_PROMPT = """You are 'IslamicAI', a knowledgeable and respectful Islamic assistant for DeenMate. 
You specialize in:
- Quran and Hadith knowledge
- Islamic jurisprudence (Fiqh)
- Prayer times and religious obligations
- Islamic history and culture
- Halal/Haram guidance
- Spiritual development

Always respond with:
- Authentic Islamic sources when possible
- Respectful and humble tone
- Clear, practical guidance
- Citations from Quran/Hadith when relevant
- Acknowledgment of scholarly differences when they exist

If you're unsure about religious rulings, recommend consulting a qualified Islamic scholar."""

class IslamicMCPTools:
    """Islamic-specific tools for DeenMate"""
    
    @staticmethod
    def get_islamic_tools() -> List[Dict[str, Any]]:
        """Return Islamic-specific MCP tools"""
        
        return [
            {
                "name": "islamic_guidance",
                "description": "Provide Islamic guidance and religious advice",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "Islamic question or topic for guidance"
                        },
                        "context": {
                            "type": "string", 
                            "description": "Additional context or specific situation"
                        },
                        "madhab": {
                            "type": "string",
                            "description": "Islamic school of thought (Hanafi, Shafi, Maliki, Hanbali)",
                            "default": "General"
                        }
                    },
                    "required": ["question"]
                }
            },
            {
                "name": "quran_explanation",
                "description": "Explain Quranic verses with context and commentary",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "verse_reference": {
                            "type": "string",
                            "description": "Quran verse reference (e.g., 'Surah Al-Fatiha 1:1-7')"
                        },
                        "verse_text": {
                            "type": "string",
                            "description": "The actual verse text (optional)"
                        },
                        "explanation_type": {
                            "type": "string",
                            "description": "Type of explanation needed",
                            "enum": ["tafsir", "context", "practical", "linguistic"],
                            "default": "practical"
                        }
                    },
                    "required": ["verse_reference"]
                }
            },
            {
                "name": "hadith_guidance",
                "description": "Provide Hadith-based guidance and explanations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "Topic or theme for Hadith guidance"
                        },
                        "hadith_text": {
                            "type": "string",
                            "description": "Specific Hadith text (optional)"
                        },
                        "collection": {
                            "type": "string",
                            "description": "Hadith collection preference",
                            "enum": ["Sahih Bukhari", "Sahih Muslim", "Abu Dawud", "Tirmidhi", "Any"],
                            "default": "Any"
                        }
                    },
                    "required": ["topic"]
                }
            },
            {
                "name": "prayer_guidance",
                "description": "Provide guidance on Salah (prayer) related questions",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prayer_question": {
                            "type": "string",
                            "description": "Question about prayer, timing, or procedures"
                        },
                        "prayer_type": {
                            "type": "string",
                            "description": "Type of prayer",
                            "enum": ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Jummah", "Tahajjud", "General"],
                            "default": "General"
                        },
                        "situation": {
                            "type": "string",
                            "description": "Special circumstances (travel, illness, etc.)"
                        }
                    },
                    "required": ["prayer_question"]
                }
            },
            {
                "name": "zakat_calculator",
                "description": "Calculate Zakat obligations and provide guidance",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "wealth_type": {
                            "type": "string",
                            "description": "Type of wealth for Zakat calculation",
                            "enum": ["cash", "gold", "silver", "business", "agriculture", "livestock"],
                            "default": "cash"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Amount of wealth"
                        },
                        "currency": {
                            "type": "string",
                            "description": "Currency (e.g., USD, BDT, etc.)",
                            "default": "USD"
                        },
                        "calculation_method": {
                            "type": "string",
                            "description": "Zakat calculation method",
                            "enum": ["standard", "detailed"],
                            "default": "standard"
                        }
                    },
                    "required": ["wealth_type", "amount"]
                }
            },
            {
                "name": "islamic_content_generator",
                "description": "Generate Islamic educational content for DeenMate",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "content_type": {
                            "type": "string",
                            "description": "Type of content to generate",
                            "enum": ["daily_reminder", "educational_article", "dua", "dhikr", "reflection", "tip"],
                            "default": "daily_reminder"
                        },
                        "topic": {
                            "type": "string",
                            "description": "Specific Islamic topic or theme"
                        },
                        "target_audience": {
                            "type": "string",
                            "description": "Target audience",
                            "enum": ["general", "youth", "adults", "families", "converts"],
                            "default": "general"
                        },
                        "length": {
                            "type": "string",
                            "description": "Content length",
                            "enum": ["short", "medium", "long"],
                            "default": "medium"
                        }
                    },
                    "required": ["content_type"]
                }
            },
            {
                "name": "halal_haram_guidance",
                "description": "Provide guidance on Halal/Haram matters",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "item_or_action": {
                            "type": "string",
                            "description": "Item, food, action, or practice to evaluate"
                        },
                        "context": {
                            "type": "string",
                            "description": "Additional context or circumstances"
                        },
                        "evidence_level": {
                            "type": "string",
                            "description": "Level of evidence requested",
                            "enum": ["basic", "detailed", "scholarly"],
                            "default": "basic"
                        }
                    },
                    "required": ["item_or_action"]
                }
            },
            {
                "name": "ramadan_fasting_guide",
                "description": "Provide Ramadan and fasting guidance",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "fasting_question": {
                            "type": "string",
                            "description": "Question about fasting rules, timing, or practices"
                        },
                        "fasting_type": {
                            "type": "string",
                            "description": "Type of fasting",
                            "enum": ["Ramadan", "voluntary", "make_up", "kaffarah"],
                            "default": "Ramadan"
                        },
                        "personal_situation": {
                            "type": "string",
                            "description": "Personal circumstances (travel, illness, pregnancy, etc.)"
                        }
                    },
                    "required": ["fasting_question"]
                }
            }
        ]
    
    @staticmethod
    def get_islamic_resources() -> List[Dict[str, Any]]:
        """Return Islamic-specific MCP resources"""
        
        return [
            {
                "uri": "islamic://daily/content",
                "name": "Daily Islamic Content",
                "description": "Daily Quranic verses, Hadiths, and reflections",
                "mimeType": "application/json"
            },
            {
                "uri": "islamic://prayer/times", 
                "name": "Prayer Times Information",
                "description": "Current prayer times and Qibla direction",
                "mimeType": "application/json"
            },
            {
                "uri": "islamic://calendar/events",
                "name": "Islamic Calendar Events",
                "description": "Upcoming Islamic holidays and significant dates",
                "mimeType": "application/json"
            },
            {
                "uri": "islamic://content/library",
                "name": "Islamic Content Library",
                "description": "Curated Islamic educational content for DeenMate",
                "mimeType": "application/json"
            }
        ]

class IslamicContentGenerator:
    """Generate Islamic content for DeenMate app"""
    
    @staticmethod
    def generate_daily_content() -> Dict[str, Any]:
        """Generate daily Islamic content"""
        return {
            "date": datetime.now().isoformat(),
            "verse_of_day": {
                "reference": "Al-Baqarah 2:255 (Ayat al-Kursi)",
                "arabic": "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ",
                "translation": "Allah - there is no deity except Him, the Ever-Living, the Self-Sustaining",
                "reflection": "This powerful verse reminds us of Allah's absolute sovereignty and constant presence in our lives."
            },
            "hadith_of_day": {
                "text": "The best of people are those who benefit others.",
                "source": "Reported by Ahmad",
                "lesson": "Today, look for opportunities to help others and make a positive impact."
            },
            "dua_of_day": {
                "arabic": "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ",
                "transliteration": "Rabbana atina fi'd-dunya hasanatan wa fi'l-akhirati hasanatan wa qina 'adhab an-nar",
                "translation": "Our Lord, give us good in this world and good in the next world, and save us from the punishment of the Fire.",
                "source": "Quran 2:201"
            },
            "daily_tip": "Remember to make Dhikr (remembrance of Allah) throughout your day. Even simple phrases like 'SubhanAllah', 'Alhamdulillah', and 'Allahu Akbar' can bring immense spiritual benefit."
        }
    
    @staticmethod
    def generate_educational_content(topic: str, target_audience: str = "general") -> Dict[str, Any]:
        """Generate educational Islamic content"""
        return {
            "topic": topic,
            "target_audience": target_audience,
            "generated_at": datetime.now().isoformat(),
            "content_template": {
                "title": f"Understanding {topic} in Islam",
                "introduction": f"Learn about the importance and practice of {topic} in Islamic life.",
                "key_points": [
                    "Historical context and significance",
                    "Quranic and Hadith references", 
                    "Practical implementation",
                    "Common misconceptions",
                    "Modern applications"
                ],
                "sources": [
                    "Quran and authentic Hadith collections",
                    "Classical Islamic scholarship",
                    "Contemporary Islamic authorities"
                ],
                "call_to_action": f"Apply the teachings of {topic} in your daily Islamic practice."
            }
        }
