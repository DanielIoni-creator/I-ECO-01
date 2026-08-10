const express = require('express');
const router = express.Router();
const { Parser } = require('json2csv');

const listings = [
  { id: 1, plant: 'Tomato', variety: 'Cherry', quantity: 50, location: 'Rome', lat: 41.9028, lng: 12.4964 },
  { id: 2, plant: 'Basil', variety: 'Genovese', quantity: 30, location: 'Milan', lat: 45.4642, lng: 9.1900 },
];

router.get('/csv', (req, res) => {
  try {
    const parser = new Parser();
    const csv = parser.parse(listings);
    res.setHeader('Content-Type', 'text/csv');
    res.setHeader('Content-Disposition', 'attachment; filename=export.csv');
    res.status(200).send(csv);
  } catch (err) {
    res.status(500).json({ error: 'CSV export failed' });
  }
});

router.get('/geojson', (req, res) => {
  try {
    const geojson = {
      type: 'FeatureCollection',
      features: listings.map(item => ({
        type: 'Feature',
        geometry: { type: 'Point', coordinates: [item.lng, item.lat] },
        properties: { id: item.id, plant: item.plant, variety: item.variety, quantity: item.quantity, location: item.location }
      }))
    };
    res.status(200).json(geojson);
  } catch (err) {
    res.status(500).json({ error: 'GeoJSON export failed' });
  }
});

module.exports = router;
