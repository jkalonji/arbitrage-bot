
# On publie les résultats sur l'url locale

from flask import Flask
import time


app = Flask(__name__)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    print('méthode shutdown')
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if shutdown is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    else:
        shutdown()



@app.route("/")
def test():
    result = {"doubleSwapOutputNatToSynth2": doubleSwapOutputNatToSynth,
           "doubleSwapOutputSynthToNat" : doubleSwapOutputSynthToNat}
    return result
    time.sleep(10)
    res = requests.post('http://localhost:5001/shutdown')
    res.text
        




if __name__ == "__main__":
    
    app.run(host='0.0.0.0', threaded=True, port=5001)
    # wait 5s
    # then shutdown
    
