# Google Forms — 2-minute setup

Google Forms can only be created while **you** are logged into Google. This project cannot open your Gmail.

## Fastest way

1. Open https://script.google.com (your college/Gmail account).
2. **New project** → delete the stub → paste `scripts/Create_CEP_Google_Forms.gs`.
3. Run **createBothForms** → Allow permissions.
4. **Executions** / **Logs** will show:
   - Survey view + edit links
   - Feedback view + edit links
5. Send those two view links back so they can be dropped into References [12] and [13].

## Manual way (same 12+12 questions)

Create two forms at https://forms.google.com (turn **Collect email addresses** off).

**Form 1 title:** CEP Survey Questionnaire – IoT Bus Stop Overcrowding Prediction  
**Form 2 title:** CEP Feedback Questionnaire – IoT Bus Stop Overcrowding Prediction  

Description for both:

```
Nirmala Memorial Foundation College of Commerce and Science (Autonomous)
Department of Information Technology
Students: Mr. Om Keluskar (24TIT078), Mr. Jashith Agre (24TIT011)
Project: IoT-Based Bus Stop System for Public Transport Overcrowding Prediction Using Machine Learning
Site: Dindoshi Bus Depot, BEST Route 326
```

Add **Name of Participant** (short answer, required), then copy the 12 questions from the matching PDF.
