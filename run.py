from psidash.psidash import load_app

app = load_app(__name__, 'kamodo-dashboard.yaml')

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8060, debug=True)
