# Parkinson detector

An Ensemble of CNN Models for Parkinson’s Disease Detection

Medical support tool for fast preliminary diagnosis can be used by any medical personnel.  Parkinson detector is written in Python and runs in a normal Windows and Linux environment. The user interface was implemented using the Qt library. 

Our application can work directly with Dicom files (.dcm) from a digital CRT machine or with any image files (jpg, png, etc.). We make a simple user interface with drag-and-drop support.

**Note:** prediction from the application cannot be used as a medical diagnosis.
## Application requirements: 

* Operational system: 
    * Windows 7 or later
    * Ubuntu 16.04 or later
    * Mac OS 10.12.6 (Sierra) or later (64-bit) (no GPU support)
* Python 3.6 or later
* Hard Drive: 4Gb of free space,
* Processor: Intel Core i3,
* Memory (RAM): 3Gb or above free.
* Internet connection: wideband connection for first use (for neural network model downloading)
* Admin privileges are not a requirement

## Run without instalation

### Requirements instalation
```
git clone https://gitlab.com/digiratory/biomedimaging/parkinson-detector.git
cd parkinson-detector
pip install -r requirements.txt
```

### Application starting
```
cd parkinson-detector
python run.pyw
```

## Instalation over pip

```
pip install parkinson-detector
```

For starting application run the follow command:

```
parkinson-detector-app
```
