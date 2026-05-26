from app import create_app
# from fakeData import main  <-- این را کامنت کنید

app = create_app()

if __name__ == "__main__":
    # main()  <-- این را هم کامنت کنید
    app.run(host="0.0.0.0", port=5000, debug=True)