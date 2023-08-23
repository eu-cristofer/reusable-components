VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} selectTOCLevel 
   Caption         =   "Select the level"
   ClientHeight    =   4836
   ClientLeft      =   108
   ClientTop       =   456
   ClientWidth     =   5784
   OleObjectBlob   =   "selectTOCLevel.frx":0000
   StartUpPosition =   1  'CenterOwner
End
Attribute VB_Name = "selectTOCLevel"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Sub CommandButton1_Click()

    Dim level As Integer
    
    For Each Control In Me.Controls
    check1 = TypeName(Control) = "OptionButton"
    check2 = Control.Value
        If check1 And check2 Then
            Call createTOC(Control.Caption)
            Exit For
        End If
    Next Control
    Me.Hide
End Sub

Sub CommandButton1_Enter()
    Call CommandButton1_Click
End Sub

Private Sub OptionButton1_Click()
    Me.OptionButton1.Value = True
    Me.OptionButton2.Value = False
    Me.OptionButton3.Value = False
    Me.OptionButton4.Value = False
End Sub

Private Sub OptionButton2_Click()
    Me.OptionButton1.Value = False
    Me.OptionButton2.Value = True
    Me.OptionButton3.Value = False
    Me.OptionButton4.Value = False
End Sub

Private Sub OptionButton3_Click()
    Me.OptionButton1.Value = False
    Me.OptionButton2.Value = False
    Me.OptionButton3.Value = True
    Me.OptionButton4.Value = False
End Sub

Private Sub OptionButton4_Click()
    Me.OptionButton1.Value = False
    Me.OptionButton2.Value = False
    Me.OptionButton3.Value = False
    Me.OptionButton4.Value = True
End Sub
