import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    symbol_shares = db.execute("SELECT symbol,SUM(shares) FROM purchases WHERE id=:user_id GROUP BY symbol ",user_id=session["user_id"])
    name_prices={}
    for i in symbol_shares:
        sym = i["symbol"]
        name_prices[sym] = lookup(sym)

    user = db.execute("SELECT cash FROM users WHERE id=:user_id",user_id=session["user_id"])
    available = user[0]["cash"]
    return render_template("index.html", symbol_shares=symbol_shares, name_prices=name_prices, available=available)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = int(request.form.get("shares"))

        if not symbol:
            return apology("must provide symbol")
        if not shares:
            return apology("must provide shares")
        if lookup(symbol) == None:
            return apology("provided symbol doesn't exist")

        quote = lookup(symbol)
        """Get stock quote."""
        userow = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"] )
        remaining = userow[0]["cash"]
        per_share = quote["price"]
        if remaining < (per_share * shares):
            return apology("not enough balance.")
        remaining = remaining - (per_share * shares)
        db.execute("INSERT INTO purchases (id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                        user_id=session["user_id"], symbol=symbol, shares=shares, price=per_share)
        db.execute("UPDATE users SET cash=:remaining WHERE id=:user_id",
                        remaining=remaining, user_id=session["user_id"])
        return redirect("/")

    else:
        return render_template("buy.html")

    """Buy shares of stock"""
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    symbol_shares = db.execute("SELECT symbol,shares,transacted,price FROM purchases WHERE id=:user_id ORDER BY transacted",user_id=session["user_id"])

    return render_template("history.html", symbol_shares=symbol_shares)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()

        if not symbol:
            return apology("must provide symbol")

        if lookup(symbol) == None:
            return apology("provided symbol doesn't exist")

        quote1 = lookup(symbol)

        """Get stock quote."""
        return render_template("quoted.html", quote = quote1)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not confirmation:
            return apology("must provide password", 403)

        elif not password:
            return apology("must provide password", 403)

        elif password != confirmation:
            return apology("password do not match", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 0:
            return apology("Username already exists", 403)
        password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash1)",username=username, hash1=password)

        usern = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        # Remember which user has logged in
        session["user_id"] = usern[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if not symbol:
            return apology("must provide symbol")
        if not shares:
            return apology("must provide shares")
        if lookup(symbol) == None:
            return apology("provided symbol doesn't exist")

        quote = lookup(symbol)
        """Get stock quote."""
        userow = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"] )
        remaining = userow[0]["cash"]
        per_share = quote["price"]


        usepur = db.execute("SELECT SUM(shares) FROM purchases WHERE (id=:user_id AND symbol=:symbol) GROUP BY symbol ",
                            user_id=session["user_id"], symbol=symbol)
        owned_shares = usepur[0]["SUM(shares)"]

        if owned_shares < shares:
            return apology("not enough shares.")

        remaining = remaining + (per_share * shares)
        db.execute("INSERT INTO purchases (id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                        user_id=session["user_id"], symbol=symbol, shares= -shares, price=per_share)
        db.execute("UPDATE users SET cash=:remaining WHERE id=:user_id",
                        remaining=remaining, user_id=session["user_id"])
        return redirect("/")

    else:
        symbols = db.execute("SELECT symbol FROM purchases WHERE id=:user_id GROUP BY symbol",user_id=session["user_id"])
        return render_template("sell.html",symbols=symbols)

    """Buy shares of stock"""
    return apology("TODO")

@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    if request.method == "POST":
        try:
            amount = float(request.form.get("amount"))
        except:
            return apology("amount must be a real number", 400)

        if not amount:
            return apology("enter a positive amount")


        db.execute("UPDATE users SET cash = cash + :amount WHERE id=:user_id",
                        amount=amount, user_id=session["user_id"])
        return redirect("/")

    else:
        return render_template("addcash.html")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
