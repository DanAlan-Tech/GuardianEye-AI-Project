require('dotenv').config();
const express = require('express');
const twilio = require('twilio');

const app = express();
app.use(express.json()); // Parses incoming JSON alert payloads

// Initialize Twilio Client using secure environment variables
const accountSid = process.env.TWILIO_ACCOUNT_SID;
const authToken = process.env.TWILIO_AUTH_TOKEN;
const client = twilio(accountSid, authToken);

/**
 * Endpoint to catch third-party or system alerts and route via SMS
 */
app.post('/webhook/alert', async (req, res) => {
    try {
        // Extract alert properties from your monitoring tool's request body
        const { alertTitle, severity, serverIp } = req.body;

        if (!alertTitle) {
            return res.status(400).json({ error: 'Missing alert information' });
        }

        // Construct the real-time notification text
        const messageBody = `🚨 ALERT TRIGGERED:\nTitle: ${alertTitle}\nSeverity: ${severity || 'UNKNOWN'}\nServer IP: ${serverIp || 'N/A'}`;

        // Dispatch the SMS via Twilio REST API
        const smsResponse = await client.messages.create({
            body: messageBody,
            from: process.env.TWILIO_PHONE_NUMBER, // Your Twilio long-code or short-code
            to: process.env.ALERT_RECIPIPIENT_NUMBER // Destination number (E.164 format)
        });

        // Respond immediately with 200 OK to the system that fired the alert
        return res.status(200).json({ 
            success: true, 
            messageSid: smsResponse.sid 
        });

    } catch (error) {
        console.error('Failed to process alert webhook:', error.message);
        return res.status(500).json({ error: 'Internal Server Error' });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Alert Hook listening on port ${PORT}`));
