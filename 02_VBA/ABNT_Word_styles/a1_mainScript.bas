Attribute VB_Name = "a1_mainScript"
Option Explicit

Sub styleABNT()

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
