import redis from 'redis';

const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err.message}`);
    });

const key = 'HolbertonSchools';
const values = {
  Portland: 50,
  Seattle: 80,
  'New York': 20,
  Bogota: 20,
  Cali: 40,
  Paris: 2
};

// Store hash in Redis
for (const [key, value] of Object.entries(values)) {
  client.hset(key, 'value', value, redis.print);
}

//Display all the fields and values stored in Hash
client.hgetall(key, (err, obj) => {
  console.log(obj);
});