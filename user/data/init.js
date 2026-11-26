db = db.getSiblingDB("userdb");

const fs = require("fs");

const usersData = JSON.parse(fs.readFileSync("/seed/users.json", "utf8"));
db.users.drop();
db.users.insertMany(usersData.users);
