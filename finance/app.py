import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import re

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    transactionsDB = db.execute(
        "SELECT symbol, stock_name, SUM(shares) AS shares FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    stock_index = []
    total_value = 0
    for transaction in transactionsDB:
        stock = lookup(transaction["symbol"])
        stock_index.append({
            "symbol": stock["symbol"],
            "name": stock["name"],
            "shares": transaction["shares"],
            "price": stock["price"],
            "total": stock["price"] * transaction["shares"],
        })
        total_value += stock["price"] * transaction["shares"]

    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]
    return render_template("index.html", stock_index=stock_index, cash=cash, total_value=total_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        if lookup(request.form.get("symbol")) == None:
            return apology("No such stock :(", 400)
        if not request.form.get("shares"):
            return apology("No shares selected")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Bad shares")
        stock = lookup(request.form.get("symbol"))
        symbol = request.form.get("symbol")

        shares_price = shares * stock["price"]
        user_id = session["user_id"]
        cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = cash_db[0]["cash"]
        now = datetime.now()
        newbalance = cash - shares_price
        db.execute("SELECT * FROM transactions WHERE symbol = ?", symbol)
        if shares_price > cash:
            return apology("Not enough money")
        elif shares < 0:
            return apology("Negative shares")
        else:
            db.execute("INSERT INTO transactions (user_id, symbol, stock_name, price, shares, date) VALUES(?, ?, ?, ?, ?, ?)",
                       user_id, symbol.upper(), stock["name"], stock["price"], shares, now)
            db.execute("INSERT INTO history (user_id, symbol, stock_name, price, shares, transaction_type, date) VALUES(?, ?, ?, ?, ?, ?, ?)",
                       user_id, symbol.upper(), stock["name"], stock["price"], shares, "bought", now)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newbalance, user_id)
            return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    historyDB = db.execute(
        "SELECT symbol, stock_name, price, shares, transaction_type, date FROM history WHERE user_id = ? ORDER BY date DESC", user_id)
    history_info = []
    for row in historyDB:
        history_info.append({
            "symbol": row["symbol"],
            "stock_name": row["stock_name"],
            "price": row["price"],
            "shares": row["shares"],
            "transaction_type": row["transaction_type"],
            "date": row["date"],
        })
    return render_template("history.html", history_info=history_info)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        SymbolInfo = lookup(request.form.get("symbol"))
        if lookup(request.form.get("symbol")) == None:
            return apology("No such stock :(", 400)
        return render_template("quoted.html", name=SymbolInfo["name"], symbol=SymbolInfo["symbol"], price=usd(SymbolInfo["price"]))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        if len(request.form.get("password")) < 8:
            return apology("Make sure your password is at least 8 letters")
        elif re.search('[0-9]', request.form.get("password")) is None:
            return apology("Make sure your password has a number in it")
        elif re.search('[A-Z]', request.form.get("password")) is None:
            return apology("Make sure your password has a capital letter in it")

        elif not request.form.get("confirmation") or request.form.get("confirmation") != request.form.get("password"):
            return apology("must provide correct confirmation")

        hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        # Query database for username
        try:
            # Remember registrant
            user = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), hash)
            session["user_id"] = user
            return redirect("/")
        except:
            return apology("Nickname already used", 400)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        stockDB = db.execute("SELECT symbol, SUM(shares) AS shares FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
        return render_template("sell.html", stockDB=stockDB)
    else:
        user_id = session["user_id"]
        symbol = request.form.get("symbol")
        shares = int(float(request.form.get("shares")))
        user_shares_db = db.execute(
            "SELECT SUM(shares) AS shares FROM transactions WHERE user_id = ? and symbol = ? GROUP BY symbol", user_id, symbol)
        user_shares = user_shares_db[0]["shares"]
        if not request.form.get("symbol"):
            return apology("Failed to select a stock")
        elif not request.form.get("shares") or shares > user_shares:
            return apology("Invalid amount of shares")
        else:
            stock = lookup(request.form.get("symbol"))
            symbol = request.form.get("symbol")
            shares_price = shares * stock["price"]
            cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
            cash = cash_db[0]["cash"]
            newbalance = cash + shares_price
            new_shares = user_shares - shares
            now = datetime.now()
            new_shares = -1 * shares
            if shares == user_shares:
                db.execute("DELETE FROM transactions WHERE symbol = ?", symbol)
                db.execute("INSERT INTO history (user_id, symbol, stock_name, price, shares, transaction_type, date) VALUES(?, ?, ?, ?, ?, ?, ?)",
                           user_id, symbol.upper(), stock["name"], stock["price"], shares, "sold", now)
                db.execute("UPDATE users SET cash = ? WHERE id = ?", newbalance, user_id)
                return redirect("/")
            else:
                db.execute("INSERT INTO transactions (user_id, symbol, stock_name, price, shares, date) VALUES(?, ?, ?, ?, ?, ?)",
                           user_id, symbol.upper(), stock["name"], stock["price"], new_shares, now)
                db.execute("INSERT INTO history (user_id, symbol, stock_name, price, shares, transaction_type, date) VALUES(?, ?, ?, ?, ?, ?, ?)",
                           user_id, symbol.upper(), stock["name"], stock["price"], shares, "sold", now)
                db.execute("UPDATE users SET cash = ? WHERE id = ?", newbalance, user_id)
                return redirect("/")