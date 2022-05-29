import vtkmodules.all as vtk
def resampleext(sourcepath,resamplepath,name):
    r = vtk.vtkCGNSReader()
    r.SetFileName(sourcepath)
    r.Update()
    r.EnableAllCellArrays()

    stl = vtk.vtkSTLReader()
    stl.SetFileName(resamplepath)
    stl.Update()

    g = vtk.vtkCompositeDataGeometryFilter()
    g.SetInputConnection(r.GetOutputPort())
    g.Update()

    resample = vtk.vtkResampleWithDataSet()
    resample.SetInputData(stl.GetOutput())
    resample.SetSourceConnection(g.GetOutputPort())
    resample.Update()

    lut = vtk.vtkLookupTable()
    lut.SetHueRange(0.667, 0)
    lut.Build()

    scalars = resample.GetOutput().GetPointData().GetArray(name).GetRange()

    Mapper = vtk.vtkPolyDataMapper()
    Mapper.SetInputConnection(resample.GetOutputPort())
    Mapper.SetScalarModeToUsePointFieldData()
    Mapper.SelectColorArray(name)
    Mapper.SetScalarRange(scalars)
    Mapper.SetLookupTable(lut)
    Actor = vtk.vtkActor()
    Actor.SetMapper(Mapper)

    legendBar = vtk.vtkScalarBarActor()
    legendBar.SetOrientationToVertical()
    legendBar.SetLookupTable(lut)
    legenProp = vtk.vtkTextProperty()
    legenProp.SetColor(0, 0, 0)
    legenProp.SetFontSize(50)
    legenProp.SetFontFamilyToArial()
    legenProp.ItalicOff()
    legenProp.BoldOff()
    legendBar.UnconstrainedFontSizeOn()
    legendBar.SetTitleTextProperty(legenProp)
    legendBar.SetLabelTextProperty(legenProp)
    legendBar.SetLabelFormat("%5.2f")
    legendBar.SetTitle(name)


    Render = vtk.vtkRenderer()
    Render.GradientBackgroundOn()
    Render.SetBackground(1, 1, 1)
    Render.SetBackground2(1, 1, 1)
    Render.AddActor(Actor)
    Render.AddActor(legendBar)


    return Render


#CoefPressure,Density,Enthalpy,Mach,Pressure,Temperature,Velocity,VelocityMagnitude

sourcepath=r'.cgns'
resamplepath=r'.stl'
name='Pressure'
num=0
Render=resampleext(sourcepath,resamplepath,name)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(Render)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
renWin.SetSize(300, 300)
renWin.Render()
iren.Initialize()
iren.Start()