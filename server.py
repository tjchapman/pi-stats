from flask import Flask, jsonify, render_template
import psutil 
import os

app = Flask(__name__)

def get_cpu_temp():
    try:
        # use vcgencmd for CPU temp - native to Pi 
        temp = os.popen('vcgencmd measure_temp').readline()
        return float(temp.replace("temp=", "").replace("'C\n", ""))
    except Exception as e:
        return None  

@app.route('/stats', methods=['GET'])
def stats():
    stats = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "per_cpu_percent": psutil.cpu_percent(interval=1, percpu=True),  
        "memory_percent": psutil.virtual_memory().percent,
        "cpu_temp": get_cpu_temp(),
        "num_processes": len(psutil.pids())
    }

    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'cpu_percent': proc.info['cpu_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass 

    top_processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:10]

    stats['top_processes'] = top_processes

    return jsonify(stats)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)


