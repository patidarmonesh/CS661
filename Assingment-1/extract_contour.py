#!/usr/bin/env python3

import argparse
import math
from vtkmodules.vtkIOXML import (
    vtkXMLImageDataReader,
    vtkXMLPolyDataWriter
)
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkPolyData,
    vtkCellArray
)


def parse_args():
    """
    Parse command-line arguments:
      -i / --input:   input .vti file path
      -v / --isovalue: contour scalar value (float)
      -o / --output:  output .vtp file path
    """
    parser = argparse.ArgumentParser(
        description="Extract a 2D isocontour from a VTI file"
    )
    parser.add_argument(
        "-i", "--input", required=True,
        help="Path to input .vti (e.g. Isabel_2D.vti)"
    )
    parser.add_argument(
        "-v", "--isovalue", type=float, required=True,
        help="Contour value (between -1438 and 630)"
    )
    parser.add_argument(
        "-o", "--output", required=True,
        help="Path to output .vtp"
    )
    return parser.parse_args()


def read_image(path):
    """
    Read a VTI (VTKImageData) file and return the image data.
    Warn if Z dimension is not 1 (expecting 2D slice).
    """
    reader = vtkXMLImageDataReader()
    reader.SetFileName(path)
    reader.Update()
    img = reader.GetOutput()
    dims = img.GetDimensions()
    if dims[2] != 1:
        print(f"Warning: Z dimension is {dims[2]}, expected 1 for a 2D slice.")
    return img


def cell_corner_point_ids(img, i, j):
    """
    Given cell indices (i,j), return the point IDs of its four corners in CCW order:
      0: bottom-left, 1: bottom-right, 2: top-right, 3: top-left
    """
    nx, ny, _ = img.GetDimensions()
    def pid(ii, jj):
        return jj * nx + ii
    return [
        pid(i,   j),   # bottom-left
        pid(i+1, j),   # bottom-right
        pid(i+1, j+1), # top-right
        pid(i,   j+1)  # top-left
    ]


def interpolate_if_straddle(pA, vA, pB, vB, iso):
    """
    If the scalar values vA and vB straddle the isovalue (one above, one below),
    compute the linear interpolation location along edge A->B.
    Return None if no crossing.
    """
    if (vA - iso) * (vB - iso) >= 0:
        return None
    t = (iso - vA) / (vB - vA)
    return [pA[k] + t * (pB[k] - pA[k]) for k in range(3)]


def extract_contour(img, iso):
    """
    Traverse each cell of the 2D image, find edge intersections with the isovalue,
    skip ambiguous (4-intersection) cases, and build line segments.
    Return as vtkPolyData.
    """
    scalars = img.GetPointData().GetScalars()
    pts = vtkPoints()
    lines = vtkCellArray()

    nx, ny, _ = img.GetDimensions()
    # Loop over each cell in the grid
    for j in range(ny - 1):
        for i in range(nx - 1):
            cids = cell_corner_point_ids(img, i, j)
            corners = [img.GetPoint(pid) for pid in cids]
            values = [scalars.GetTuple1(pid) for pid in cids]

            inter_pts = []
            # Check the 4 edges in CCW order: (0->1), (1->2), (2->3), (3->0)
            for idx in range(4):
                pA, pB = corners[idx], corners[(idx + 1) % 4]
                vA, vB = values[idx], values[(idx + 1) % 4]
                ip = interpolate_if_straddle(pA, vA, pB, vB, iso)
                if ip:
                    inter_pts.append(ip)

            # Need at least 2 intersections for a segment
            if len(inter_pts) < 2:
                continue
            # Skip ambiguous saddle cases (4 intersections)
            if len(inter_pts) == 4:
                continue

            # Order the intersection points around their centroid to connect properly
            cx = sum(p[0] for p in inter_pts) / len(inter_pts)
            cy = sum(p[1] for p in inter_pts) / len(inter_pts)
            angles = [math.atan2(p[1] - cy, p[0] - cx) for p in inter_pts]
            sorted_pts = [pt for _, pt in sorted(zip(angles, inter_pts))]

            # For two points, create one line segment
            a_id = pts.InsertNextPoint(sorted_pts[0])
            b_id = pts.InsertNextPoint(sorted_pts[1])
            lines.InsertNextCell(2)
            lines.InsertCellPoint(a_id)
            lines.InsertCellPoint(b_id)

    # Assemble into polydata
    poly = vtkPolyData()
    poly.SetPoints(pts)
    poly.SetLines(lines)
    return poly


def main():
    args = parse_args()
    img = read_image(args.input)
    poly = extract_contour(img, args.isovalue)

    # Write out binary .vtp to save space
    writer = vtkXMLPolyDataWriter()
    writer.SetFileName(args.output)
    writer.SetInputData(poly)
    writer.SetDataModeToBinary()
    writer.Write()
    print(f"Contour at {args.isovalue} written to {args.output}")


if __name__ == "__main__":
    main()
