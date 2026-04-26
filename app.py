import os
from flask import Flask, request, jsonify, render_template
from flask_caching import Cache
from api_client import ModAPI
from mod_state import ModState

app = Flask(__name__)

# Configure Caching (1-hour timeout is usually safe for mod versions)
cache = Cache(app, config={
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': 'cache-directory',
    'CACHE_DEFAULT_TIMEOUT': 3600 
})

api = ModAPI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_compatibility():
    data = request.json
    mod_requests = data.get('mods', [])
    
    mod_objects = []
    found_metadata = []
    not_found = []

    for m in mod_requests:
        identifier = m['id'].strip()
        
        # We cache the entire ModState object based on the identifier
        cache_key = f"{m['platform']}_{identifier}"
        state = cache.get(cache_key)
        
        if state is None:
            state = api.fetch_mod(m['platform'], identifier)
            # Only cache if we actually found versions
            if state.supported_configs:
                cache.set(cache_key, state)
        
        if state.supported_configs:
            mod_objects.append(state)
            # Metadata for the UI (slug and URL)
            found_metadata.append({
                "name": identifier,
                "url": f"https://modrinth.com/mod/{identifier}" if m['platform'] == 'modrinth' else "#"
            })
        else:
            not_found.append(identifier)
    
    best_configs, failed_mods = ModState.analyze_compatibility(mod_objects)
    sorted_configs = sorted(list(best_configs), key=lambda x: x[0], reverse=True)
    
    return jsonify({
        "recommended_configs": sorted_configs,
        "incompatible_mods": failed_mods,
        "found_mods": found_metadata,
        "not_found": not_found,
        "status": "Perfect Match" if not failed_mods and not not_found else "Partial Compatibility"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)