Attribute VB_Name = "Tool_eraseCustomStyles"
Option Explicit
Sub eraseCustomStyles()
'------------------------------------------------------------------------------
' eraseCustomStyles
'
' Description:
'   Deletes custom styles from the active document.
'
' Inputs:
'   None
'
' Outputs:
'   None
'
' Remarks:
'   This subroutine is used to remove specific custom styles from the active document.
'   The styles "New_normal", "Text_body", "Title_non_numbered", "Title_out_of_TOC"
'   and "Title_1" through "Title_5" are deleted if they exist in the document's styles collection.
'
'   Error handling is used to ensure that if any of the styles do not exist, the code will
'   continue execution without throwing an error.
'
' Source
'   https://github.com/eu-cristofer/reusable-components
'
'------------------------------------------------------------------------------
    
    ' Suppress error messages temporarily
    On Error Resume Next
    
    ' Delete specified custom styles
    ActiveDocument.Styles("New_normal").Delete
    ActiveDocument.Styles("Text_body").Delete
    ActiveDocument.Styles("Title_unnumbered").Delete
    ActiveDocument.Styles("Title_outside_TOC").Delete
    
    ' Delete custom title styles "Title_1" through "Title_5"
    Dim intLoop As Integer
    For intLoop = 1 To 5
        ActiveDocument.Styles("Title" & "_" & intLoop).Delete
    Next intLoop
    
    ' Re-enable error messages
    On Error GoTo 0
    
End Sub

