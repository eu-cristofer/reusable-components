Attribute VB_Name = "GeradorDeSumario"
Option Explicit

Sub GeraSumario()
'Este código cria um sumário no slide com título sumário
'A referência para a criaçăo do sumário săo as seçőes do documento

    Dim i As Integer
    Dim j As Integer
    Dim k As Integer
    Dim sl As Integer
    Dim titulo() As Variant
    Dim pagina() As Integer
    Dim secoes As Integer
    
    'determina o índice do slide  Sumário
    sl = GetSlideSumario()

        'Identificaçãoo das seções do documento
        With ActivePresentation.SectionProperties
            
            ReDim titulo(.Count)
            ReDim pagina(.Count)
            secoes = .Count
            
            'Guarda os títulos das seçõees e os índices em variável
            For i = 1 To secoes
                titulo(i - 1) = .Name(i)
                pagina(i - 1) = .FirstSlide(i)
            Next
            
            ' Registra o último slide
            pagina(secoes) = ActivePresentation.Slides.Count
            
        End With

        'Escreve no slide índice número sl os tíulos
        With ActivePresentation.Slides(sl).Shapes
            .Placeholders(2).TextFrame.TextRange.Text = "" 'Apaga o o texto do placeholder número 2
                
                'Escreve o título no placeholder a partir do seção número 2
                For j = 1 To (secoes - 1)
                    .Placeholders(2).TextFrame.TextRange.InsertAfter (titulo(j) & Chr(13))
                    Debug.Print titulo(j)
                Next
        
        End With
        
        'Grava o hyperlink no texto ttulo da seoo a parti da segunda seo
        For k = 1 To (secoes - 1) 'For loop para varrer todos ttulos (sees)
    
            
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
            
            ' Varre todas as pginas a partir da segunda seo
            For j = pagina(i) To pagina(i + 1)
                
                ' Varre cada placeholder to slide
                For k = 1 To ActivePresentation.Slides(j).Shapes.Placeholders.Count
                    
                    ' Verifica o nome do placeholder
                    If ActivePresentation.Slides(j).Shapes.Placeholders(k).Name = "Text Placeholder 2" Then
                        ActivePresentation.Slides(j).Shapes.Placeholders(k - 1).TextFrame.TextRange = titulo(i)
                    
                    ' Verifica o nome do placeholder
                    ElseIf InStr(ActivePresentation.Slides(j).Shapes.Placeholders(k).Name, "Text Placeholder") Then
                        ActivePresentation.Slides(j).Shapes.Placeholders(k).TextFrame.TextRange = titulo(i)
                    
                    End If
                    
                Next
            Next
        Next
        
End Sub

Private Function GetSlideSumario() As Integer
'Esta funçăo tem como objetivo encontrar o Slide intitulado "Sumário"
    
    Debug.Print "******************************************"
    Debug.Print "Processamento da funçăo GetSlideSumário():"
    
    Dim Sld As Slide

        For Each Sld In ActivePresentation.Slides
            
            On Error GoTo errorhandle

            If Sld.Shapes.Placeholders(1).TextFrame.TextRange.Text = "Sumário" Then
                GetSlideSumario = Sld.SlideIndex
            End If

errorhandle:
            
            Debug.Print ("Slide " & Sld.SlideNumber & " Erro número " & Err.Number)
            
            'Disables enabled exception in the current
            'procedure and resets it to Nothing.
            On Error GoTo -1
        
        Next
    
    Debug.Print ("Slide Índice --> " & GetSlideSumario)

End Function