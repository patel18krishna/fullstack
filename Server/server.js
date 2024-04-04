const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

// Initialize Express app
const app = express();

// Set up middleware
app.use(bodyParser.json());

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/server', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});
const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));

// Define MongoDB Schema
const Schema = mongoose.Schema;
const yourDataSchema = new Schema({
  // Define schema fields as per your HTML form
  // Example:
  name: String,
  email: String,
  // Add more fields as needed
});

// Create MongoDB Model
const YourData = mongoose.model('YourData', yourDataSchema);

// Define a route to handle form submission
app.post('/submit-form', async (req, res) => {
  try {
    // Create a new document from the submitted form data
    const newData = new YourData(req.body);

    // Save the document to MongoDB
    await newData.save();

    // Respond with a success message
    res.status(200).send('Data saved successfully');
  } catch (error) {
    // Handle errors
    console.error(error);
    res.status(500).send('Internal Server Error');
  }
});

// Start the server
const port = 3000;
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});