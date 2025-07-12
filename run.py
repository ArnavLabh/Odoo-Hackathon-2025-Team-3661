from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("Flask app created successfully!")
    print("SQLite database should be created as 'skillswap.db' in the project directory.")
    print("Starting development server...")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
