Attribute VB_Name = "Tool_addTOC"
Option Explicit
Sub addTOC()
    Dim UserForm As Object
    Set UserForm = New selectTOCLevel
    UserForm.Show
End Sub
