/* Velenje */
db.runCommand({
    geoNear: 'stations',
    near: { type: "Point" , coordinates: [ 15.101902, 46.34309 ] } ,
    spherical: true,
    maxDistance: 10000,
    query: {"prices.petrol-q-max-95" : {$exists: true}}
});

/* Ljubljana */
db.runCommand({
    geoNear: 'stations',
    near: { type: "Point" , coordinates: [ 14.5058, 46.0569 ] } ,
    spherical: true,
    maxDistance: 10000,
    query: {"prices.petrol-q-max-95" : {$exists: true}}
});


