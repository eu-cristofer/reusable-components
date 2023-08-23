Attribute VB_Name = "Tool_reducePriority"
Option Explicit
Sub reducePriority()
    '------------------------------------------------------------------------------
    ' reducePriority
    '
    ' Description:
    '   Decreases the priority of styles in the active document based on a threshold.
    '   Styles with a priority lower than 50 are adjusted by adding 50 to their priority.
    '   The goal of this procedure is to list the custom styles first into the gallery
    '
    ' Inputs:
    '   None
    '
    ' Outputs:
    '   None
    '
    ' Remarks:
    '   This subroutine iterates through all the styles in the active document and
    '   adjusts the priority of styles that have a priority lower than 50.
    '
    ' Source:
    '   https://github.com/eu-cristofer/reusable-components
    '
    '------------------------------------------------------------------------------
    Dim oStyles As Styles
    Dim Style As Style
    
    ' Get a reference to the styles collection of the active document
    Set oStyles = Application.ActiveDocument.Styles
    
    ' Iterate through each style in the styles collection
    For Each Style In oStyles
        ' Check if the style's priority is below 50
        If Style.Priority < 50 Then
            ' Increase the priority index of the style by adding 50
            Style.Priority = (Style.Priority + 50)
        End If
    Next Style

End Sub
