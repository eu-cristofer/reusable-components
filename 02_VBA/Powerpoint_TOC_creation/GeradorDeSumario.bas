Attribute VB_Name = "GeradorDeSumario"
Option Explicit

Private Function SumarioTitle() As String
    ' Builds the slide title string via ChrW so accents survive import.
    SumarioTitle = "Sum" & ChrW(225) & "rio"
End Function

Sub GeraSumario()
    ' Fills the "Sumário" slide with section titles, hyperlinks, and section labels.
    ' The presentation must already contain sections since they define the working data.

    Dim i As Integer
    Dim j As Integer
    Dim k As Integer
    Dim sl As Integer
    Dim titulo() As Variant
    Dim pagina() As Integer
    Dim secoes As Integer
    
    ' Determine the slide index for the "Sumário" title so we know where to write the TOC.
    sl = GetSlideSumario()

        ' Retrieve every section name and its starting slide number.
        With ActivePresentation.SectionProperties
            
            ReDim titulo(.Count)
            ReDim pagina(.Count)
            secoes = .Count
            
            ' Cache section names and slide indices for later use.
            For i = 1 To secoes
                titulo(i - 1) = .Name(i)
                pagina(i - 1) = .FirstSlide(i)
            Next
            
            ' Also remember the final slide index so the last section has a boundary.
            pagina(secoes) = ActivePresentation.Slides.Count
            
        End With

        ' Pull the section names into the placeholder on the Sumário slide.
        With ActivePresentation.Slides(sl).Shapes
            .Placeholders(2).TextFrame.TextRange.Text = "" 'Start with an empty placeholder 2
                
                ' Append each section title (skipping the first) and add a newline.
                For j = 1 To (secoes - 1)
                    .Placeholders(2).TextFrame.TextRange.InsertAfter (titulo(j) & Chr(13))
                    Debug.Print titulo(j)
                Next
        
        End With
        
        ' Turn the inserted titles into hyperlinks pointing to the section start slides.
        For k = 1 To (secoes - 1)
    
            
            With ActivePresentation.Slides(sl).Shapes.Placeholders(2).TextFrame.TextRange.Find(titulo(k)) 'Seleciona o texto
            
                'Transforma o texto em hyperlink
                With .ActionSettings(ppMouseClick)
                    .Action = ppActionHyperlink
                    .Hyperlink.SubAddress = pagina(k)
                End With
        
            End With
            
        Next
        
        ' Varre todos as seoes, a partir da segunda, e insere a seo no campo adequado
        For i = 1 To (secoes - 1)
            
            ' Iterate through every slide that belongs to section i.
            For j = pagina(i) To pagina(i + 1)
                
                ' Loop placeholders to find the one that should be labeled.
                For k = 1 To ActivePresentation.Slides(j).Shapes.Placeholders.Count
                    
                    ' If placeholder 2 is present, write section title in the previous placeholder.
                    If ActivePresentation.Slides(j).Shapes.Placeholders(k).Name = "Text Placeholder 2" Then
                        ActivePresentation.Slides(j).Shapes.Placeholders(k - 1).TextFrame.TextRange = titulo(i)
                    
                    ' Otherwise, look for any placeholder that matches "Text Placeholder".
                    ElseIf InStr(ActivePresentation.Slides(j).Shapes.Placeholders(k).Name, "Text Placeholder") Then
                        ActivePresentation.Slides(j).Shapes.Placeholders(k).TextFrame.TextRange = titulo(i)
                    
                    End If
                    
                Next
            Next
        Next
        
End Sub

Private Function GetSlideSumario() As Integer
    'Iterates every slide to find the title placeholder that reads "Sumário".
    'Using the ChrW constant ensures the accent survives module import.
    
    Debug.Print "******************************************"
    Debug.Print "Processamento da fun" & ChrW(231) & "o GetSlideSum" & ChrW(225) & "rio():"
    
    Dim Sld As Slide

        For Each Sld In ActivePresentation.Slides
    
            On Error GoTo errorhandle

            If Sld.Shapes.Placeholders(1).TextFrame.TextRange.Text = SumarioTitle() Then
                GetSlideSumario = Sld.SlideIndex
            End If

errorhandle:
            
            'Log placeholder errors (usually occurs if placeholder 1 doesn't exist).
            Debug.Print ("Slide " & Sld.SlideNumber & " Erro n" & ChrW(250) & "mero " & Err.Number)
            
            'Disable the error handler so the loop can continue.
            On Error GoTo -1
        
        Next
    Debug.Print ("Slide " & ChrW(205) & "ndice --> " & GetSlideSumario) ' Report final index (0 if not found)

End Function