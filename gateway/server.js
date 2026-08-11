const express = require('express');
const cors = require('cors');
const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'MyZubster Gateway' });
});

app.listen(port, () => {
  console.log(`🚀 MyZubster Gateway running on port ${port}`);
});
