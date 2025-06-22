var db = connect(
    "mongodb://lifeweb:It5~TPn04p1-eTAH@localhost:27017/admin"
);
db.createUser(
{
    user: "exporter",
    pwd: "exporter",
    roles: [
        { role: "clusterMonitor", db: "admin"},
        { role: "read", db: "appdb" }
    ]
})
