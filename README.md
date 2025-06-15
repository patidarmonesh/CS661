# CS661-Assignment-1
**Question-1 (IsoContour)**

**Purpose**
Extract a contour line at a specified isovalue from `Isabel_2D.vti` and output a `.vtp` file.

**Files**

* `extract_contour.py`  : Python script
* `Isabel_2D.vti`       : Input data
* `contour.vtp`         : Output contour (will be generated)

**Requirements**

* Python 3.x
* VTK Python bindings

Install VTK:

```
pip install vtk
```

**Usage**
In a terminal, run:

```
python extract_contour.py \
  --input Isabel_2D.vti \
  --isovalue <float> \
  --output contour.vtp
```

Replace `<float>` with a value between -1438 and 630.

**Visualize**
Load the generated `contour.vtp` in ParaView (or any VTK viewer) and adjust line color as needed.
