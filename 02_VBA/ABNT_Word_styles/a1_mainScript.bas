Attribute VB_Name = "a1_mainScript"
Option Explicit

Sub styleABNT()
        '------------------------------------------------------------------------------
    ' styleABNT
    '
    ' Description:
    '   This function is the main script of a bunch of routines to create a set of
    '   Microsoft Word styles in accordance with ABNT NBR 14724 - Trabalho AcadÃªmico.
    '
    ' Inputs:
    '   None
    '
    ' Outputs:
    '   None
    '
    ' Remarks:
    '   This routine is used orquestrate the process o creation styles and reorganize
    '   the quick styles gallery. The following styles are created:
    '           - New_normal;
    '           - Text_body;
    '           - Title_unnumbered;
    '           - Title_outside_TOC;
    '           - Title_1;
    '           - Title_2;
    '           - Title_3;
    '           - Title_4; and
    '           - Title_5.
    '   Furthermore, a custom mulilevel list is created and connects to the recently
    '   created styles.
    '
    ' Source
    '   https://github.com/eu-cristofer/reusable-components
    '
    '------------------------------------------------------------------------------

    ' Deletes custom styles from the active document
    Call eraseCustomStyles
 
    ' Decrases the priority of some existing styles in the
    ' active document. The purpose is to keep the customs styles
    ' appearing first in the galery
    Call reducePriority
    
    ' Creates a new paragraph style with specified font size
    ' and font name settings.
    Call createFontSizeName(styleName:="New_normal")
    
    ' Creates a new text body style.
    ' The style inherits settings from createFontSizeName and
    ' adds paragraph alignment, line spacing, and space after settings.
    Call createBody(styleName:="Text_body")
        
    ' From text body settings, it creates outside TOC title
    Call createUnnumberedTitle(styleName:="Title_outside_TOC")
    
    ' From text body settings, it creates unnumered title
    Call createUnnumberedTitle(styleName:="Title_unnumbered")
    
    ' Finally, creates numbered from 1 to 5 titles
    Call createNumberedTitle(styleName:="Title")
    
    ' Create a custom mulilevel list and connects to the recently
    ' created styles
    Call createList
    
    ' In the end it selects the current range and apply Text_body
    ' style.
    Selection.Range.Style = "Text_body"
  
End Sub
