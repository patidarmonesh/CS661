# CS661-Assignment-1

# Isocontour Extraction & VTK Volume Rendering

**Question-1 (IsoContour)**

**Purpose**
Extract a contour line at a specified isovalue from `Isabel_2D.vti` and output a `.vtp` file.

**Files**

- `extract_contour.py` : Python script
- `Isabel_2D.vti` : Input data
- `contour.vtp` : Output contour (will be generated)

**Requirements**

- Python 3.x
- VTK Python bindings

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

**Question-2 (VTK Volume Rendering and Transfer Function)**

**Objective**
This Python script performs volume rendering of 3D scalar data using the VTK library. It includes:
Ray-casting using vtkSmartVolumeMapper
Custom color and opacity transfer functions
Optional Phong shading for realistic lighting
1000x1000 resolution rendering window
An outline around the volume using vtkOutlineFilter

**Input**
A VTK XML image data file: 'Isabel_3D.vti'

**How to Run**
In a terminal,go to the address of directory containing the file volume_rendering.py
and run-
`python volume_rendering.py`

You’ll be prompted:
Do you want to use Phong shading? (yes/no):
Enter yes to apply realistic lighting, or no to skip it.

#Group- Monesh Patidar, Ishita Mangal, Smruti Paramita Sahoo
#Course: [CS661 / Soumya Dutta]
