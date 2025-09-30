print(">>> Initiating Config Server Replica Set...");
rs.initiate({
  _id: "configReplSet",
  configsvr: true,
  members: [{ _id: 0, host: "localhost:27018" }],
});

print(">>> Initiating Shard1 Replica Set...");
rs.initiate({
  _id: "shard1",
  members: [{ _id: 0, host: "localhost:27019" }],
});

print(">>> Initiating Shard2 Replica Set...");
rs.initiate({
  _id: "shard2",
  members: [{ _id: 0, host: "localhost:27020" }],
});

print(">>> Adding shards to the cluster...");
sh.addShard("shard1ReplSet/shard1:27019");
sh.addShard("shard2ReplSet/shard2:27020");

print(">>> Sharded cluster initialization complete!");
