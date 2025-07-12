from app import create_app

app = create_app()

# List all routes
for rule in app.url_map.iter_rules():
    if 'public_profile' in rule.rule:
        print(f"Route: {rule.rule}, Methods: {rule.methods}, Endpoint: {rule.endpoint}")
