Attribute VB_Name = "Tool_exportModules"
Sub exportModules()
    '---------------------------------------------------------------------------
    ' Sub exportModules
    '
    ' Description:
    '   This subroutine exports VBA modules from a workbook/document to individual files
    '   in a specified folder and creates a list of exported module names.
    '
    ' Usage:
    '   Run this subroutine to export modules and create a module list text file.
    '
    ' Source
    '   https://github.com/eu-cristofer/reusable-components
    '---------------------------------------------------------------------------
    
    Dim exportFolder As String
    Dim moduleName As String
    Dim moduleText As String
    Dim moduleListText As String
    Dim moduleListFileName As String
    Dim moduleCount As Long
    Dim module As Object ' Reference to a module object
    Dim dialog As FileDialog
    
    ' Show folder selection dialog to choose the export location
    Set dialog = Application.FileDialog(msoFileDialogFolderPicker)
    If dialog.Show = -1 Then
        exportFolder = dialog.SelectedItems(1)
    Else
        MsgBox "No folder selected. Exiting."
        Exit Sub
    End If
    
    ' Create the module list text file
    moduleListFileName = exportFolder & "\00_module_list.txt"
    Open moduleListFileName For Output As #1
    
    ' Loop through each module in the workbook/document
    For Each module In ActiveDocument.VBProject.VBComponents
        moduleName = module.Name
        
        ' Determine the file extension based on the component type
        Dim fileExtension As String
        Select Case module.Type
            Case 1 ' vext_ct_StdModule
                fileExtension = ".bas"
            Case 2 ' vext_ct_ClassModule
                fileExtension = ".cls"
            Case 3 ' vbext_ct_MSForm
                fileExtension = ".frm"
            Case Else
                fileExtension = ".txt" ' Default extension for unknown types
        End Select
        
        ' Export the module to a file
        Dim check1 As Boolean
        Dim check2 As Boolean
        Dim check3 As Boolean
        
        check1 = module.Type <> 100
        check2 = module.Name <> "Tool_exportModules"
        check3 = module.Name <> "Tool_importModules"
        If check1 And check2 And check3 Then
            module.Export exportFolder & Application.PathSeparator & moduleName & fileExtension
            
            ' Append module name to the module list
            moduleListText = moduleListText & moduleName & fileExtension & vbNewLine
            moduleCount = moduleCount + 1
        End If
    
    Next module
    
    ' Write module list to the text file
    Print #1, moduleListText
    Close #1
    
    ' Display a completion message with module count and list location
    MsgBox moduleCount & " modules exported to " & exportFolder & ". Module list saved as " & moduleListFileName, vbInformation
End Sub

