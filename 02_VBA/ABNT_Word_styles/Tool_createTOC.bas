Attribute VB_Name = "Tool_createTOC"
Option Explicit
Sub createTOC(Optional level As Integer = 4)
    '------------------------------------------------------------------------------
    'addTOC
    '
    ' Description:
    '   Creates a table of contents based on specified styles and headings in the active document.
    '   The table of contents is generated at the specified range and includes headings within
    '   the defined heading level range.
    '
    ' Inputs:
    '   None
    '
    ' Outputs:
    '   None
    '
    ' Remarks:
    '   This subroutine should be executed to add a table of contents to the active document.
    '
    ' Source
    '   https://github.com/eu-cristofer/reusable-components
    '
    '------------------------------------------------------------------------------
  
    ' Declare variables
    Dim myRange As Range
    Dim stylesList As String
    Dim intLoop As Integer
    
    ' Set the range for which the table of contents will be generated
    ' Comment: Modify the range as needed. Currently set to the user's selection.
    Set myRange = Selection.Range
    
    ' Initialize the styles list with the first style
    stylesList = "Title_unnumbered,1"
    
    ' Generate styles list for table of contents
    For intLoop = 1 To level
        stylesList = stylesList & ", Title" & "_" & intLoop & "," & intLoop
        
        ' Configure the table of contents styles based on the loop counter
        With ActiveDocument.Styles("TOC " & intLoop)
            .AutomaticallyUpdate = True
            .BaseStyle = "New_normal"
            .NextParagraphStyle = "New_normal"
            
            ' Apply font formatting based on the loop counter
            Select Case intLoop
                Case 1
                    .font.AllCaps = True
                    .font.Bold = True
                Case 2
                    .font.AllCaps = True
                    .font.Bold = False
                Case 3
                    .font.AllCaps = False
                    .font.Bold = False
                Case 4
                    .font.AllCaps = False
                    .font.Bold = False
                    .font.Size = 11
            End Select
        End With
    Next intLoop
    
    ' Add the table of contents to the document
    ActiveDocument.TablesOfContents.Add _
        Range:=myRange, _
        UseFields:=False, _
        UseHeadingStyles:=True, _
        LowerHeadingLevel:=4, _
        UpperHeadingLevel:=1, _
        AddedStyles:=stylesList
End Sub
    
