/**
 * Open https://script.google.com with YOUR Google account.
 * New project → paste this file → Run createBothForms.
 * Grant permissions, then View → Logs for the live form links.
 */
function createBothForms() {
  var survey = buildForm_(
    "CEP Survey Questionnaire – IoT Bus Stop Overcrowding Prediction",
    SURVEY_ITEMS_
  );
  var feedback = buildForm_(
    "CEP Feedback Questionnaire – IoT Bus Stop Overcrowding Prediction",
    FEEDBACK_ITEMS_
  );
  Logger.log("SURVEY VIEW: " + survey.getPublishedUrl());
  Logger.log("SURVEY EDIT: " + survey.getEditUrl());
  Logger.log("FEEDBACK VIEW: " + feedback.getPublishedUrl());
  Logger.log("FEEDBACK EDIT: " + feedback.getEditUrl());
}

var DESC_ =
  "Nirmala Memorial Foundation College of Commerce and Science (Autonomous)\\n" +
  "Department of Information Technology\\n" +
  "Students: Mr. Om Keluskar (24TIT078), Mr. Jashith Agre (24TIT011)\\n" +
  "Project: IoT-Based Bus Stop System for Public Transport Overcrowding Prediction Using Machine Learning\\n" +
  "Site: Dindoshi Bus Depot, BEST Route 326";

function buildForm_(title, items) {
  var form = FormApp.create(title);
  form.setDescription(DESC_);
  form.setCollectEmail(false);
  form.setAllowResponseEdits(false);
  form.addTextItem().setTitle("Name of Participant").setRequired(true);
  items.forEach(function (it) {
    form.addMultipleChoiceItem()
      .setTitle(it.q)
      .setChoiceValues(it.opts)
      .setRequired(true);
  });
  return form;
}

var SURVEY_ITEMS_ = [
  {q:"How frequently do you experience overcrowding at Dindoshi Bus Depot or the BEST Route 326 bus stop?", opts:["Every Day","Several Times a Week","Occasionally","Rarely"]},
  {q:"Which mode of transport do you use most frequently to reach this stop?", opts:["BEST Bus (Route 326)","Other BEST Bus","Train then BEST Bus","Walking"]},
  {q:"What is the biggest problem you face because of overcrowding at the bus stop?", opts:["Missed bus / cannot board","Pushing or injury risk","Long uncomfortable wait","No crowding warning"]},
  {q:"Have you ever been unable to board a bus because the stop or doorway was too crowded?", opts:["Yes, Multiple Times","Yes, Once","No","Not Applicable"]},
  {q:"How safe do you feel while waiting at an overcrowded bus stop?", opts:["Very Safe","Safe","Unsafe","Very Unsafe"]},
  {q:"Have you ever reported overcrowding to depot staff or BEST officials?", opts:["Yes","No","Didn't Know How","Never Felt It Would Help"]},
  {q:"If you did report overcrowding, how satisfied were you with the response?", opts:["Very Satisfied","Satisfied","Dissatisfied","Never Reported"]},
  {q:"How important is it to warn commuters as soon as overcrowding is detected?", opts:["Extremely Important","Important","Slightly Important","Not Important"]},
  {q:"Do you think rain, heat, or peak hours make overcrowding at the stop more dangerous?", opts:["Strongly Agree","Agree","Disagree","Strongly Disagree"]},
  {q:"Would you trust an automated IoT system that predicts overcrowding using on-site lights, without requiring a mobile app?", opts:["Definitely Yes","Probably Yes","Probably No","Definitely No"]},
  {q:"Which feature would be most useful in a smart bus-stop overcrowding system?", opts:["On-site LED display","Telegram staff alerts","Live risk percentage","Bus-left operator button"]},
  {q:"Do you believe an IoT-based overcrowding prediction system can improve commuter safety at BEST bus stops?", opts:["Strongly Agree","Agree","Disagree","Strongly Disagree"]}
];

var FEEDBACK_ITEMS_ = [
  {q:"How easy was it to understand the purpose of the IoT bus-stop overcrowding system?", opts:["Very Easy","Easy","Neutral","Difficult"]},
  {q:"How useful do you think automatic passenger counting using the IoT sensor would be for overcrowding awareness?", opts:["Very Useful","Useful","Moderately Useful","Not Useful at All"]},
  {q:"How clear and understandable was the demonstrated overcrowding-prediction process?", opts:["Very Clear","Clear","Neutral","Unclear"]},
  {q:"How useful were the on-site red and green LED indicators for understanding crowding?", opts:["Very Useful","Useful","Moderately Useful","Not Useful at All"]},
  {q:"How useful would real-time Telegram alerts be for depot staff when crowding becomes CRITICAL?", opts:["Very Useful","Useful","Moderately Useful","Not Useful at All"]},
  {q:"How easy was it to understand the crowding information shown on the dashboard (count, weather, risk, status)?", opts:["Very Easy","Easy","Neutral","Difficult"]},
  {q:"How clearly did the hardware demonstration show how the sensor detects passenger crossings?", opts:["Very Clear","Clear","Neutral","Unclear"]},
  {q:"How confident are you that this system can warn of overcrowding faster than manual visual guessing?", opts:["Very Confident","Confident","Moderately Confident","Slightly Confident"]},
  {q:"Would you be willing to use this system if it remained available at Dindoshi Route 326?", opts:["Definitely Yes","Probably Yes","Not Sure","Definitely No"]},
  {q:"How clear and easy to understand were the NORMAL, WARNING, and CRITICAL status lights?", opts:["Very Clear","Clear","Neutral","Unclear"]},
  {q:"How useful do you think this system would be for improving crowding awareness at your bus stop?", opts:["Very Useful","Useful","Moderately Useful","Not Useful at All"]},
  {q:"Overall, how satisfied are you with the IoT bus-stop overcrowding system and its potential for commuter safety?", opts:["Very Satisfied","Satisfied","Neutral","Dissatisfied"]}
];
