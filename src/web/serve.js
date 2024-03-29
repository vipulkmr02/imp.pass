#!/usr/bin/node
const express = require("express");
const bodyParser = require("body-parser");
const session = require("express-session");
const { exec } = require("child_process");
const app = express();
const PORT = 4000;

app.set("view engine", "ejs");
app.use(express.static(__dirname + "/views"));
app.use('/css', express.static(__dirname + "/css"));
app.use(session({
    secret: 'secret-key',
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }
}));
app.use(bodyParser.urlencoded({ extended: true }));


app.get("/", (req, res) => { res.render("home"); });
app.get("/login", (req, res) => { res.render("login"); });

app.get("/signup-form", (req, res) => { res.render("signup"); });

app.get("/set", (req, res) => { res.render("set"); });
app.get("/get", (req, res) => { res.render("get"); });
app.get("/delete", (req, res) => { res.render("delete"); });
app.get("/update", (req, res) => { res.render("update"); });

app.get("/logout", (req, res) => {
    const USERNAME = req.session.user.username;

    exec(`cd ../src\n\
        python3 imp-pass.py -u${USERNAME} --logout`,
        (error, stdout, stderr) => { }
    );

});

app.post("/signup", (req, res) => {
    const username = (req.body.username);
    const pwd = (req.body.password);

    const cache_creds = `cd ../src\n\
            python3 imp-pass.py -u${username} -p${pwd}`;

    console.log(`${username}\n${pwd}`)

    var CONTENT = "";
    exec(
        `cd ../src\npython3 imp-pass.py -u${username} -p${pwd} --signup`,
        (error, stdout, stderr) => {
            if (error || stdout.includes("ERROR")) {
                console.log("SERVER ERROR");
                console.log(`stderr:\n${stderr}`);
                CONTENT = "<h1 style=\"font-family:Arial\">Sign UP failed</h1>";
            }

            else {
                CONTENT = "\
                    <h1 style=\"font-family:Arial\">\
                    Sign UP successful\
                    </h1>\
                    <a href=\"/\" \
                    style=\"font-family: Arial; \
                    text-decoration:none;\">\
                    LOGIN\
                    </a>";
            }
            res.send(CONTENT);
        }
    );

});

app.post("/authorize", (req, res) => {
    const { username, password } = req.body;
    console.log(`${password}`)
    const cache_creds = `cd ../src\n\
    python3 imp-pass.py -u${username} -p${password} --cache`;

    exec(
        cache_creds, (error, stdout, stderr) => {
            if (error) {
                console.log("SERVER ERROR");
                console.log(`stderr:\n${stderr}`);
                res.sendStatus(500).send("<p style=\"font-family: Arial\">Server Error</p>");
                return;
            } else if (stdout == "LOGIN FAILED") {
                console.log("Login Failed");
                res.send("<p style=\"font-family: Arial\"> Login Failed </p>");
                return;
            } else {
                req.session.user = { username };
                console.log(`stdout:\n${stdout}`);
                res.render("menu");
            }
        }
    )
});

app.post("/set-password", (req, res) => {
    const { PID, pwd } = req.body;
    const set_script = `cd ../src\n\
    python3 imp-pass.py -u${req.session.user.username} -q "set ${PID} ${pwd}"`;

    exec(set_script, (error, stdout, stderr) => {
        if (error)
            res.render("set", { msg: "SOME ERROR OCCURED" });
        else
            res.render("set", { msg: "OKAY" });
    })
});

app.post("/get-password", (req, res) => {
    const { PID } = req.body;
    const get_script = `cd ../src\n\
    python3 imp-pass.py -u${req.session.user.username} -q "get ${PID}"`;

    exec(get_script, (error, stdout, stderr) => {
        if (error) {
            res.render("get", { msg: "SOME ERROR OCCURED" });
        } else {
            res.render("get", { msg: `password: ${stdout}` })
        }
    })
});

app.post("/update-password", (req, res) => {
    const { PID, pwd } = req.body;
    const get_script = `cd ../src\n\
    python3 imp-pass.py -u${req.session.user.username} -q "update ${PID} ${pwd}"`;

    exec(get_script, (error, stdout, stderr) => {
        if (error) {
            res.render("update", { msg: "SOME ERROR OCCURED" });
        } else {
            res.render("update", { msg: `OKAY` })
        }
    })
});

app.post("/delete-password", (req, res) => {
    const { PID } = req.body;
    const get_script = `cd ../src\n\
    python3 imp-pass.py -u${req.session.user.username} -q "delete ${PID}"`;

    exec(get_script, (error, stdout, stderr) => {
        if (error) {
            res.render("delete", { msg: "SOME ERROR OCCURED" });
        } else {
            res.render("delete", { msg: `OKAY` })
        }
    })
});

app.post("/logout-session")

app.listen(PORT, () => {
    console.log(`server started\nPORT ${PORT}`);
});

