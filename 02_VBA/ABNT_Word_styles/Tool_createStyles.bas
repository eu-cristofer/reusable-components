Attribute VB_Name = "Tool_createStyles"
Option Explicit

Function createFontSizeName( _
    ByVal styleName As String, _
    Optional ByRef fontSize As Integer = 12, _
    Optional ByRef fontName As String = "Arial" _
    )
    '------------------------------------------------------------------------------
    ' createFontSizeName
    '
    ' Description:
    '   Creates a new paragraph style with specified font size and font name settings.
    '
    ' Inputs:
    '   styleName - Name of the new style to be created.
    '   fontSize  - (Optional) Font size for the style (default: 12).
    '   fontName  - (Optional) Font name for the style (default: "Arial").
    '
    ' Outputs:
    '   None
    '
    ' Remarks:
    '   This subroutine creates a new paragraph style in the active document. The style
    '   is based on "No Spacing" with the specified font size and font name settings.
    '
    ' Source:
    '   https://github.com/eu-cristofer/reusable-components
    '------------------------------------------------------------------------------

    ' Constants
    Const BASE_STYLE As String = "No Spacing"
    Const LANG_ID_ENGLISH As Integer = 1033
    
    ' Get a reference to the styles collection of the active document
    Dim oStyles As Styles
    Set oStyles = Application.ActiveDocument.Styles
    
    ' Add a new style to the collection
    oStyles.Add Name:=styleName, Type:=wdStyleTypeParagraph
    
    ' Configure the new style
    With oStyles(styleName)
        .BaseStyle = BASE_STYLE
        .QuickStyle = True
        .UnhideWhenUsed = False
        .Visibility = False
        .Priority = 1
        .LanguageID = LANG_ID_ENGLISH
        .AutomaticallyUpdate = True
        
        ' Configure font settings
        With .font
            .Name = fontName
            .Size = fontSize
        End With
    End With
End Function


Function createBody( _
    ByVal styleName As String, _
    Optional ByRef fontSize As Integer = 12, _
    Optional ByRef fontName As String = "Arial" _
    )
    '------------------------------------------------------------------------------
    ' createBody
    '
    ' Description:
    '   Creates a new body style for paragraphs with specified font size and font name settings.
    '
    ' Inputs:
    '   styleName - Name of the new style to be created.
    '   fontSize  - (Optional) Font size for the style (default: 12).
    '   fontName  - (Optional) Font name for the style (default: "Arial").
    '
    ' Outputs:
    '   None
    '
    ' Remarks:
    '   This subroutine creates a new body style for paragraphs in the active document.
    '   The style inherits settings from createFontSizeName and adds paragraph alignment,
    '   line spacing, and space after settings.
    '
    ' Source:
    '   https://github.com/eu-cristofer/reusable-components
    '------------------------------------------------------------------------------

    ' Constants
    Const NEXT_STYLE As String = "Text_body"
    ' Note that 1 line is equal to 12 points in Word
    Const LINE_SPACING As Single = 1.5              ' Adjust as needed
    Const SPACE_AFTER As Single = 1                 ' Adjust as needed
    
    ' Create the font size style with given parameters
    Call createFontSizeName(styleName, fontSize, fontName)

    With Application.ActiveDocument.Styles(styleName)
        ' Set the following paragraph style
        .NextParagraphStyle = NEXT_STYLE
        
        With .paragraphFormat
            ' Set paragraph alignment using enumerated constant
            .Alignment = wdAlignParagraphJustify
            
            ' Set line spacing and space after
            .LineSpacing = LinesToPoints(LINE_SPACING)
            .spaceAfter = LinesToPoints(SPACE_AFTER)
        End With
    End With
End Function


Function createUnnumberedTitle( _
    ByVal styleName As String, _
    Optional ByRef fontSize As Integer = 12, _
    Optional ByRef fontName As String = "Arial" _
    )
    '------------------------------------------------------------------------------
    ' createUnnumberedTitle
    '
    ' Description:
    '   Creates a new unnumbered title style with specified font size and font name settings.
    '
    ' Inputs:
    '   styleName - Name of the new style to be created.
    '   fontSize  - (Optional) Font size for the style (default: 12).
    '   fontName  - (Optional) Font name for the style (default: "Arial").
    '
    ' Outputs:
    '   None
    '
    ' Remarks:
    '   This subroutine creates a new unnumbered title style in the active document.
    '   The style inherits settings from createBody and adds bold, all-caps font settings,
    '   paragraph alignment, and space before/after settings.
    '
    ' Source:
    '   https://github.com/eu-cristofer/reusable-components
    '------------------------------------------------------------------------------

    ' Constants
    Const NEW_PRIORITY As Integer = 2
    Const SPACE_BEFORE As Single = 2
    Const SPACE_AFTER As Single = 2
    
    Call createBody(styleName, fontSize, fontName)

    With Application.ActiveDocument.Styles(styleName)
        .Priority = NEW_PRIORITY
        
        ' Configure font settings
        With .font
            .Bold = True
            .AllCaps = True
        End With
        
        ' Configure paragraph format settings
        With .paragraphFormat
            .Alignment = wdAlignParagraphLeft
            .spaceBefore = LinesToPoints(SPACE_BEFORE)
            .spaceAfter = LinesToPoints(SPACE_AFTER)
        End With
    End With
End Function


Function createNumberedTitle( _
    ByVal styleName As String, _
    Optional ByRef fontSize As Integer = 12, _
    Optional ByRef fontName As String = "Arial" _
    )
    '------------------------------------------------------------------------------
    ' createNumberedTitle
    '
    ' Description:
    '   Creates a new numbered title style along with variations.
    '
    ' Inputs:
    '   styleName - Base name of the new styles to be created.
    '   fontSize  - (Optional) Font size for the styles (default: 12).
    '   fontName  - (Optional) Font name for the styles (default: "Arial").
    '
    ' Outputs:
    '   None
    '
    ' Remarks:
    '   This subroutine creates a new numbered title style along with variations
    '   based on the specified base name. Each variation adjusts settings like
    '   space before/after, boldness, and all-caps formatting.
    '
    ' Source:
    '   https://github.com/eu-cristofer/reusable-components
    '------------------------------------------------------------------------------
   
    Dim strFormat As String
    strFormat = ""
    
    Dim intLoop As Integer
    
    For intLoop = 1 To 5
        ' Use the same settings of unnumbered title, level 1
        Call createUnnumberedTitle(styleName & "_" & intLoop, fontSize, fontName)
        
        With ActiveDocument.Styles(styleName & "_" & intLoop)
            .Priority = 3
 
            Select Case intLoop
            
                Case 1
                    ' Configure paragraph format settings
                    With .paragraphFormat
                        .LineSpacing = LinesToPoints(1.5)
                        .spaceBefore = LinesToPoints(2)
                        .spaceAfter = LinesToPoints(2)
                    End With
                
                Case 2
                    ' Configure paragraph format settings
                    With .paragraphFormat
                        .LineSpacing = LinesToPoints(1)
                        .spaceBefore = LinesToPoints(2)
                        .spaceAfter = LinesToPoints(2)
                    End With
                                
                Case 3
                    ' Configure paragraph format settings
                    With .paragraphFormat
                        .LineSpacing = LinesToPoints(1)
                        .spaceBefore = LinesToPoints(1.5)
                        .spaceAfter = LinesToPoints(1)
                    End With
                    
                    ' Configure font settings
                    With .font
                        .Bold = False
                        .AllCaps = True
                    End With
                                
                Case 4
                    ' Configure paragraph format settings
                    With .paragraphFormat
                        .LineSpacing = LinesToPoints(1)
                        .spaceBefore = LinesToPoints(1.5)
                        .spaceAfter = LinesToPoints(1)
                    End With
                    
                    ' Configure font settings
                    With .font
                        .Bold = True
                        .AllCaps = False
                    End With
                    
                Case 5
                    ' Configure paragraph format settings
                    With .paragraphFormat
                        .LineSpacing = LinesToPoints(1)
                        .spaceBefore = LinesToPoints(1.5)
                        .spaceAfter = LinesToPoints(1)
                    End With
                    
                    ' Configure font settings
                    With .font
                        .Bold = False
                        .AllCaps = False
                    End With
            End Select
        End With
    Next intLoop
End Function


