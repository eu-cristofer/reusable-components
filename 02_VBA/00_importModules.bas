Attribute VB_Name = "Tool_importModules"
Option Explicit

Sub ImportModules()
    '---------------------------------------------------------------------------
    ' Sub importModules
    '
    ' Description:
    '   This function import the modules from a user selected folder. The
    '   modules to import shall be listed the into a text file named "00_module_list.txt"
    '   located into the same selected folder.
    '
    ' Usage:
    '   Run this subroutine to export modules and create a module list text file.
    '
    ' Source
    '   https://github.com/eu-cristofer/reusable-components
    '---------------------------------------------------------------------------
    

    ' Open the folder selection dialog
    Dim selectedFolder As FileDialog
    Set selectedFolder = Application.FileDialog(msoFileDialogFolderPicker)
    selectedFolder.Title = "Select the modules folder"
    
    ' Check if the user clicked OK
    If selectedFolder.Show = -1 Then
        Dim folderPath As String
        folderPath = selectedFolder.SelectedItems(1)
        
        ' Specify the path to the text file containing module names
        Dim txtFilePath As String
        txtFilePath = folderPath & "\00_module_list.txt"
        
        ' Check if the text file exists
        If Dir(txtFilePath) <> "" Then
            ' Read the content of the text file
            Dim txtFileContent As String
            Open txtFilePath For Input As #1
            txtFileContent = Input$(LOF(1), 1)
            Debug.Print txtFileContent
            Close #1
            
            ' Split the content into an array of module names
            Dim moduleNames() As String
            moduleNames = Split(txtFileContent, vbCrLf)
            
            ' Import each module
            Dim moduleName As String
            Dim i As Long
            For i = LBound(moduleNames) To UBound(moduleNames)
                moduleName = Trim(moduleNames(i))
                If moduleName <> "" Then
                    ImportModuleFromFile folderPath & "\" & moduleName
                End If
            Next i
        Else
            MsgBox "Text file 'module_list.txt' not found in the selected folder.", vbExclamation
        End If
    Else
        MsgBox "Try again. Pick a folder and click OK"
    End If
End Sub

Private Sub ImportModuleFromFile(ByRef filePath As String)
    
    Dim vbComp As Object
    ' Check if the module file exists
    If Dir(filePath) <> "" Then
        ' Import the module
        Set vbComp = ActiveDocument.VBProject.VBComponents.Import(filePath)
    Else
        MsgBox "Module file not found: " & filePath, vbExclamation
    End If
End Sub