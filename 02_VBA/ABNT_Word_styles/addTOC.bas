Attribute VB_Name = "addTOC"
Option Explicit
Sub a1_addTOC()
    '------------------------------------------------------------------------------
    ' a1_addTOC
    '
    ' Description:
    '   Add the Table of Contents in the document where the cursos is placed.
    '
    ' Inputs:
    '   None
    '
    ' Outputs:
    '   None
    '
    ' Remarks:
    '   This subroutine creates TOC in the current document for the following styles:
    '           - Title_unnumbered;
    '           - Title_1;
    '           - Title_2;
    '           - Title_3; and
    '           - Title_4.
    '   Note that it offers the possibility to vary TOC levels to from 1 up to 4, where
    '   4  will generate a TOC with the above mentioned stylesand 1 willkeep only the
    '   following styles:
    '           - Title_unnumbered; and
    '           - Title_1.  
    '
    ' Source:
    '   https://github.com/eu-cristofer/reusable-components
    '------------------------------------------------------------------------------
    Dim UserForm As Object
    Set UserForm = New selectTOCLevel
    UserForm.Show
End Sub
