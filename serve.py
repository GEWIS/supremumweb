from app import create_app, config

app = create_app(config.dev_config)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, use_reloader=True, debug=True)
