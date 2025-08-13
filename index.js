const { Telegraf } = require('telegraf');
const https = require('https');
const fetch = require('node-fetch');

// Disable SSL verification for development (Node.js environment level)
process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = 0;

// Bot token
const token = '8445356732:AAF-19VhpFcwT2rUW81HOgry1yZ9RxY1QTY';

// Create HTTPS agent that ignores SSL certificate verification (for development only)
const httpsAgent = new https.Agent({
    rejectUnauthorized: false,
    checkServerIdentity: () => undefined,
    secureProtocol: 'TLS_method',
    keepAlive: true,
    timeout: 30000
});

// Create bot instance with custom HTTPS agent and additional options
const bot = new Telegraf(token, {
    telegram: {
        agent: httpsAgent,
        apiRoot: 'https://api.telegram.org',
        attachmentAgent: httpsAgent
    },
    handlerTimeout: 90000
});

// Handle /start command
bot.start(async (ctx) => {
    const userName = ctx.from.first_name || 'User';
    await ctx.reply(`Hello ${userName}! I'm your bot.`);
});

// Main function to start the bot
async function main() {
    try {
        console.log('Starting bot...');
        
        // Test direct API call first to debug the issue
        try {
            console.log('Testing direct API call...');
            const response = await fetch(`https://api.telegram.org/bot${token}/getMe`, {
                agent: httpsAgent,
                headers: {
                    'User-Agent': 'Telegraf/4.15.6',
                    'Content-Type': 'application/json'
                },
                timeout: 10000
            });
            
            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers.raw());
            
            const responseText = await response.text();
            console.log('Response body (first 500 chars):', responseText.substring(0, 500));
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${responseText}`);
            }
            
            const botInfo = JSON.parse(responseText);
            console.log('Bot info:', botInfo);
            
        } catch (error) {
            console.error('Direct API call failed:', error.message);
            console.error('Full error:', error);
            throw error;
        }
        
        // Set up logging
        bot.use((ctx, next) => {
            const userName = ctx.from?.first_name || 'User';
            const userId = ctx.from?.id || 'Unknown';
            const text = ctx.message?.text || ctx.update_type;
            console.log(`Received message from ${userName} (ID: ${userId}): ${text}`);
            return next();
        });
        
        // Start polling with error handling
        await bot.launch({
            polling: {
                timeout: 30,
                limit: 100,
                allowedUpdates: ['message', 'callback_query']
            }
        });
        console.log('Bot is running...');
        
        // Enable graceful stop
        process.once('SIGINT', () => bot.stop('SIGINT'));
        process.once('SIGTERM', () => bot.stop('SIGTERM'));
        
    } catch (error) {
        console.error('Error starting bot:', error);
        process.exit(1);
    }
}

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
    console.error('Uncaught Exception:', error);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

// Start the bot if this file is run directly
if (require.main === module) {
    main();
}

module.exports = { bot, main };
