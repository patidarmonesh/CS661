import vtk

# Loading 3D data
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("Isabel_3D.vti")
reader.Update()

#Create colour transfer function
colours = vtk.vtkColorTransferFunction()
colours.AddRGBPoint(-4931.54, 0, 1, 1)
colours.AddRGBPoint(-2508.95, 0, 0, 1)
colours.AddRGBPoint(-1873.9, 0, 0, 0.5)
colours.AddRGBPoint(-1027.16, 1, 0, 0)
colours.AddRGBPoint(-298.031, 1, 0.4, 0)
colours.AddRGBPoint(2594.97, 1, 1, 0)

# Create opacity transfer function
Opacity = vtk.vtkPiecewiseFunction()
Opacity.AddPoint(-4931.54, 1.0)
Opacity.AddPoint(101.815, 0.002)
Opacity.AddPoint(2594.97, 0.0)

# Create volume property
volume_property = vtk.vtkVolumeProperty()
volume_property.SetColor(colours)
volume_property.SetScalarOpacity(Opacity)

# Create volume mapper
volume_mapper = vtk.vtkSmartVolumeMapper()
volume_mapper.SetInputConnection(reader.GetOutputPort())

# Create volume
volume = vtk.vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Add outline to volume
outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)

# Create renderer and render window
renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(1000, 1000)

# Create render window interactor
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

renderer.AddVolume(volume)
renderer.AddActor(outline_actor)

# Taking input from user for Phong Shading
use_phong_shading = input("Do you want to use Phong shading? (yes/no): ").lower()

if use_phong_shading == "yes":
    volume_property.ShadeOn()
    volume_property.SetAmbient(0.5)
    volume_property.SetDiffuse(0.5)
    volume_property.SetSpecular(0.5)

# Render
render_window.Render()
render_window_interactor.Start()
