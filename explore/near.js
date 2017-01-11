db.stations.find({
    company: 'petrol',
    loc: {$near: {$geometry: {type: "Point", coordinates: [14.5058, 46.0569]}, $maxDistance: 100000}},
    'prices.bencin-95': {$exists: 1}
}, {
    name: 1,
    key: 1,
    'prices.bencin-95': 1
}).sort({
    'prices.bencin-95': 1
});