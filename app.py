from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>My Website</h1>
    <form method="POST" action="/submit">
        <input name="name" placeholder="Your Name" required>
        <br><br>
        <textarea name="message" placeholder="Your Message" required></textarea>
        <br><br>
        <button type="submit">Submit</button>
    </form>
    """

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    message = request.form.get("message")
    return "Thank you for your message!"

if __name__ == "__main__":
    app.run()
