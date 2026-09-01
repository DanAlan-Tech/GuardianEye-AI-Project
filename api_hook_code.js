require('dotenv').config();
const express = require('express');
const twilio = require('twilio');

const app = express();
app.use(express.json()); 

const accountSid = process.env.TWILIO_ACCOUNT_SID;
const authToken = process.env.TWILIO_AUTH_TOKEN;
const client = twilio(accountSid, authToken);



app.post('/webhook/alert', async (req, res) => {
    try {
       
        const { alertTitle, severity, serverIp } = req.body;

        if (!alertTitle) {
            return res.status(400).json({ error: 'Missing alert information' });
        }

       
        const messageBody = `🚨 ALERT TRIGGERED:\nTitle: ${alertTitle}\nSeverity: ${severity || 'UNKNOWN'}\nServer IP: ${serverIp || 'N/A'}`;

        const smsResponse = await client.messages.create({
            body: messageBody,
            from: process.env.TWILIO_PHONE_NUMBER, 
            to: process.env.ALERT_RECIPIPIENT_NUMBER 

    
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
