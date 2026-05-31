<!DOCTYPE html>
<html>
<head>
  <title>Rural RPM Intake Form</title>
  <style>
    body { font-family: Arial; background: #f4f6f8; margin: 30px; }
    .container { max-width: 1000px; margin: auto; background: white; padding: 25px; border-radius: 12px; }
    h1 { color: #12355b; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; }
    label { font-weight: bold; display: block; margin-top: 12px; }
    input, select, textarea { width: 100%; padding: 10px; margin-top: 5px; }
    .checkbox label { font-weight: normal; }
    button { margin-top: 20px; padding: 12px; background: #1f7a4d; color: white; border: none; font-size: 16px; border-radius: 8px; }
    .panel { border: 1px solid #ddd; padding: 18px; border-radius: 10px; }
  </style>
</head>
<body>

<div class="container">
  <h1>Rural RPM Patient Intake Form</h1>

  <div class="grid">
    <div class="panel">
      <h2>Patient Information</h2>
      <label>Patient Name</label><input type="text">
      <label>Patient ID</label><input type="text">
      <label>Age</label><input type="number">
      <label>Rural Location / County</label><input type="text">
      <label>Caregiver Name</label><input type="text">

      <label>Preferred Contact</label>
      <select>
        <option>SMS</option>
        <option>Phone Call</option>
        <option>App</option>
        <option>Caregiver</option>
      </select>
    </div>

    <div class="panel">
      <h2>RPM / Triage Inputs</h2>
      <label>Weight</label><input type="text">
      <label>Blood Pressure</label><input type="text">
      <label>Heart Rate</label><input type="text">
      <label>SpO2</label><input type="text">
      <label>Glucose</label><input type="text">
      <label>Temperature</label><input type="text">
    </div>
  </div>

  <div class="panel" style="margin-top:25px;">
    <h2>Symptoms</h2>
    <div class="checkbox"><label><input type="checkbox"> Shortness of breath</label></div>
    <div class="checkbox"><label><input type="checkbox"> Chest pain</label></div>
    <div class="checkbox"><label><input type="checkbox"> Dizziness</label></div>
    <div class="checkbox"><label><input type="checkbox"> Swelling</label></div>
    <div class="checkbox"><label><input type="checkbox"> Fatigue</label></div>
    <div class="checkbox"><label><input type="checkbox"> Difficulty sleeping flat</label></div>
  </div>

  <div class="panel" style="margin-top:25px;">
    <h2>Notes</h2>
    <label>Medication Notes</label>
    <textarea rows="4"></textarea>

    <label>Additional Notes</label>
    <textarea rows="4"></textarea>
  </div>

  <button onclick="alert('Prototype only: data would be sent to multiagent model.')">
    Send to Multiagent Model
  </button>
</div>

</body>
</html>