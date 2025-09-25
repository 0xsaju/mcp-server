// Custom n8n node for DeenMate MCP Server integration
const { IExecuteFunctions } = require('n8n-workflow');

class DeenMateMCP {
  description = {
    displayName: 'DeenMate MCP',
    name: 'deenmateMcp',
    group: ['transform'],
    version: 1,
    subtitle: '={{$parameter["operation"]}}',
    description: 'Interact with DeenMate MCP Server for Islamic AI operations',
    defaults: {
      name: 'DeenMate MCP',
    },
    inputs: ['main'],
    outputs: ['main'],
    credentials: [
      {
        name: 'deenmateMcpApi',
        required: true,
      },
    ],
    properties: [
      {
        displayName: 'Operation',
        name: 'operation',
        type: 'options',
        noDataExpression: true,
        options: [
          {
            name: 'Islamic Guidance',
            value: 'islamicGuidance',
            description: 'Get Islamic guidance and religious advice',
            action: 'Get Islamic guidance',
          },
          {
            name: 'Calculate Zakat',
            value: 'calculateZakat',
            description: 'Calculate Zakat obligations',
            action: 'Calculate Zakat',
          },
          {
            name: 'Generate Islamic Content',
            value: 'generateContent',
            description: 'Generate Islamic educational content',
            action: 'Generate Islamic content',
          },
          {
            name: 'Generate Flutter Code',
            value: 'generateFlutter',
            description: 'Generate Flutter code for Islamic features',
            action: 'Generate Flutter code',
          },
          {
            name: 'Generate Backend API',
            value: 'generateBackend',
            description: 'Generate TypeScript backend API',
            action: 'Generate backend API',
          },
          {
            name: 'Prayer Guidance',
            value: 'prayerGuidance',
            description: 'Get guidance on prayer-related questions',
            action: 'Get prayer guidance',
          },
          {
            name: 'Get Daily Content',
            value: 'getDailyContent',
            description: 'Retrieve daily Islamic content',
            action: 'Get daily content',
          },
        ],
        default: 'islamicGuidance',
      },
      
      // Islamic Guidance fields
      {
        displayName: 'Question',
        name: 'question',
        type: 'string',
        required: true,
        displayOptions: {
          show: {
            operation: ['islamicGuidance'],
          },
        },
        default: '',
        placeholder: 'What is your Islamic question?',
        description: 'The Islamic question you need guidance on',
      },
      {
        displayName: 'Context',
        name: 'context',
        type: 'string',
        displayOptions: {
          show: {
            operation: ['islamicGuidance'],
          },
        },
        default: '',
        placeholder: 'Additional context or situation',
        description: 'Optional additional context for the question',
      },
      {
        displayName: 'Madhab',
        name: 'madhab',
        type: 'options',
        displayOptions: {
          show: {
            operation: ['islamicGuidance'],
          },
        },
        options: [
          { name: 'General', value: 'General' },
          { name: 'Hanafi', value: 'Hanafi' },
          { name: 'Shafi', value: 'Shafi' },
          { name: 'Maliki', value: 'Maliki' },
          { name: 'Hanbali', value: 'Hanbali' },
        ],
        default: 'General',
        description: 'Islamic school of thought',
      },
      
      // Zakat calculation fields
      {
        displayName: 'Wealth Type',
        name: 'wealthType',
        type: 'options',
        required: true,
        displayOptions: {
          show: {
            operation: ['calculateZakat'],
          },
        },
        options: [
          { name: 'Cash', value: 'cash' },
          { name: 'Gold', value: 'gold' },
          { name: 'Silver', value: 'silver' },
          { name: 'Business', value: 'business' },
          { name: 'Agriculture', value: 'agriculture' },
        ],
        default: 'cash',
        description: 'Type of wealth for Zakat calculation',
      },
      {
        displayName: 'Amount',
        name: 'amount',
        type: 'number',
        required: true,
        displayOptions: {
          show: {
            operation: ['calculateZakat'],
          },
        },
        default: 0,
        description: 'Amount of wealth',
      },
      {
        displayName: 'Currency',
        name: 'currency',
        type: 'options',
        displayOptions: {
          show: {
            operation: ['calculateZakat'],
          },
        },
        options: [
          { name: 'USD', value: 'USD' },
          { name: 'BDT', value: 'BDT' },
          { name: 'EUR', value: 'EUR' },
          { name: 'GBP', value: 'GBP' },
          { name: 'SAR', value: 'SAR' },
        ],
        default: 'USD',
        description: 'Currency for calculation',
      },
      
      // Content generation fields
      {
        displayName: 'Content Type',
        name: 'contentType',
        type: 'options',
        required: true,
        displayOptions: {
          show: {
            operation: ['generateContent'],
          },
        },
        options: [
          { name: 'Daily Reminder', value: 'daily_reminder' },
          { name: 'Educational Article', value: 'educational_article' },
          { name: 'Dua', value: 'dua' },
          { name: 'Dhikr', value: 'dhikr' },
          { name: 'Reflection', value: 'reflection' },
          { name: 'Tip', value: 'tip' },
        ],
        default: 'daily_reminder',
        description: 'Type of Islamic content to generate',
      },
      {
        displayName: 'Topic',
        name: 'topic',
        type: 'string',
        displayOptions: {
          show: {
            operation: ['generateContent'],
          },
        },
        default: '',
        placeholder: 'Specific topic (optional)',
        description: 'Specific Islamic topic for content generation',
      },
      
      // Code generation fields
      {
        displayName: 'Feature Name',
        name: 'featureName',
        type: 'string',
        required: true,
        displayOptions: {
          show: {
            operation: ['generateFlutter', 'generateBackend'],
          },
        },
        default: '',
        placeholder: 'Name of the feature',
        description: 'Name of the feature to generate code for',
      },
      {
        displayName: 'Feature Type',
        name: 'featureType',
        type: 'options',
        displayOptions: {
          show: {
            operation: ['generateFlutter'],
          },
        },
        options: [
          { name: 'Prayer Times', value: 'prayer_times' },
          { name: 'Zakat Calculator', value: 'zakat_calculator' },
          { name: 'Quran Reader', value: 'quran_reader' },
          { name: 'Hadith Reader', value: 'hadith_reader' },
          { name: 'Islamic Content', value: 'islamic_content' },
          { name: 'Custom', value: 'custom' },
        ],
        default: 'custom',
        description: 'Type of Islamic feature',
      },
      
      // Prayer guidance fields
      {
        displayName: 'Prayer Question',
        name: 'prayerQuestion',
        type: 'string',
        required: true,
        displayOptions: {
          show: {
            operation: ['prayerGuidance'],
          },
        },
        default: '',
        placeholder: 'Your prayer-related question',
        description: 'Question about Islamic prayer',
      },
    ],
  };

  async execute(this: IExecuteFunctions) {
    const items = this.getInputData();
    const returnData = [];
    const credentials = await this.getCredentials('deenmateMcpApi');
    
    const baseUrl = credentials.url || 'http://localhost:8080';

    for (let i = 0; i < items.length; i++) {
      const operation = this.getNodeParameter('operation', i) as string;

      try {
        let endpoint = '';
        let requestBody = {};

        switch (operation) {
          case 'islamicGuidance':
            endpoint = '/islamic/guidance';
            requestBody = {
              question: this.getNodeParameter('question', i),
              context: this.getNodeParameter('context', i),
              madhab: this.getNodeParameter('madhab', i),
            };
            break;

          case 'calculateZakat':
            endpoint = '/islamic/zakat';
            requestBody = {
              wealth_type: this.getNodeParameter('wealthType', i),
              amount: this.getNodeParameter('amount', i),
              currency: this.getNodeParameter('currency', i),
            };
            break;

          case 'generateContent':
            endpoint = '/islamic/content';
            requestBody = {
              content_type: this.getNodeParameter('contentType', i),
              topic: this.getNodeParameter('topic', i),
              target_audience: 'general',
              length: 'medium',
            };
            break;

          case 'generateFlutter':
            endpoint = '/code/flutter';
            requestBody = {
              feature_name: this.getNodeParameter('featureName', i),
              feature_type: this.getNodeParameter('featureType', i),
              components: ['widget', 'screen'],
              islamic_context: true,
            };
            break;

          case 'generateBackend':
            endpoint = '/code/backend';
            requestBody = {
              api_name: this.getNodeParameter('featureName', i),
              api_type: 'custom',
              http_methods: ['GET', 'POST'],
              include_auth: true,
              include_validation: true,
            };
            break;

          case 'prayerGuidance':
            endpoint = '/tools/call';
            requestBody = {
              tool_name: 'prayer_guidance',
              arguments: {
                prayer_question: this.getNodeParameter('prayerQuestion', i),
                prayer_type: 'General',
                situation: '',
              },
            };
            break;

          case 'getDailyContent':
            endpoint = '/islamic/daily';
            // GET request, no body needed
            break;

          default:
            throw new Error(`Unknown operation: ${operation}`);
        }

        const method = operation === 'getDailyContent' ? 'GET' : 'POST';
        
        const response = await this.helpers.httpRequest({
          method,
          url: `${baseUrl}${endpoint}`,
          body: method === 'POST' ? requestBody : undefined,
          headers: {
            'Content-Type': 'application/json',
          },
        });

        returnData.push({
          json: {
            operation,
            success: response.success || true,
            data: response.data || response,
            message: response.message || 'Operation completed successfully',
            timestamp: new Date().toISOString(),
          },
        });

      } catch (error) {
        if (this.continueOnFail()) {
          returnData.push({
            json: {
              operation,
              success: false,
              error: error.message,
              timestamp: new Date().toISOString(),
            },
          });
        } else {
          throw error;
        }
      }
    }

    return [returnData];
  }
}

module.exports = {
  DeenMateMCP,
};
