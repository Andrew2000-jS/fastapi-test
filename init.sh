#!/bin/bash
set -e

echo ">>> Starting Config Server (configReplSet)..."
mongod --configsvr --replSet configReplSet --port 27018 --dbpath /data/configsvr --bind_ip_all &

echo ">>> Waiting for Config Server..."
until mongosh --host configsvr --port 27018 --eval "db.adminCommand('ping')" &> /dev/null; do
  echo "Config server not ready yet. Retrying in 2 seconds..."
  sleep 2
done
echo ">>> Config server is ready."

echo ">>> Initiating Config Server replica set..."
mongosh --host configsvr --port 27018 <<EOF
rs.initiate({
  _id: "configReplSet",
  configsvr: true,
  members: [{ _id: 0, host: "configsvr:27018" }]
})
EOF
echo ">>> Config Server replica set initialized."

echo ">>> Starting Shard1..."
mongod --shardsvr --replSet shard1ReplSet --port 27019 --dbpath /data/shard1 --bind_ip_all &

echo ">>> Starting Shard2..."
mongod --shardsvr --replSet shard2ReplSet --port 27020 --dbpath /data/shard2 --bind_ip_all &

echo ">>> Waiting for Shard1..."
until mongosh --host shard1 --port 27019 --eval "db.adminCommand('ping')" &> /dev/null; do
  echo "Shard1 not ready yet. Retrying in 2 seconds..."
  sleep 2
done

echo ">>> Waiting for Shard2..."
until mongosh --host shard2 --port 27020 --eval "db.adminCommand('ping')" &> /dev/null; do
  echo "Shard2 not ready yet. Retrying in 2 seconds..."
  sleep 2
done

echo ">>> Initiating Shard1 replica set..."
mongosh --host shard1 --port 27019 <<EOF
rs.initiate({
  _id: "shard1ReplSet",
  members: [{ _id: 0, host: "shard1:27019" }]
})
EOF

echo ">>> Initiating Shard2 replica set..."
mongosh --host shard2 --port 27020 <<EOF
rs.initiate({
  _id: "shard2ReplSet",
  members: [{ _id: 0, host: "shard2:27020" }]
})
EOF

echo ">>> Starting mongos..."
mongos --configdb configReplSet/configsvr:27018 --bind_ip_all --port 27017 &

echo ">>> Waiting for mongos..."
until mongosh --host localhost --port 27017 --eval "db.adminCommand('ping')" &> /dev/null; do
  sleep 2
done
echo ">>> Mongos router is ready."

echo ">>> Adding shards to the cluster..."
mongosh --host localhost --port 27017 <<EOF
sh.addShard("shard1ReplSet/shard1:27019")
sh.addShard("shard2ReplSet/shard2:27020")
EOF

echo ">>> Shards added. Cluster setup complete."

wait
