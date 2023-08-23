Attribute VB_Name = "Tool_createUserForm"
Option Explicit
Sub createUserForm()
    
    Dim UserForm As Object
    Dim selectedNumber As Integer
    Dim i As Integer
    
    
    ' Create UserForm
    Set UserForm = ActiveDocument.VBProject.VBComponents.Add(3)
    
    With UserForm
        .Properties("Name") = "selectTOCLevel"
        .Properties("Caption") = "Select the level"
        .Properties("Width") = 300
        .Properties("Height") = 270
    End With
    
    ' Add Controls
    With UserForm.designer
        ' Create OptionButtons
        For i = 1 To 4
            .Controls.Add "Forms.OptionButton.1", , True
            .Controls("OptionButton" & i).Caption = i
            .Controls("OptionButton" & i).Left = 10
            .Controls("OptionButton" & i).Top = 10 + 25 * (i - 1)
            .Controls("OptionButton" & i).GroupName = "ItemList"
            If i = 4 Then
                .Controls("OptionButton" & i).Value = True ' Set the default selection to Item 4
            End If
        Next i
        
        ' Create OK Button
        .Controls.Add "Forms.CommandButton.1", , True
        .Controls("CommandButton1").Caption = "OK"
        .Controls("CommandButton1").Left = 100
        .Controls("CommandButton1").Top = 100
    End With
    
    ' Add code on the form for the command buttona
    With UserForm.CodeModule
        Dim X As Integer
        X = .CountOfLines
        .InsertLines X + 1, "Sub CommandButton1_Click()"
        .InsertLines X + 2, ""
        .InsertLines X + 3, "    Dim level As Integer"
        .InsertLines X + 4, "    "
        .InsertLines X + 5, "    For Each Control In Me.Controls"
        .InsertLines X + 6, "    check1 = TypeName(Control) = " & Chr(34) & "OptionButton" & Chr(34)
        .InsertLines X + 7, "    check2 = Control.Value"
        .InsertLines X + 8, "        If check1 And check2 Then"
        .InsertLines X + 9, "            Call createTOC(Control.Caption)"
        .InsertLines X + 10, "            Exit For"
        .InsertLines X + 11, "        End If"
        .InsertLines X + 12, "    Next Control"
        .InsertLines X + 13, "    Me.Hide"
        .InsertLines X + 14, "End Sub"
        .InsertLines X + 15, ""
        .InsertLines X + 16, "Sub CommandButton1_Enter()"
        .InsertLines X + 17, "    Call CommandButton1_Click"
        .InsertLines X + 18, "End Sub"
        .InsertLines X + 19, ""
        .InsertLines X + 20, "Private Sub OptionButton1_Click()"
        .InsertLines X + 21, "    Me.OptionButton1.Value = True"
        .InsertLines X + 22, "    Me.OptionButton2.Value = False"
        .InsertLines X + 23, "    Me.OptionButton3.Value = False"
        .InsertLines X + 24, "    Me.OptionButton4.Value = False"
        .InsertLines X + 25, "End Sub"
        .InsertLines X + 26, ""
        .InsertLines X + 27, "Private Sub OptionButton2_Click()"
        .InsertLines X + 28, "    Me.OptionButton1.Value = False"
        .InsertLines X + 29, "    Me.OptionButton2.Value = True"
        .InsertLines X + 30, "    Me.OptionButton3.Value = False"
        .InsertLines X + 31, "    Me.OptionButton4.Value = False"
        .InsertLines X + 32, "End Sub"
        .InsertLines X + 33, ""
        .InsertLines X + 34, "Private Sub OptionButton3_Click()"
        .InsertLines X + 35, "    Me.OptionButton1.Value = False"
        .InsertLines X + 36, "    Me.OptionButton2.Value = False"
        .InsertLines X + 37, "    Me.OptionButton3.Value = True"
        .InsertLines X + 38, "    Me.OptionButton4.Value = False"
        .InsertLines X + 39, "End Sub"
        .InsertLines X + 40, ""
        .InsertLines X + 41, "Private Sub OptionButton4_Click()"
        .InsertLines X + 42, "    Me.OptionButton1.Value = False"
        .InsertLines X + 43, "    Me.OptionButton2.Value = False"
        .InsertLines X + 44, "    Me.OptionButton3.Value = False"
        .InsertLines X + 45, "    Me.OptionButton4.Value = True"
        .InsertLines X + 46, "End Sub"
    End With
End Sub
