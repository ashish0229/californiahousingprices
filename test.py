import pickle

with open(r"C:\Users\somir\Desktop\regmodel.pkl", "rb") as f:
    regmodel = pickle.load(f)
print("Model type:", type(regmodel))

with open(r"C:\Users\somir\Desktop\scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
print("Scaler type:", type(scaler))
