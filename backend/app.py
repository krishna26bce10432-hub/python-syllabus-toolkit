from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from algorithms import *

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"
app = Flask(__name__, static_folder=str(FRONTEND), static_url_path="")

@app.get("/")
def home():
    return send_from_directory(FRONTEND, "index.html")

@app.get("/api/health")
def health():
    return jsonify(ok=True, message="Python backend is connected")

@app.post("/api/run")
def run_algorithm():
    try:
        data=request.get_json(silent=True) or {}
        op=data.get("operation"); a=data.get("args") or {}
        n=lambda k,t=int:t(a[k])
        if op=="factorial": result=factorial(n("n"))
        elif op=="fibonacci": result=fibonacci(n("n"))
        elif op=="fibonacci_sequence": result=fibonacci_sequence(n("n"))
        elif op=="sum_average": result=sum_and_average([float(x) for x in a["numbers"]])
        elif op=="reverse": result=reverse_number(n("n"))
        elif op=="count_digits": result=count_digits(n("n"))
        elif op=="gcd": result=gcd(n("a"),n("b"))
        elif op=="base_conversion": result=base_conversion(n("n"),n("base"))
        elif op=="smallest_divisor": result=smallest_divisor(n("n"))
        elif op=="is_prime": result=is_prime(n("n"))
        elif op=="generate_primes": result=generate_primes(n("limit"))
        elif op=="prime_factors": result=prime_factors(n("n"))
        elif op=="sqrt_newton": result=square_root_newton(float(a["n"]))
        elif op=="sqrt_repeated": result=square_root_repeated_subtraction(n("n"))
        elif op=="sqrt_long": result=square_root_long_division(n("n"))
        elif op=="swap_temp": result=swap_with_temp(float(a["a"]),float(a["b"]))
        elif op=="swap_no_temp": result=swap_without_temp(float(a["a"]),float(a["b"]))
        elif op=="large_power": result=large_power(n("base"),n("exponent"))
        elif op=="pseudo_random": result=pseudo_random_number(n("seed"),n("low"),n("high"))
        elif op=="random_float": result=random_float(float(a["low"]),float(a["high"]))
        elif op=="control":
            mode=a.get("mode","if"); x=n("n")
            if mode=="if": result="Positive" if x>0 else "Condition is false"
            elif mode=="if_else": result="Even" if x%2==0 else "Odd"
            elif mode=="while": result=list(range(1,min(max(x,0),20)+1))
            elif mode=="for": result=list(range(1,min(max(x,0),20)+1))
            elif mode=="break": result=list(range(1,min(max(x-1,0),20)+1))
            elif mode=="continue": result=[i for i in range(1,21) if i!=x]
            elif mode=="pass": result="pass executed"
            else: raise ValueError("Unknown control mode")
        else: raise ValueError("Unknown operation")
        return jsonify(ok=True,operation=op,result=result)
    except Exception as e:
        return jsonify(ok=False,error=str(e)),400

@app.get("/<path:path>")
def files(path):
    p=FRONTEND/path
    if p.is_file(): return send_from_directory(FRONTEND,path)
    return send_from_directory(FRONTEND,"index.html")

if __name__=="__main__":
    print("Open http://127.0.0.1:5000")
    app.run(host="127.0.0.1",port=5000,debug=False)
