"""Research-only IMU classifier. Synthetic labels do not establish real handling."""
from dataclasses import dataclass
from typing import List
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

LABELS = {0: "IDLE", 1: "ACCIDENTAL_BUMP", 2: "PHONE_HANDLING_PATTERN"}
SAMPLES = 100
HZ = 50

@dataclass(frozen=True)
class MotionWindow:
    accel_x: np.ndarray
    accel_y: np.ndarray
    accel_z: np.ndarray
    gyro_x: np.ndarray
    gyro_y: np.ndarray
    gyro_z: np.ndarray

def extract_features(w: MotionWindow):
    axes = [np.asarray(getattr(w, k), dtype=float) for k in
            ("accel_x","accel_y","accel_z","gyro_x","gyro_y","gyro_z")]
    if any(a.shape != (SAMPLES,) or not np.all(np.isfinite(a)) for a in axes):
        raise ValueError("Expected six finite 100-sample axes")
    a = np.sqrt(sum(x*x for x in axes[:3]))
    g = np.sqrt(sum(x*x for x in axes[3:]))
    # Remove DC/gravity-dominated baseline before estimating dynamic energy.
    dynamic = a - np.mean(a)
    spectral = np.abs(np.fft.rfft(dynamic))**2 / SAMPLES**2
    frequencies = np.fft.rfftfreq(SAMPLES, d=1/HZ)
    band = float(spectral[(frequencies >= 1) & (frequencies <= 10)].sum())
    return np.array([a.mean(),a.std(),a.max(),np.ptp(a),
                     g.mean(),g.std(),g.max(),np.mean(a>11.5),
                     np.mean(dynamic**2),np.mean(g**2),band],dtype=float)

def generate_synthetic_data(n_per_class=200, seed=20261021):
    """Deliberately simplified simulator. No empirical claim about human behavior."""
    rng=np.random.default_rng(seed)
    windows=[]; labels=[]; groups=[]
    for i in range(n_per_class):
        for cls in range(3):
            ax=rng.normal(0,.05,SAMPLES)
            ay=rng.normal(0,.05,SAMPLES)
            az=rng.normal(9.81,.05,SAMPLES)
            gx=rng.normal(0,.01,SAMPLES)
            gy=rng.normal(0,.01,SAMPLES)
            gz=rng.normal(0,.01,SAMPLES)
            if cls==1:
                start=int(rng.integers(20,75))
                az[start:start+10]+=rng.uniform(8,15,10)
                gx+=rng.normal(0,.02,SAMPLES)
            elif cls==2:
                ax=rng.normal(2.5,1.2,SAMPLES)
                ay=rng.normal(3,1.5,SAMPLES)
                az=rng.normal(8,2,SAMPLES)
                gx=rng.normal(1.2,.8,SAMPLES)
                gy=rng.normal(1.5,.9,SAMPLES)
                gz=rng.normal(.8,.5,SAMPLES)
            windows.append(MotionWindow(ax,ay,az,gx,gy,gz))
            labels.append(cls)
            groups.append(i) # synthetic generator iteration; not a participant identifier
    return windows,np.array(labels),np.array(groups)

class PhoneHandlingClassifier:
    def __init__(self):
        base=RandomForestClassifier(n_estimators=100,max_depth=8,random_state=42)
        self.model=CalibratedClassifierCV(base,method="sigmoid",cv=3)
        self.trained=False
    def train(self,windows: List[MotionWindow],labels):
        y=np.asarray(labels)
        if len(set(y))<3: raise ValueError("Need all three classes for calibration")
        self.model.fit(np.stack([extract_features(w) for w in windows]),y)
        self.trained=True
    def classify_event(self,window):
        if not self.trained: raise RuntimeError("Model is not trained")
        p=self.model.predict_proba(extract_features(window).reshape(1,-1))[0]
        index=int(np.argmax(p))
        return LABELS[int(self.model.classes_[index])],float(p[index])

def demo():
    windows,y,_=generate_synthetic_data()
    train_idx,test_idx=train_test_split(np.arange(len(y)),test_size=.3,
                                        random_state=42,stratify=y)
    clf=PhoneHandlingClassifier()
    clf.train([windows[i] for i in train_idx],y[train_idx])
    pred=clf.model.predict(np.stack([extract_features(windows[i]) for i in test_idx]))
    print("SYNTHETIC SIMULATION ONLY — NOT FIELD VALIDATION")
    print(classification_report(y[test_idx],pred,labels=[0,1,2],target_names=list(LABELS.values()),zero_division=0))
    print("Confusion matrix:",confusion_matrix(y[test_idx],pred,labels=[0,1,2]).tolist())
    print("Example:",clf.classify_event(windows[test_idx[0]]))
if __name__=="__main__": demo()
