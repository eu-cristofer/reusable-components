Attribute VB_Name = "Tool_ListPrintInfo"
Option Explicit
Sub listPrintInfo()

    Set oStyles = Application.ActiveDocument.Styles
    
    With oStyles("No Spacing")
        Debug.Print "Auto Update:", .AutomaticallyUpdate
        Debug.Print "BaseStyle:", .BaseStyle
        'Debug.Print .Borders
        Debug.Print "Builtin:", .BuiltIn
        Debug.Print "Description:", .Description
        
        Debug.Print Chr(10) & "Font"
        With .font
            Debug.Print "AllCaps", .AllCaps
            Debug.Print "Bold", .Bold
            Debug.Print "BoldBi", .BoldBi
            'Debug.Print "Borders", .Borders
            Debug.Print "ColorIndex", .ColorIndex
            Debug.Print "ColorIndexBi", .ColorIndexBi
            Debug.Print "ContextualAlternates", .ContextualAlternates
            Debug.Print "DiacriticColor", .DiacriticColor
            Debug.Print "DisableCharacterSpaceGrid", .DisableCharacterSpaceGrid
            Debug.Print "DoubleStrikeThrough", .DoubleStrikeThrough
            'Debug.Print "Duplicate", .Duplicate
            Debug.Print "Emboss", .Emboss
            Debug.Print "EmphasisMark", .EmphasisMark
            Debug.Print "Engrave", .Engrave
            'Debug.Print "Fill", .Fill
            'Debug.Print "Glow", .Glow
            Debug.Print "Hidden", .Hidden
            Debug.Print "Italic", .Italic
            Debug.Print "ItalicBi", .ItalicBi
            Debug.Print "Kerning", .Kerning
            Debug.Print "Ligatures", .Ligatures
            'Debug.Print "Line", .Line
            Debug.Print "Name", .Name
            Debug.Print "NameAscii", .NameAscii
            Debug.Print "NameBi", .NameBi
            Debug.Print "NameFarEast", .NameFarEast
            Debug.Print "NameOther", .NameOther
            Debug.Print "NumberForm", .NumberForm
            Debug.Print "NumberSpacing", .NumberSpacing
            Debug.Print "Outline", .Outline
            Debug.Print "Parent", .Parent
            Debug.Print "Position", .Position
            'Debug.Print "Reflection", .Reflection
            Debug.Print "Scaling", .Scaling
            'Debug.Print "Shading", .Shading
            Debug.Print "Shadow", .Shadow
            Debug.Print "Size", .Size
            Debug.Print "SizeBi", .SizeBi
            Debug.Print "SmallCaps", .SmallCaps
            Debug.Print "Spacing", .Spacing
            Debug.Print "StrikeThrough", .StrikeThrough
            Debug.Print "StylisticSet", .StylisticSet
            Debug.Print "Subscript", .Subscript
            Debug.Print "Superscript", .Superscript
            Debug.Print "TextColor", .TextColor
            'Debug.Print "TextShadow", .TextShadow
            'Debug.Print "ThreeD", .ThreeD
            Debug.Print "Underline", .Underline
            Debug.Print "UnderlineColor", .UnderlineColor
        End With

        'Debug.Print .Frame
        Debug.Print .InUse
        Debug.Print .LanguageID
        Debug.Print .LanguageIDFarEast
        Debug.Print .Linked
        Debug.Print "LinkStyle", .LinkStyle
        Debug.Print .ListLevelNumber
        'Debug.Print .ListTemplate
        Debug.Print .Locked
        Debug.Print .NameLocal
        Debug.Print .NextParagraphStyle
        Debug.Print .NoProofing
        Debug.Print .NoSpaceBetweenParagraphsOfSameStyle
        
        Debug.Print Chr(10) & "paragraph"
        With .paragraphFormat
            Debug.Print "AddSpaceBetweenFarEastAndAlpha", .AddSpaceBetweenFarEastAndAlpha
            Debug.Print "AddSpaceBetweenFarEastAndDigit", .AddSpaceBetweenFarEastAndDigit
            Debug.Print "Alignment", .Alignment
            Debug.Print "Application", .Application
            Debug.Print "AutoAdjustRightIndent", .AutoAdjustRightIndent
            Debug.Print "BaseLineAlignment", .BaseLineAlignment
            Debug.Print "CharacterUnitFirstLineIndent", .CharacterUnitFirstLineIndent
            Debug.Print "CharacterUnitLeftIndent", .CharacterUnitLeftIndent
            Debug.Print "CharacterUnitRightIndent", .CharacterUnitRightIndent
            Debug.Print "CollapsedByDefault", .CollapsedByDefault
            Debug.Print "Creator", .Creator
            Debug.Print "DisableLineHeightGrid", .DisableLineHeightGrid
            Debug.Print "FarEastLineBreakControl", .FarEastLineBreakControl
            Debug.Print "FirstLineIndent", .FirstLineIndent
            Debug.Print "HalfWidthPunctuationOnTopOfLine", .HalfWidthPunctuationOnTopOfLine
            Debug.Print "HangingPunctuation", .HangingPunctuation
            Debug.Print "Hyphenation", .Hyphenation
            Debug.Print "KeepTogether", .KeepTogether
            Debug.Print "KeepWithNext", .KeepWithNext
            Debug.Print "LeftIndent", .LeftIndent
            Debug.Print "LineSpacing", .LineSpacing
            Debug.Print "LineSpacingRule", .LineSpacingRule
            Debug.Print "LineUnitAfter", .LineUnitAfter
            Debug.Print "LineUnitBefore", .LineUnitBefore
            Debug.Print "MirrorIndents", .MirrorIndents
            Debug.Print "NoLineNumber", .NoLineNumber
            Debug.Print "OutlineLevel", .OutlineLevel
            Debug.Print "PageBreakBefore", .PageBreakBefore
            Debug.Print "Parent", .Parent
            Debug.Print "ReadingOrder", .ReadingOrder
            Debug.Print "RightIndent", .RightIndent
            'Debug.Print "Shading", .Shading
            Debug.Print "SpaceAfter", .spaceAfter
            Debug.Print "SpaceAfterAuto", .SpaceAfterAuto
            Debug.Print "SpaceBefore", .spaceBefore
            Debug.Print "SpaceBeforeAuto", .SpaceBeforeAuto
            'Debug.Print "Style", .Style
            'Debug.Print "TabStops", .TabStops
            Debug.Print "TextboxTightWrap", .TextboxTightWrap
            Debug.Print "WidowControl", .WidowControl
            Debug.Print "WordWrap", .WordWrap
        End With
        
        Debug.Print .Parent
        Debug.Print .Priority
        Debug.Print .QuickStyle
        'Debug.Print .Shading
        'Debug.Print .Table
        Debug.Print .Type
        Debug.Print .UnhideWhenUsed
        Debug.Print .Visibility

    End With

End Sub
